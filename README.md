# Calibrated Multimodal Proxy-Distress Affect Modeling on Speech Corpora (Short Title)

## DERS-X

DERS-X (Distress Emotion Recognition System - Extended) is a reproducible research benchmark for calibrated multimodal affect modeling from speech and text. The manuscript and this repository use **proxy-distress / distress-like affect** as a benchmark-specific construct derived from public speech-emotion annotations. The work does **not** claim clinical distress diagnosis, emergency triage, real-world crisis detection, or operational emergency-call readiness.

The framework combines:

- Wav2Vec 2.0 Base acoustic representations;
- DistilBERT-base-uncased transcript representations;
- bidirectional cross-modal attention;
- continuous proxy-distress regression with an auxiliary nine-class emotion objective;
- post-hoc calibration;
- dialog-level aggregation/context analysis;
- cross-corpus transfer; and
- controlled acoustic, channel, and transcript degradation tests.

## Evaluation protocol

The primary IEMOCAP evaluation is **10-fold leave-one-speaker-out (LOSO)**. IEMOCAP contains five dyadic sessions and 10 speakers; each primary fold holds out **one individual speaker**. The held-out speaker is excluded from model development, target construction, model selection, and calibration for that fold. Development data are partitioned at the dialog level into training, validation, and calibration subsets to avoid dialog leakage.


## Headline paper results

| Summary | Reported value |
| --- | ---: |
| Fold-averaged proxy-distress Macro-F1 | **0.755 +/- 0.030** |
| Pooled held-out proxy-distress Macro-F1 | **0.814** |
| Pooled held-out accuracy | **0.843** |
| Pooled held-out UAR | **0.748** |
| Fold-averaged dialog QWK | **0.784 +/- 0.027** |
| Pooled held-out dialog QWK | **0.808** |
| Fold-averaged regression MAE | **0.58 +/- 0.04** |
| Abstract-reported Pearson correlation | **0.712 +/- 0.006** |
| Fold-averaged auxiliary emotion Macro-F1 | **0.700 +/- 0.028** |
| Pooled auxiliary emotion Macro-F1 | **approximately 0.61** |
| Auxiliary-emotion ECE after temperature scaling | **0.031** (from 0.084) |
| Binned proxy-distress ECE after variance-aware calibration | **0.041** (from 0.072) |

Fold-averaged, pooled held-out, and seed-wise summaries are different aggregation levels and must not be treated as interchangeable.

## Repository structure

| File | Purpose |
| --- | --- |
| `DERS-X-B.ipynb` | End-to-end research notebook. Its core IEMOCAP split is speaker-level LOSO |
| `paper_results.yaml` | Canonical machine-readable registry of numerical values explicitly reported in the current manuscript. |
| `results-fold_results.csv` | Aggregate 10-fold LOSO summaries; no fabricated per-speaker rows. |
| `results-ablation_summary.csv` | Paper Tables 10-13 ablation values. |
| `results-calibration_summary.csv` | Paper calibration results. |
| `results-emotion_classwise.csv` | Pooled auxiliary-emotion class-wise F1 values. |
| `results-cross_corpus_summary.csv` | Paper cross-corpus transfer summaries. |
| `results-degradation_summary.csv` | Paper Tables 17-19 degradation results. |
| `results-modality_degradation_summary.csv` | Paper Table 20 modality results under combined degradation. |
| `results-attention_summary.csv` | Paper attention-share diagnostic values. |
| `scripts-show_results.py` | Displays the paper-aligned result tables. |
| `scripts-verify_results.py` | Checks consistency among the paper-aligned YAML and CSV result artifacts. |
| `scripts-repository_audit.py` | Audits repository protocol/documentation consistency and can flag notebook-level paper-exact gaps. |
| `Methodology.txt` | Concise paper-aligned methodology summary. |
| `docs-experimental_setup.md` | Model, training, degradation, and computing setup. |
| `docs-reproducibility.md` | Reproduction and artifact-verification guidance. |
| `REVIEWER_NOTE.md` | Reviewer-facing scope and reproducibility note. |
| `CODE_PROVENANCE.md` | Provenance and result-artifact boundaries. |
| `NOTEBOOK_ALIGNMENT_REQUIRED.md` | Exact code-level differences that still require author action for a fully paper-exact notebook. |
| `REPOSITORY_REPLACEMENT_MANIFEST.md` | One-time upload/replace/delete checklist. |
| `environment.yml` | Recommended Conda environment aligned with the reported CUDA 11.8 software stack. |
| `requirements.txt` | Pip-compatible Python dependencies. |
| `Installation.txt` | Installation and validation commands. |
| `CITATION.cff` | Software citation metadata aligned to the manuscript title. |

