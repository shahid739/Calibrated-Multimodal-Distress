#!/usr/bin/env python3
"""Artifact-level consistency check for the DERS-X repository.

This script verifies that the archived five-session fold summary is
consistent with the corresponding values in paper_results.yaml.

It does NOT retrain the model and does NOT claim to reconstruct pooled
metrics, Pearson correlation, or calibrated ECE unless the complete
underlying prediction artifacts are available.

Usage:
    python scripts-verify_results.py --results_dir .
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd
import yaml


EXPECTED_FOLDS = ["Ses01", "Ses02", "Ses03", "Ses04", "Ses05"]

# Absolute tolerances reflect rounding in the archived CSV.
TOLERANCES = {
    "fold_averaged_macro_f1": 0.002,
    "fold_averaged_macro_f1_std": 0.002,
    "fold_averaged_uar": 0.002,
    "fold_averaged_uar_std": 0.002,
    "fold_averaged_qwk": 0.002,
    "fold_averaged_qwk_std": 0.003,
    "regression_mae": 0.002,
    "regression_mae_std": 0.005,
}


def load_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a YAML mapping in {path}")
    return data


def check_required_columns(frame: pd.DataFrame) -> None:
    required = {
        "fold",
        "emo_macro_f1",
        "emo_uar",
        "dist_qwk",
        "dist_mae",
    }
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(
            "results-fold_results.csv is missing required columns: "
            + ", ".join(missing)
        )


def summarize(frame: pd.DataFrame) -> dict[str, float]:
    return {
        "fold_averaged_macro_f1": float(frame["emo_macro_f1"].mean()),
        "fold_averaged_macro_f1_std": float(frame["emo_macro_f1"].std(ddof=1)),
        "fold_averaged_uar": float(frame["emo_uar"].mean()),
        "fold_averaged_uar_std": float(frame["emo_uar"].std(ddof=1)),
        "fold_averaged_qwk": float(frame["dist_qwk"].mean()),
        "fold_averaged_qwk_std": float(frame["dist_qwk"].std(ddof=1)),
        "regression_mae": float(frame["dist_mae"].mean()),
        "regression_mae_std": float(frame["dist_mae"].std(ddof=1)),
    }


def verify(results_dir: Path) -> bool:
    fold_path = results_dir / "results-fold_results.csv"
    paper_path = results_dir / "paper_results.yaml"

    if not fold_path.exists():
        raise FileNotFoundError(f"Required file not found: {fold_path}")

    frame = pd.read_csv(fold_path)
    check_required_columns(frame)
    paper = load_yaml(paper_path)

    observed_folds = frame["fold"].astype(str).tolist()
    if observed_folds != EXPECTED_FOLDS:
        print("[FAIL] Fold identifiers/order do not match the archived five-session protocol.")
        print(f"       Expected: {EXPECTED_FOLDS}")
        print(f"       Observed: {observed_folds}")
        return False

    generated = summarize(frame)

    print("=" * 72)
    print("DERS-X archived-result consistency check")
    print("Protocol: five-fold leave-one-session-out (Ses01-Ses05)")
    print("=" * 72)

    all_ok = True
    for key, generated_value in generated.items():
        if key not in paper:
            print(f"[FAIL] Missing key in paper_results.yaml: {key}")
            all_ok = False
            continue

        paper_value = float(paper[key])
        tolerance = TOLERANCES[key]
        difference = abs(generated_value - paper_value)
        ok = difference <= tolerance
        label = "PASS" if ok else "FAIL"
        print(
            f"[{label}] {key}: archived={generated_value:.6f}, "
            f"registry={paper_value:.6f}, abs_diff={difference:.6f}, "
            f"tol={tolerance:.6f}"
        )
        all_ok = all_ok and ok

    print("-" * 72)
    print(
        "Not checked here: pooled Macro-F1/QWK, Pearson correlation, or calibrated ECE.\n"
        "Those quantities require the complete prediction/calibration artifacts and should\n"
        "not be inferred from the five-row fold summary alone."
    )
    print("=" * 72)

    if all_ok:
        print("[PASS] Archived fold summary is consistent with paper_results.yaml.")
    else:
        print("[FAIL] One or more archived values are inconsistent with paper_results.yaml.")
    return all_ok


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check archived DERS-X fold results against paper_results.yaml"
    )
    parser.add_argument(
        "--results_dir",
        type=Path,
        default=Path("."),
        help="Repository/results directory (default: current directory)",
    )
    args = parser.parse_args()

    try:
        return 0 if verify(args.results_dir.resolve()) else 1
    except (FileNotFoundError, ValueError, KeyError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
