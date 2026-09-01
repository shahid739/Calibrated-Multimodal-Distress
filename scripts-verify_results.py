```python
""" 

import os
import sys
import argparse
import pandas as pd
import yaml
import numpy as np

def load_paper_results():
    """Load paper results from YAML file"""
    paper_results = {
        'fold_averaged_macro_f1': 0.755,
        'fold_averaged_macro_f1_std': 0.030,
        'pooled_macro_f1': 0.814,
        'pearson_r': 0.712,
        'pearson_r_std': 0.006,
        'dialog_qwk': 0.809,
        'dialog_qwk_std': 0.003,
        'regression_mae': 0.58,
        'regression_mae_std': 0.04,
        'ece_after_scaling': 0.031,
        'ece_after_scaling_std': 0.001,
        'auxiliary_emotion_macro_f1': 0.700,
        'auxiliary_emotion_macro_f1_std': 0.028,
        'moderate_f1': 0.527,
        'moderate_f1_std': 0.026,
        'low_f1': 0.858,
        'low_f1_std': 0.014,
        'high_f1': 0.829,
        'high_f1_std': 0.032,
        'high_recall': 0.794,
        'high_recall_std': 0.015,
    }
    return paper_results

def verify_results(results_dir):
    """Compare generated results with paper results"""
    # Load generated results
    fold_results = pd.read_csv(os.path.join(results_dir, 'fold_results.csv'))
    
    # Compute summary statistics
    generated = {
        'fold_averaged_macro_f1': fold_results['emo_macro_f1'].mean(),
        'fold_averaged_macro_f1_std': fold_results['emo_macro_f1'].std(ddof=1),
        'fold_averaged_uar': fold_results['emo_uar'].mean(),
        'fold_averaged_uar_std': fold_results['emo_uar'].std(ddof=1),
        'fold_averaged_qwk': fold_results['dist_qwk'].mean(),
        'fold_averaged_qwk_std': fold_results['dist_qwk'].std(ddof=1),
    }
    
    paper = load_paper_results()
    
    print("\n" + "="*60)
    print("Result Verification: Generated vs Paper")
    print("="*60)
    
    all_match = True
    for key in ['fold_averaged_macro_f1', 'fold_averaged_uar', 'fold_averaged_qwk']:
        gen = generated.get(key, 0)
        paper_val = paper.get(key.replace('fold_averaged_', ''), 0)
        if paper_val is None:
            continue
        
        diff = abs(gen - paper_val)
        is_match = diff < 0.02  # Allow 2% tolerance
        
        print(f"\n{key.replace('_', ' ').title()}:")
        print(f"  Generated: {gen:.4f}")
        print(f"  Paper:     {paper_val:.4f}")
        print(f"  Difference: {diff:.4f}")
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
    parser.add_argument("--results_dir", type=str, required=True, help="Path to results directory")
    args = parser.parse_args()
    
    verify_results(args.results_dir)