## Dataset information

The raw third-party corpora are **not redistributed** in this repository. Obtain each dataset from its official provider and comply with the corresponding license/access terms.

| Dataset | Role in manuscript | Official source |
| --- | --- | --- |
| IEMOCAP | Primary multimodal benchmark; 10-speaker LOSO evaluation | https://sail.usc.edu/iemocap/ |
| MSP-Podcast | Bidirectional cross-corpus transfer | https://lab-msp.com/MSP/MSP-Conversation.html |
| MUSAN | Background-noise degradation experiments | https://www.openslr.org/17/ |

## Target construction and leakage controls

For each IEMOCAP LOSO fold, activation is standardized with **training-partition statistics only**. The four proxy-distress levels are then constructed using the 25th, 50th, and 75th percentiles of the training-fold standardized target. The held-out speaker is never used to estimate target statistics or quartile thresholds.

The remaining development dialogs are split approximately 80%/10%/10% into training, validation, and calibration partitions. Dialogs are disjoint across these partitions.

## Main model and optimization settings

Paper-reported configuration:

- Wav2Vec 2.0 Base acoustic encoder;
- DistilBERT-base-uncased text encoder;
- 16 kHz mono waveform input;
- maximum 128 WordPiece tokens;
- 256-dimensional modality token space;
- 4-head bidirectional cross-modal attention;
- dropout 0.2;
- effective batch size 8;
- AdamW optimizer;
- encoder learning rate `1e-5`;
- newly initialized layer learning rate `1e-4`;
- 10% linear warmup;
- weight decay 0.01;
- gradient clipping norm 1.0;
- up to 20 epochs;
- early-stopping patience 3;
- training seeds 13, 29, and 47;
- multitask weights `lambda_emo = 1.0` and `lambda_reg = 0.5`.


## Calibration

The paper reports two distinct calibration analyses and they should remain separate:

1. **Auxiliary emotion classification:** temperature scaling reduces ECE from **0.084 to 0.031**.
2. **Binned proxy-distress output:** variance-aware calibration reduces ECE from **0.072 to 0.041**.

These ECE values concern different model outputs and calibration procedures and are not directly interchangeable.

## Robustness protocol reported by the paper

The paper evaluates additive background noise at 20, 15, 10, and 5 dB SNR; AMR-NB channel compression at 12.2 kbps; 10% VoIP packet loss with mean burst length 3 packets; transcript corruption at 10%, 20%, and 30% WER; and combined 15 dB + 15% WER, 10 dB + 25% WER, and 5 dB + 35% WER conditions. Five perturbation realizations are used per condition with seeds 13, 29, 47, 101, and 202.


## Inspect and verify archived paper values

Create the environment:

```bash
conda env create -f environment.yml
conda activate dersx_env
```

or install Python dependencies with:

```bash
python -m pip install -r requirements.txt
```

Display paper-aligned result tables:

```bash
python scripts-show_results.py --results_dir .
```

Verify cross-file consistency:

```bash
python scripts-verify_results.py --results_dir .
```

Audit the repository after replacing the old files:

```bash
python scripts-repository_audit.py --repo .
```

For the stricter notebook implementation audit:

```bash
python scripts-repository_audit.py --repo . --strict-notebook
```

## Reproducing experiments

Do not interpret `scripts-verify_results.py` as a neural-model retraining test. It verifies that the archived manuscript-facing result files agree with one another.

## Reproducibility boundary

This repository intentionally distinguishes **paper-result preservation** from **full computational rerun equivalence**. The result registry and CSVs are aligned to the current manuscript. The public notebook already uses the correct individual-speaker LOSO split.

## Data and code availability

Source code and manuscript-facing reproducibility artifacts are publicly available in this repository. IEMOCAP, MSP-Podcast, and MUSAN remain third-party datasets and are not redistributed here.

For strongest reproducibility, the final archival release should additionally include, when permitted:

- the exact IEMOCAP 5,479-utterance subset manifest;
- complete held-out prediction exports used to compute pooled metrics;
- per-run environment reports and split IDs; and
- a versioned archival DOI (for example, a Zenodo release DOI).

## Citation

Citation metadata are provided in `CITATION.cff`. After creating the final immutable release, add the release DOI to both `CITATION.cff` and the manuscript if required by the target journal.

## License

The source code is distributed under the MIT License. Dataset licenses are separate and remain controlled by their original providers.
