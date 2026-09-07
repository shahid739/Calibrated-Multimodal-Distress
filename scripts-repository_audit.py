#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path
import yaml

REQUIRED = [
    'README.md','paper_results.yaml','results-fold_results.csv','results-ablation_summary.csv',
    'results-calibration_summary.csv','results-emotion_classwise.csv','results-cross_corpus_summary.csv',
    'results-degradation_summary.csv','results-modality_degradation_summary.csv','results-attention_summary.csv',
    'Methodology.txt','docs-experimental_setup.md','docs-reproducibility.md','REVIEWER_NOTE.md',
    'CODE_PROVENANCE.md','NOTEBOOK_ALIGNMENT_REQUIRED.md','CITATION.cff','environment.yml','requirements.txt',
    'scripts-show_results.py','scripts-verify_results.py'
]
STALE_PATTERNS = [
    r'five[- ]fold leave[- ]one[- ]session[- ]out',
    r'five[- ]session',
    r'Ses01\s*[-–]\s*Ses05',
    r'0\.738\s*(?:\+/-|±)\s*0\.014',
]
DOCS = ['README.md','Methodology.txt','docs-experimental_setup.md','docs-reproducibility.md','REVIEWER_NOTE.md']

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',default='.')
    ap.add_argument('--strict-notebook',action='store_true')
    args=ap.parse_args(); root=Path(args.repo)
    errors=[]; warnings=[]
    for fn in REQUIRED:
        if not (root/fn).exists(): errors.append(f'missing required file: {fn}')
    obsolete=root/'scripts-patch_dersx_b_session_protocol.py'
    if obsolete.exists(): errors.append('delete obsolete scripts-patch_dersx_b_session_protocol.py (it converts the notebook to the wrong session-level protocol)')
    for fn in DOCS:
        p=root/fn
        if not p.exists(): continue
        txt=p.read_text(encoding='utf-8',errors='ignore')
        for pat in STALE_PATTERNS:
            if re.search(pat,txt,re.I): errors.append(f'{fn}: stale protocol/result text matches /{pat}/')
    yp=root/'paper_results.yaml'
    if yp.exists():
        y=yaml.safe_load(yp.read_text(encoding='utf-8'))
        if y.get('metadata',{}).get('evaluation_protocol')!='leave-one-speaker-out (LOSO)': errors.append('paper_results.yaml protocol mismatch')
        if int(y.get('metadata',{}).get('n_primary_folds',0))!=10: errors.append('paper_results.yaml n_primary_folds must be 10')
    cff=root/'CITATION.cff'
    if cff.exists():
        c=yaml.safe_load(cff.read_text(encoding='utf-8'))
        expected='A Reproducible Benchmark Protocol for Calibrated Multimodal Proxy-Distress Affect Modeling on Speech Corpora'
        if c.get('title')!=expected: errors.append('CITATION.cff title does not exactly match manuscript')
    nb=root/'DERS-X-B.ipynb'
    if nb.exists():
        raw=nb.read_text(encoding='utf-8',errors='ignore')
        for token in ['prepare_iemocap_loso','heldout_speaker','speaker_id','lambda_emo','lambda_reg']:
            if token not in raw: errors.append(f'notebook missing expected speaker-LOSO/core token: {token}')
        if 'five_fold_leave_one_session_out' in raw: errors.append('notebook contains stale five-session primary protocol')
        gap_checks={
            'context model still uses DialogContextGRU instead of manuscript two-layer Transformer':'DialogContextGRU' in raw,
            'variance-aware / Platt proxy-distress calibration not detectable':('variance' not in raw.lower() or 'platt' not in raw.lower()),
            'Gaussian acoustic-noise fallback remains present':'deterministic_gaussian_fallback' in raw,
            'paper burst packet-loss process is not detectable':('mean_burst' not in raw.lower() and 'burst_length' not in raw.lower()),
            'paper 60/20/20 ASR corruption is not detectable':('0.60' not in raw and '60%' not in raw),
        }
        for msg,bad in gap_checks.items():
            if bad:
                (errors if args.strict_notebook else warnings).append('NOTEBOOK: '+msg)
    else:
        warnings.append('DERS-X-B.ipynb not present in this replacement bundle; notebook checks run after overlaying files onto the GitHub repository.')
    if warnings:
        print('WARNINGS:')
        for w in warnings: print(' -',w)
    if errors:
        print('FAIL:')
        for e in errors: print(' -',e)
        raise SystemExit(1)
    print('PASS: repository manuscript-facing files are aligned to the current paper protocol/results.')
    if warnings: print('The warnings above must be resolved before claiming full paper-exact notebook rerun equivalence.')

if __name__=='__main__':
    main()
