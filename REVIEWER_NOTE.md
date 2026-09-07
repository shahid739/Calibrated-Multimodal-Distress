# Reviewer Note: manuscript/repository alignment

This repository is aligned to the manuscript titled **“A Reproducible Benchmark Protocol for Calibrated Multimodal Proxy-Distress Affect Modeling on Speech Corpora.”**

## Primary validation protocol

The manuscript uses **10-fold leave-one-speaker-out (LOSO)** evaluation on IEMOCAP. One of the 10 speakers is held out per fold. Holding out one entire IEMOCAP session is a different protocol and is not the protocol reported by the current manuscript.

## Result-artifact policy

The manuscript reports the aggregate 10-fold LOSO mean/SD but not the ten individual speaker-fold metric rows. Accordingly:

- `results-fold_results.csv` contains only manuscript-reported aggregate summaries;
- no per-speaker measurements have been reverse-engineered or fabricated;
- `paper_results.yaml` is the canonical registry for values explicitly present in the manuscript.

## Primary reported values

- Fold-averaged proxy-distress Macro-F1: 0.755 +/- 0.030.
- Pooled held-out Macro-F1: 0.814.
- Fold-averaged dialog QWK: 0.784 +/- 0.027.
- Pooled dialog QWK: 0.808.
- Fold-averaged regression MAE: 0.58 +/- 0.04.
- Fold-averaged auxiliary emotion Macro-F1: 0.700 +/- 0.028.
- Auxiliary-emotion ECE: 0.084 -> 0.031 after temperature scaling.
- Binned proxy-distress ECE: 0.072 -> 0.041 after variance-aware calibration.

## Verification commands

```bash
python scripts-show_results.py --results_dir .
python scripts-verify_results.py --results_dir .
python scripts-repository_audit.py --repo .
```

## Computational reproducibility boundary

The public notebook currently implements the correct speaker-level LOSO split and several core paper settings. 

