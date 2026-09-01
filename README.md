# DERS-X: A Reproducible Benchmark Protocol for Calibrated Multimodal Proxy-Distress Affect Modeling on Speech Corpora

## Title

**DERS-X: A Reproducible Benchmark Protocol for Calibrated Multimodal Proxy-Distress Affect Modeling on Speech Corpora**

## Description

DERS-X (Distress Emotion Recognition System - Extended) is a research benchmark for calibrated multimodal affect modeling from speech and text. The implementation combines:

- Wav2Vec 2.0 acoustic representations;
- DistilBERT transcript representations;
- bidirectional cross-modal attention;
- continuous proxy-distress regression with an auxiliary emotion-recognition objective; and
- post-hoc calibration and uncertainty analysis.

The target is a **benchmark-specific distress-like affect construct** derived from public speech-emotion annotations. It is not a clinical diagnosis, emergency-triage system, or real-world distress detector.

## Repository Structure

| File | Purpose |
|---|---|
| `DERS-X-B.ipynb` | Canonical end-to-end reference implementation for data parsing, model training, calibration, evaluation, robustness tests, and ablations. The final repository version should implement the same five-session holdout protocol as the archived primary results. |
| `paper_results.yaml` | Machine-readable registry of the numerical values reported by the manuscript/repository. |
| `results-fold_results.csv` | Archived fold-level summary for the five IEMOCAP session folds. |
| `results-utterance_predictions.csv` | Held-out prediction export. For pooled-metric reconstruction this file must contain the complete held-out prediction set, not only a preview/sample. |
| `results-ablation_summary.csv` | Archived ablation summary. |
| `scripts-show_results.py` | Displays archived result tables. |
| `scripts-verify_results.py` | Checks internal consistency between archived fold results and `paper_results.yaml`. |
| `scripts-repository_audit.py` | Performs a pre-resubmission structural audit of required documentation and validation-protocol consistency. |
| `docs-reproducibility.md` | Detailed reproduction and verification instructions. |
| `docs-experimental_setup.md` | Model, training, and computing setup. |
| `Methodology.txt` | Plain-text methodological summary. |
| `environment.yml` | Recommended Conda environment. |
| `requirements.txt` | Pip-compatible dependency list. |
| `Installation.txt` | Plain-text installation and quick-start commands. |
| `CITATION.cff` | Machine-readable software citation metadata. |
| `LICENSE.txt` | MIT software license. |
| `CONTRIBUTING.md` | Contribution guidelines. |
| `CODE_OF_CONDUCT.md` | Community conduct guidelines. |

## Dataset Information

The raw third-party corpora are **not redistributed** in this repository. Researchers must obtain them from their official sources and comply with the corresponding licenses/terms.

| Dataset | Role | Official source | Redistribution note |
|---|---|---|---|
| IEMOCAP | Primary multimodal speech-emotion benchmark | https://sail.usc.edu/iemocap/ | USC-controlled access; obtain from the official distributor. |
| MSP-Podcast | Cross-corpus / dimensional-affect evaluation | https://lab-msp.com/MSP/MSP-Conversation.html | Obtain under the dataset's own access terms. |
| MUSAN | Acoustic degradation/noise experiments | https://www.openslr.org/17/ | Obtain from OpenSLR under its stated license. |

### IEMOCAP evaluation unit

The archived primary fold table is indexed by **five held-out IEMOCAP sessions (`Ses01`-`Ses05`)**. The final paper-aligned notebook and manuscript should use the same terminology: **five-fold leave-one-session-out evaluation**. Each IEMOCAP session contains a dyad; therefore, holding out an entire session excludes both speakers in that session from model development for that fold.

## Code Information

The neural architecture and end-to-end experiment workflow are implemented in `DERS-X-B.ipynb`. Reviewer-facing scripts provide a lightweight way to inspect and verify the archived result artifacts without retraining the neural models.

The primary notebook is self-contained and does not require the legacy flat `configs-*.yaml` files. To avoid presenting stale settings as paper-exact, remove those unused legacy configuration files unless you deliberately maintain them as clearly labeled examples. For paper-exact reproduction, use the parameters defined in the final paper-aligned notebook and the documented environment.

## Primary Archived Results

`paper_results.yaml` is the canonical machine-readable registry for reported numerical values. The principal archived values currently include:

