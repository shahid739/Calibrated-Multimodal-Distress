#!/usr/bin/env python3
"""Display archived DERS-X result artifacts without overstating reproducibility.

This utility reads the repository's archived CSV/YAML artifacts. It does not
retrain the model. A complete held-out prediction export is required before
pooled metrics can be independently reconstructed from predictions.

Usage:
    python scripts-show_results.py --method csv --results_dir .
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import yaml


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    return value if isinstance(value, dict) else {}


def show_results_from_csv(results_dir: Path) -> int:
    fold_path = results_dir / "results-fold_results.csv"
    prediction_path = results_dir / "results-utterance_predictions.csv"
    registry_path = results_dir / "paper_results.yaml"

    if not fold_path.exists():
        print(f"[ERROR] Missing required file: {fold_path}")
        return 2

    fold_results = pd.read_csv(fold_path)
    registry = load_yaml(registry_path)

    print("=" * 72)
    print("DERS-X archived result artifacts")
    print("=" * 72)
    print("\nFold-level archive")
    print(fold_results.to_string(index=False))

    required = {"emo_macro_f1", "emo_uar", "dist_qwk", "dist_mae"}
    if required.issubset(fold_results.columns):
        print("\nFold-summary statistics")
        print(
            f"  Macro-F1: {fold_results['emo_macro_f1'].mean():.4f} "
            f"+/- {fold_results['emo_macro_f1'].std(ddof=1):.4f}"
        )
        print(
            f"  UAR:      {fold_results['emo_uar'].mean():.4f} "
            f"+/- {fold_results['emo_uar'].std(ddof=1):.4f}"
        )
        print(
            f"  QWK:      {fold_results['dist_qwk'].mean():.4f} "
            f"+/- {fold_results['dist_qwk'].std(ddof=1):.4f}"
        )
        print(
            f"  MAE:      {fold_results['dist_mae'].mean():.4f} "
            f"+/- {fold_results['dist_mae'].std(ddof=1):.4f}"
        )

    if registry:
        print("\nCanonical manuscript registry (selected values)")
        keys = [
            "fold_averaged_macro_f1",
            "fold_averaged_macro_f1_std",
            "fold_averaged_uar",
            "fold_averaged_uar_std",
            "fold_averaged_qwk",
            "fold_averaged_qwk_std",
            "pooled_macro_f1",
            "pooled_qwk",
            "regression_mae",
            "regression_mae_std",
            "ece_before_calibration",
            "ece_after_temperature_scaling",
        ]
        for key in keys:
            if key in registry:
                print(f"  {key}: {registry[key]}")

    print("\nHeld-out prediction artifact")
    if prediction_path.exists():
        predictions = pd.read_csv(prediction_path)
        print(f"  Rows present: {len(predictions)}")
        if len(predictions) <= 5:
            print(
                "  [WARN] This appears to be a preview/sample rather than a complete "
                "held-out export. Do not claim independent pooled-metric reconstruction "
                "from this file."
            )
        elif len(predictions):
            print("\nPrediction sample")
            print(predictions.head(10).to_string(index=False))
    else:
        print("  [WARN] results-utterance_predictions.csv is not present.")

    print("\nNote: this command displays archived artifacts; it does not retrain DERS-X.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Display archived DERS-X results")
    parser.add_argument("--method", choices=["csv"], default="csv")
    parser.add_argument("--results_dir", type=Path, default=Path("."))
    args = parser.parse_args()
    return show_results_from_csv(args.results_dir.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
