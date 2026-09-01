#!/usr/bin/env python3
"""Patch DERS-X-B.ipynb from individual-speaker LOSO to five-session holdout.

Why this exists
---------------
The archived primary fold file in the repository uses Ses01-Ses05, while the
current public notebook plans folds from speaker_id values such as Ses01F.
Those are different evaluation protocols. This utility changes the notebook
so its primary IEMOCAP fold unit is session_id.

IMPORTANT
---------
Run this only if the submitted manuscript's primary archived analysis is the
five-session protocol represented by results-fold_results.csv. If the paper
actually reports ten individual-speaker folds, do not use this patch; recover
the genuine speaker-level result artifacts instead.

Usage
-----
    python scripts-patch_dersx_b_session_protocol.py \
        DERS-X-B.ipynb DERS-X-B.session-patched.ipynb
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


def source_text(cell: dict) -> str:
    src = cell.get("source", [])
    if isinstance(src, list):
        return "".join(src)
    return str(src)


def set_source(cell: dict, text: str) -> None:
    # Preserve standard notebook line-list representation.
    cell["source"] = text.splitlines(keepends=True)


def replace_once(text: str, old: str, new: str, label: str) -> tuple[str, int]:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected exactly one {label} occurrence; found {count}.")
    return text.replace(old, new, 1), 1


def patch_notebook(payload: dict) -> tuple[dict, list[str]]:
    changes: list[str] = []
    cells = payload.get("cells", [])
    if not isinstance(cells, list):
        raise ValueError("Notebook has no valid cells list.")

    # 1) Configuration: representative fold IDs must be session IDs.
    config_done = False
    for cell in cells:
        if cell.get("cell_type") != "code":
            continue
        text = source_text(cell)
        if "budget_representative_fold" in text and "Ses01F" in text:
            text = text.replace('budget_representative_fold: str = "Ses01F"',
                                'budget_representative_fold: str = "Ses01"')
            text = text.replace(
                'budget_seed_check_folds: Tuple[str, ...] = ("Ses01F", "Ses03M", "Ses05M")',
                'budget_seed_check_folds: Tuple[str, ...] = ("Ses01", "Ses03", "Ses05")',
            )
            text = text.replace(
                'budget_degradation_folds: Tuple[str, ...] = ("Ses01F",)',
                'budget_degradation_folds: Tuple[str, ...] = ("Ses01",)',
            )
            text = text.replace(
                'budget_ablation_folds: Tuple[str, ...] = ("Ses01F",)',
                'budget_ablation_folds: Tuple[str, ...] = ("Ses01",)',
            )
            set_source(cell, text)
            config_done = True
            changes.append("Converted budget/reference fold IDs from speaker IDs to session IDs.")
            break
    if not config_done:
        raise RuntimeError("Could not locate the notebook configuration fold-ID block.")

    # 2) Replace the IEMOCAP holdout splitter with session-level semantics.
    splitter_done = False
    splitter_pattern = re.compile(
        r"def prepare_iemocap_loso\(.*?\n\n\ndef prepare_all_dialog_split",
        flags=re.DOTALL,
    )
    replacement = '''def prepare_iemocap_loso(df: pd.DataFrame, heldout_session: str, seed: int) -> Dict[str, Any]:
    """Prepare one five-fold IEMOCAP leave-one-session-out split.

    The complete held-out session is test data. Training, validation, and
    calibration data come only from the other four sessions and are split by
    dialog, preserving dialog disjointness.
    """
    test = df[df.session_id.astype(str) == heldout_session].copy()
    if test.empty:
        raise ValueError(f"No rows for held-out session {heldout_session}")

    pool = df[df.session_id.astype(str) != heldout_session].copy()
    train, val, cal = split_dialogs_three_way(pool, seed)

    split_sets = {
        k: set(v.dialog_id.astype(str))
        for k, v in {"train": train, "val": val, "cal": cal, "test": test}.items()
    }
    for a in split_sets:
        for b in split_sets:
            if a < b and split_sets[a] & split_sets[b]:
                raise AssertionError(f"Dialog leakage between {a} and {b}")

    development_sessions = set(train.session_id.astype(str)) | set(val.session_id.astype(str)) | set(cal.session_id.astype(str))
    if heldout_session in development_sessions:
        raise AssertionError("Held-out session leaked into development data")

    stats = fit_target_stats(train, "IEMOCAP")
    return {
        "train": apply_target_stats(train, stats),
        "val": apply_target_stats(val, stats),
        "cal": apply_target_stats(cal, stats),
        "test": apply_target_stats(test, stats),
        "target_stats": stats,
    }


def prepare_all_dialog_split'''

    for cell in cells:
        if cell.get("cell_type") != "code":
            continue
        text = source_text(cell)
        if "def prepare_iemocap_loso" in text and "def prepare_all_dialog_split" in text:
            new_text, n = splitter_pattern.subn(replacement, text, count=1)
            if n != 1:
                raise RuntimeError("Could not safely replace prepare_iemocap_loso().")
            set_source(cell, new_text)
            splitter_done = True
            changes.append("Changed prepare_iemocap_loso() to hold out session_id rather than speaker_id.")
            break
    if not splitter_done:
        raise RuntimeError("Could not locate prepare_iemocap_loso() cell.")

    # 3) Patch the main fold runner metadata/variable names.
    runner_done = False
    for cell in cells:
        if cell.get("cell_type") != "code":
            continue
        text = source_text(cell)
        if "def run_iemocap_fold" in text and "heldout_speaker" in text:
            text = text.replace("heldout_speaker: str", "heldout_session: str")
            text = text.replace("prepare_iemocap_loso(df, heldout_speaker, seed)",
                                "prepare_iemocap_loso(df, heldout_session, seed)")
            text = text.replace("/ heldout_speaker", "/ heldout_session")
            text = text.replace('"protocol": "strict_LOSO"',
                                '"protocol": "five_fold_leave_one_session_out"')
            text = text.replace('"heldout_speaker": heldout_speaker',
                                '"heldout_session": heldout_session')
            # Save session ID alongside speaker/dialog IDs for split auditing.
            text = text.replace(
                'part[["utterance_id", "dialog_id", "speaker_id"]].to_csv(',
                'part[["utterance_id", "dialog_id", "speaker_id", "session_id"]].to_csv(',
            )
            # run_main_loso loop labels are cosmetic but should match the protocol.
            text = text.replace("for speaker in folds:", "for session in folds:")
            text = text.replace("                speaker,\n                seed,", "                session,\n                seed,")
            text = text.replace('"speaker": speaker,', '"session": session,')
            text = text.replace("/ speaker\n", "/ session\n")
            set_source(cell, text)
            runner_done = True
            changes.append("Updated run_iemocap_fold() metadata and main-loop labels for held-out sessions.")
            break
    if not runner_done:
        raise RuntimeError("Could not locate run_iemocap_fold() cell.")

    # 4) Primary execution plan: derive folds from session_id, not speaker_id.
    plan_done = False
    for cell in cells:
        if cell.get("cell_type") != "code":
            continue
        text = source_text(cell)
        if "def execute_plan" in text and "sorted(iemocap.speaker_id.unique())" in text:
            text = text.replace(
                "speakers = sorted(iemocap.speaker_id.unique())\n    plan = build_plan(speakers)",
                "folds = sorted(iemocap.session_id.astype(str).unique())\n    plan = build_plan(folds)",
            )
            set_source(cell, text)
            plan_done = True
            changes.append("Changed execute_plan() fold discovery from speaker_id to session_id.")
            break
    if not plan_done:
        raise RuntimeError("Could not locate execute_plan() speaker-based fold discovery.")

    # 5) Add a notebook-level protocol note in a new Markdown cell near the top.
    note = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Primary validation protocol\n",
            "\n",
            "The paper-aligned primary IEMOCAP evaluation uses five-fold **leave-one-session-out** validation (`Ses01`-`Ses05`). Each held-out session contains both speakers in that dyad and is excluded from training, validation, and calibration data for that fold.\n",
        ],
    }
    insert_at = 1 if len(cells) >= 1 else 0
    cells.insert(insert_at, note)
    changes.append("Inserted an explicit notebook Markdown note describing the five-session protocol.")

    return payload, changes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="Path to current DERS-X-B.ipynb")
    parser.add_argument("output", type=Path, help="Path for patched notebook")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Input notebook not found: {args.input}", file=sys.stderr)
        return 2

    with args.input.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    try:
        patched, changes = patch_notebook(payload)
    except (RuntimeError, ValueError) as exc:
        print(f"Patch aborted: {exc}", file=sys.stderr)
        return 3

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(patched, handle, ensure_ascii=False, indent=1)
        handle.write("\n")

    print(f"Patched notebook written to: {args.output}")
    for change in changes:
        print(f" - {change}")
    print("Review the patched notebook before replacing the original.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