| Metric | Value |
|---|---:|
| Fold-averaged Macro-F1 | 0.738 +/- 0.014 |
| Fold-averaged UAR | 0.708 +/- 0.013 |
| Fold-averaged QWK | 0.784 +/- 0.016 |
| Pooled held-out Macro-F1 | 0.814 |
| Pooled QWK | 0.808 |
| Regression MAE | 0.58 +/- 0.04 |
| Temperature-scaling ECE | 0.031 (from 0.084 before calibration) |

Fold-averaged and pooled metrics summarize different aggregation levels and should not be treated as interchangeable.

## Usage Instructions

### 1. Clone the repository

```bash
git clone https://github.com/shahid739/Calibrated-Multimodal-Distress.git
cd Calibrated-Multimodal-Distress
```

### 2. Create the environment

```bash
conda env create -f environment.yml
conda activate dersx_env
```

Alternatively, install the pip dependencies:

```bash
python -m pip install -r requirements.txt
```

### 3. Inspect the archived results

```bash
python scripts-show_results.py --method csv --results_dir .
```

### 4. Verify archived fold-summary consistency

```bash
python scripts-verify_results.py --results_dir .
```

This command checks whether the five archived fold rows are internally consistent with the corresponding values stored in `paper_results.yaml`. It is an **artifact-consistency check**, not a substitute for a complete retraining run.

### 5. Run a fresh end-to-end experiment

1. Obtain the required third-party datasets from their official sources.
2. Configure the local dataset paths in `DERS-X-B.ipynb`.
3. For a paper-exact IEMOCAP rerun, provide the exact retained IEMOCAP subset manifest used for the reported analysis if the notebook requests one.
4. Select the paper-aligned experiment profile.
5. Execute the notebook cells sequentially.
6. Preserve the generated environment report, split IDs, predictions, metrics, and run logs.

A fresh neural training run can be computationally expensive and may show small hardware/library-dependent numerical variation. The archived result files provide the fixed reference values used for manuscript consistency checks.

## Requirements

The recommended environment is defined by `environment.yml`. `requirements.txt` is provided for pip-based installation.

Core software includes Python, PyTorch, torchaudio, Transformers, NumPy, pandas, SciPy, scikit-learn, matplotlib, librosa, soundfile, PyYAML, and related runtime utilities. A CUDA-capable NVIDIA GPU is strongly recommended for full model training; the artifact-verification scripts can run on CPU.

## Methodology

The paper-aligned workflow is summarized in `Methodology.txt` and described in greater detail in `docs-reproducibility.md`.

At a high level, the workflow:

1. parses and audits the speech corpora;
2. performs fold-specific target construction using training data only;
3. holds out one complete IEMOCAP session per primary fold;
4. keeps development partitions dialog-disjoint;
5. encodes audio with Wav2Vec 2.0 and text with DistilBERT;
6. fuses the two modalities using bidirectional cross-modal attention;
7. optimizes the multitask objectives;
8. fits calibration parameters using calibration data only; and
9. reports fold-level and pooled held-out metrics separately.

Audio is resampled to 16 kHz and handled as variable-length utterances with dynamic minibatch padding in the paper-aligned notebook. Text is normalized and tokenized with a maximum of 128 wordpieces.

## Reproducibility and Data Availability

The repository contains source code, configuration/environment files, archived fold summaries, and supporting result artifacts. Raw IEMOCAP/MSP-Podcast data are not redistributed because they are third-party resources governed by their own access terms.

For strongest reproducibility, the final release should also include:

- the exact IEMOCAP utterance/subset manifest used by the reported analysis, when applicable;
- the complete held-out prediction export used to compute pooled metrics; and
- a versioned archival DOI for the final repository snapshot.

## Citation

Software citation metadata are provided in `CITATION.cff`. After the final GitHub release is archived, cite the version-specific Zenodo DOI in the manuscript and repository documentation.

## License

The source code is distributed under the MIT License. See `LICENSE.txt`.

Dataset licenses are separate from the software license and remain controlled by the original dataset providers.

## Contributing

See `CONTRIBUTING.md` for contribution instructions and `CODE_OF_CONDUCT.md` for community guidelines.

## Reproducibility Documentation

Additional details are available in:

- `docs-reproducibility.md`
- `docs-experimental_setup.md`
- `REVIEWER_NOTE.md`
- `CODE_PROVENANCE.md`
Further, pooled metrics are reported from paper_results.yaml but cannot be independently reconstructed from the repository. Moreover, I have used all available IEMOCAP utterances