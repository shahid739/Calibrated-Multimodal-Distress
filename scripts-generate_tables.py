#!/usr/bin/env python
"""
Table Generation Script for DERS-X
"""

import os
import argparse
import pandas as pd
import numpy as np
from pathlib import Path


def mean_std(series):
    return series.mean(), series.std(ddof=1)


def generate_summary_table(fold_results):
    """Generate mean ± std summary table"""
    metric_cols = [c for c in fold_results.columns if c not in ["exp", "fold", "held_out"]]
    rows = []
    for c in metric_cols:
        if pd.api.types.is_numeric_dtype(fold_results[c]):
            m, s = mean_std(fold_results[c])
            rows.append({"metric": c, "mean": m, "std": s})
    return pd.DataFrame(rows).sort_values("metric")


def generate_latex_table(df, caption="", label=""):
    """Generate LaTeX table string"""
    tex = df.to_latex(index=False, float_format=lambda x: f"{x:.4f}")
    if caption:
        tex = tex.replace("\\begin{table}", f"\\begin{{table}}\n\\caption{{{caption}}}")
    if label:
        tex = tex.replace(f"\\caption{{{caption}}}", f"\\caption{{{caption}}}\\label{{{label}}}")
    return tex


def main():
    parser = argparse.ArgumentParser(description="Generate paper tables")
    parser.add_argument("--results_dir", type=str, required=True, help="Results directory")
    parser.add_argument("--output_dir", type=str, default="tables", help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # Load results
    fold_results = pd.read_csv(os.path.join(args.results_dir, "fold_results.csv"))
    predictions = pd.read_csv(os.path.join(args.results_dir, "utterance_predictions.csv"))

    # Generate summary
    summary = generate_summary_table(fold_results)
    summary.to_csv(os.path.join(args.output_dir, "summary.csv"), index=False)

    # Save LaTeX
    with open(os.path.join(args.output_dir, "summary.tex"), "w") as f:
        f.write(generate_latex_table(summary, caption="LOSO Summary", label="tab:loso_summary"))

    print(f"Tables saved to: {args.output_dir}")


if __name__ == "__main__":
    main()