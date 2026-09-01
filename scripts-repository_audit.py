#!/usr/bin/env python3
"""Pre-resubmission repository audit for the DERS-X PeerJ package.

This is a lightweight structural check. It does not validate scientific
correctness of the manuscript and does not retrain the model.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import json
import sys

import pandas as pd
import yaml


REQUIRED_README_HEADINGS = [
    "## Title",
    "## Description",
    "## Dataset Information",
    "## Code Information",
    "## Usage Instructions",
    "## Requirements",
    "## Methodology",
    "## Citation",
    "## License",
    "## Contributing",
]

REQUIRED_FILES = [
    "README.md",
    "DERS-X-B.ipynb",
    "paper_results.yaml",
    "results-fold_results.csv",
    "scripts-show_results.py",
    "scripts-verify_results.py",
    "docs-reproducibility.md",
    "docs-experimental_setup.md",
    "Methodology.txt",
    "environment.yml",
    "requirements.txt",
    "CITATION.cff",
    "LICENSE.txt",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "Installation.txt",
]

EXPECTED_FOLDS = ["Ses01", "Ses02", "Ses03", "Ses04", "Ses05"]


def pass_line(message: str) -> None:
    print(f"[PASS] {message}")


def fail_line(message: str) -> None:
    print(f"[FAIL] {message}")


def warn_line(message: str) -> None:
    print(f"[WARN] {message}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.repo.resolve()
    failures = 0

    print(f"Auditing: {root}")

    for name in REQUIRED_FILES:
        if (root / name).exists():
            pass_line(f"Found {name}")
        else:
            fail_line(f"Missing required/recommended file: {name}")
            failures += 1

    if (root / "CITATION.cff.txt").exists():
        fail_line("CITATION.cff.txt still exists; delete it after adding CITATION.cff")
        failures += 1

    readme_path = root / "README.md"
    if readme_path.exists():
        readme = readme_path.read_text(encoding="utf-8", errors="replace")
        for heading in REQUIRED_README_HEADINGS:
            if heading in readme:
                pass_line(f"README contains {heading}")
            else:
                fail_line(f"README missing {heading}")
                failures += 1
        if "conda activate dersx_env" in readme:
            pass_line("README uses the environment name dersx_env")
        else:
            fail_line("README does not use 'conda activate dersx_env'")
            failures += 1

    fold_path = root / "results-fold_results.csv"
    if fold_path.exists():
        folds = pd.read_csv(fold_path)["fold"].astype(str).tolist()
        if folds == EXPECTED_FOLDS:
            pass_line("Archived fold IDs match the five-session protocol")
        else:
            fail_line(f"Unexpected archived fold IDs: {folds}")
            failures += 1

    notebook_path = root / "DERS-X-B.ipynb"
    if notebook_path.exists():
        try:
            payload = json.loads(notebook_path.read_text(encoding="utf-8"))
            code = "\n".join(
                "".join(cell.get("source", []))
                if isinstance(cell.get("source", []), list)
                else str(cell.get("source", ""))
                for cell in payload.get("cells", [])
                if cell.get("cell_type") == "code"
            )
            if "sorted(iemocap.session_id.astype(str).unique())" in code:
                pass_line("Notebook primary plan derives folds from session_id")
            elif "sorted(iemocap.speaker_id.unique())" in code:
                fail_line(
                    "Notebook still derives primary folds from speaker_id, while the archived fold table uses sessions"
                )
                failures += 1
            else:
                warn_line("Could not automatically identify notebook primary fold discovery")
        except Exception as exc:
            fail_line(f"Could not parse notebook: {exc}")
            failures += 1

    cff_path = root / "CITATION.cff"
    if cff_path.exists():
        try:
            cff = yaml.safe_load(cff_path.read_text(encoding="utf-8"))
            repo_url = str(cff.get("repository-code", ""))
            if repo_url.endswith("shahid739/Calibrated-Multimodal-Distress"):
                pass_line("CITATION.cff repository URL is correct")
            else:
                fail_line(f"CITATION.cff repository-code looks wrong: {repo_url}")
                failures += 1
        except Exception as exc:
            fail_line(f"Could not parse CITATION.cff: {exc}")
            failures += 1


    # Stale flat-repository artifacts that previously described another layout or codebase.
    hard_stale = ["src-init.py", "MANIFEST.in.txt"]
    for name in hard_stale:
        if (root / name).exists():
            fail_line(f"Stale/broken packaging artifact still present: {name}")
            failures += 1

    setup_path = root / "setup.py"
    if setup_path.exists():
        setup_text = setup_path.read_text(encoding="utf-8", errors="replace")
        if "find_packages()" in setup_text and not (root / "dersx").is_dir() and not (root / "src").is_dir():
            fail_line("setup.py uses find_packages() but no package directory is present")
            failures += 1

    for name in ["configs-default_config.yaml", "configs-audio_only.yaml", "configs-text_only.yaml"]:
        path = root / name
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="replace")
            if "max_audio_seconds: 10" in text or "AbstractTTS/IEMOCAP" in text:
                warn_line(f"Legacy config may conflict with canonical notebook: {name}")

    prepare_path = root / "scripts-prepare_data.py"
    if prepare_path.exists():
        text = prepare_path.read_text(encoding="utf-8", errors="replace")
        if "AbstractTTS/IEMOCAP" in text:
            warn_line("scripts-prepare_data.py uses an alternate Hugging Face IEMOCAP source; remove or label it as non-paper-exact")

    files_path = root / "files.txt"
    if files_path.exists() and "DERS-X-Benchmark/" in files_path.read_text(encoding="utf-8", errors="replace"):
        warn_line("files.txt documents an obsolete repository layout")

    figure_readme = root / "figures-README.md"
    if figure_readme.exists():
        warn_line("figures-README.md is present; confirm its listed figure files and values actually exist/match paper_results.yaml")

    predictions = root / "results-utterance_predictions.csv"
    if predictions.exists():
        try:
            n = len(pd.read_csv(predictions))
            if n <= 5:
                warn_line(
                    "results-utterance_predictions.csv contains only a few rows; pooled metrics cannot be independently reconstructed from a preview-only file"
                )
            else:
                pass_line(f"Prediction export contains {n} rows")
        except Exception as exc:
            warn_line(f"Could not inspect prediction export: {exc}")

    print("-" * 72)
    if failures:
        print(f"Audit completed with {failures} failure(s).")
        return 1
    print("Audit completed with no structural failures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
