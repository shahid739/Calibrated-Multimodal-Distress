#!/usr/bin/env python3
import argparse
from pathlib import Path
import math
import pandas as pd
import yaml

def close(a,b,tol=1e-9):
    return math.isclose(float(a),float(b),rel_tol=0,abs_tol=tol)

def need(cond,msg,errors):
    if not cond: errors.append(msg)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results_dir",default=".")
    args=ap.parse_args(); root=Path(args.results_dir)
    errors=[]
    y=yaml.safe_load((root/'paper_results.yaml').read_text(encoding='utf-8'))
    need(y['metadata']['evaluation_protocol']=='leave-one-speaker-out (LOSO)','YAML protocol must be LOSO',errors)
    need(y['metadata']['held_out_unit']=='individual IEMOCAP speaker','YAML held-out unit must be individual speaker',errors)
    need(int(y['metadata']['n_primary_folds'])==10,'YAML must report 10 primary folds',errors)
    fold=pd.read_csv(root/'results-fold_results.csv')
    fa=fold.loc[fold.record_type=='fold_averaged'].iloc[0]
    po=fold.loc[fold.record_type=='pooled_held_out'].iloc[0]
    need(int(fa.n_folds)==10,'fold summary n_folds != 10',errors)
    need(close(fa.macro_f1,y['primary_results']['fold_averaged']['proxy_distress_macro_f1']['mean']),'fold Macro-F1 mismatch',errors)
    need(close(fa.macro_f1_sd,y['primary_results']['fold_averaged']['proxy_distress_macro_f1']['sd']),'fold Macro-F1 SD mismatch',errors)
    need(close(fa.qwk,y['primary_results']['fold_averaged']['dialog_qwk']['mean']),'fold QWK mismatch',errors)
    need(close(po.macro_f1,y['primary_results']['pooled_held_out']['proxy_distress_macro_f1']),'pooled Macro-F1 mismatch',errors)
    need(close(po.uar,y['primary_results']['pooled_held_out']['proxy_distress_uar']),'pooled UAR mismatch',errors)
    need(close(po.accuracy,y['primary_results']['pooled_held_out']['proxy_distress_accuracy']),'pooled accuracy mismatch',errors)
    cal=pd.read_csv(root/'results-calibration_summary.csv')
    a=cal.loc[cal.output=='auxiliary_emotion'].iloc[0]
    p=cal.loc[cal.output=='binned_proxy_distress'].iloc[0]
    need(close(a.ece_before,y['calibration']['auxiliary_emotion']['ece_before_temperature_scaling']),'aux ECE-before mismatch',errors)
    need(close(a.ece_after,y['calibration']['auxiliary_emotion']['ece_after_temperature_scaling']),'aux ECE-after mismatch',errors)
    need(close(p.ece_before,y['calibration']['binned_proxy_distress']['ece_before_variance_aware_calibration']),'proxy ECE-before mismatch',errors)
    need(close(p.ece_after,y['calibration']['binned_proxy_distress']['ece_after_variance_aware_calibration']),'proxy ECE-after mismatch',errors)
    deg=pd.read_csv(root/'results-degradation_summary.csv')
    need(len(deg)==14,'degradation table should have 14 manuscript rows',errors)
    need(not ((deg.snr_db.fillna(-999)==0).any()),'unexpected 0-dB row present',errors)
    abl=pd.read_csv(root/'results-ablation_summary.csv')
    stale=' '.join(abl.variant.astype(str)).lower()
    for token in ['arcface','maxout','entropy weighting','entropy_weighting','auxiliary prosody','auxiliary_prosody']:
        need(token not in stale,f'stale ablation token present: {token}',errors)
    if errors:
        print('FAIL')
        for e in errors: print(' -',e)
        raise SystemExit(1)
    print('PASS: manuscript-facing YAML/CSV result artifacts are internally consistent.')
    print('NOTE: this is an artifact-consistency check, not a model retraining test.')

if __name__=='__main__':
    main()
