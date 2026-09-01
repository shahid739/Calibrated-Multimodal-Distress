"""
Verify Results Against Paper for DERS-X

This script compares the generated results with the values reported in the paper.

Usage:
    python scripts-verify_results.py --results_dir ./
"""

import os
import sys
import argparse
import pandas as pd
import yaml

def load_paper_results():
    """Load paper results from paper_results.yaml"""
    try:
        with open('paper_results.yaml', 'r') as f:
            paper = yaml.safe_load(f)
        return paper
    except FileNotFoundError:
        print("Warning: paper_results.yaml not found. Using hardcoded values.")
        # Fallback hardcoded values
        return {
            'fold_averaged_macro_f1': 0.738,
            'fold_averaged_macro_f1_std': 0.014,
            'pooled_macro_f1': 0.814,
            'pearson_r': 0.712,
            'pearson_r_std': 0.006,
            'dialog_qwk': 0.808,
            'dialog_qwk_std': 0.012,
            'regression_mae': 0.58,
            'regression_mae_std': 0.04,
            'ece_after_scaling': 0.031,
            'ece_after_scaling_std': 0.001,
            'auxiliary_emotion_macro_f1': 0.700,
            'auxiliary_emotion_macro_f1_std': 0.028,
        }

def verify_results(results_dir):
    """Compare generated results with paper results"""
    try:
        fold_results = pd.read_csv(os.path.join(results_dir, 'results-fold_results.csv'))
    except FileNotFoundError:
        print("Error: results-fold_results.csv not found.")
        return False

    # Compute generated summary
    generated = {
        'fold_averaged_macro_f1': fold_results['emo_macro_f1'].mean(),
        'fold_averaged_macro_f1_std': fold_results['emo_macro_f1'].std(ddof=1),
        'fold_averaged_uar': fold_results['emo_uar'].mean(),
        'fold_averaged_uar_std': fold_results['emo_uar'].std(ddof=1),
        'fold_averaged_qwk': fold_results['dist_qwk'].mean(),
        'fold_averaged_qwk_std': fold_results['dist_qwk'].std(ddof=1),
        'fold_averaged_mae': fold_results['dist_mae'].mean(),
        'fold_averaged_mae_std': fold_results['dist_mae'].std(ddof=1),
        'fold_averaged_ece': fold_results['emo_ece'].mean(),
        'fold_averaged_ece_std': fold_results['emo_ece'].std(ddof=1),
    }

    paper = load_paper_results()

    print("\n" + "="*60)
    print("DERS-X Result Verification: Generated vs Paper")
    print("="*60)

    comparisons = [
        ('fold_averaged_macro_f1', paper.get('fold_averaged_macro_f1', 0.738), generated['fold_averaged_macro_f1']),
        ('fold_averaged_uar', paper.get('fold_averaged_uar', 0.708), generated['fold_averaged_uar']),
        ('fold_averaged_qwk', paper.get('dialog_qwk', 0.808), generated['fold_averaged_qwk']),
        ('fold_averaged_mae', paper.get('regression_mae', 0.58), generated['fold_averaged_mae']),
        ('fold_averaged_ece', paper.get('ece_after_scaling', 0.031), generated['fold_averaged_ece']),
    ]

    all_match = True
    for name, paper_val, gen_val in comparisons:
        diff = abs(gen_val - paper_val)
        tolerance = 0.02  # 2% tolerance
        is_match = diff <= tolerance

        print(f"\n{name.replace('_', ' ').title()}:")
        print(f"  Generated: {gen_val:.4f}")
        print(f"  Paper:     {paper_val:.4f}")
        print(f"  Diff:      {diff:.4f}")
        print(f"  Match:     {'✓ YES' if is_match else '✗ NO'}")

        if not is_match:
            all_match = False

    print("\n" + "="*60)
    if all_match:
        print("✓ All results match the paper within tolerance.")
        print("  The code successfully reproduces the reported results.")
    else:
        print("✗ Some results do not match the paper.")
        print("  Please check your configuration and data.")
    print("="*60)

    return all_match

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify results against paper")
    parser.add_argument("--results_dir", type=str, default='./', help="Path to results directory")
    args = parser.parse_args()

    verify_results(args.results_dir)