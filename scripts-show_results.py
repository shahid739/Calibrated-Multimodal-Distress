#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd
import yaml

FILES = [
    "results-fold_results.csv",
    "results-ablation_summary.csv",
    "results-calibration_summary.csv",
    "results-emotion_classwise.csv",
    "results-cross_corpus_summary.csv",
    "results-degradation_summary.csv",
    "results-modality_degradation_summary.csv",
    "results-attention_summary.csv",
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results_dir", default=".")
    args = ap.parse_args()
    root = Path(args.results_dir)
    registry = yaml.safe_load((root / "paper_results.yaml").read_text(encoding="utf-8"))
    print("DERS-X paper-aligned registry")
    print("Protocol:", registry["metadata"]["evaluation_protocol"])
    print("Held-out unit:", registry["metadata"]["held_out_unit"])
    print("Primary folds:", registry["metadata"]["n_primary_folds"])
    print()
    for fn in FILES:
        path = root / fn
        if path.exists():
            print("="*80)
            print(fn)
            print(pd.read_csv(path).to_string(index=False))

if __name__ == "__main__":
    main()
