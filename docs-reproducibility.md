# Reproducibility Guide

## 1. Purpose

This repository supports two distinct reproducibility tasks:

1. **Artifact-level verification**: inspect the archived fold/result files and check their consistency with `paper_results.yaml` without retraining the neural model.
2. **Fresh end-to-end rerun**: obtain the third-party datasets, configure local paths, and execute the paper-aligned notebook.

These two tasks should not be conflated. Artifact verification is fast and deterministic; full neural reruns are data-, hardware-, and environment-dependent.

## 2. Canonical Sources

The following files define the final repository record:

- `paper_results.yaml` - canonical numerical registry;
- `results-fold_results.csv` - five session-level fold summaries;
- `DERS-X-B.ipynb` - canonical end-to-end reference implementation after protocol synchronization;
- `environment.yml` - authoritative Conda environment definition;
- `requirements.txt` - pip convenience dependencies.

The final repository should not contain contradictory duplicate values in README/reviewer notes/configuration files.

## 3. Data Access

### IEMOCAP

Official source: https://sail.usc.edu/iemocap/

IEMOCAP is a third-party corpus and is not redistributed here. Obtain access from USC and place the extracted corpus at a local path referenced by the notebook configuration.

### MSP-Podcast

Official source: https://lab-msp.com/MSP/MSP-Conversation.html

Obtain the dataset from its official distributor and set the corresponding local path in the notebook.

### MUSAN

Official source: https://www.openslr.org/17/

MUSAN is used for controlled acoustic degradation/noise experiments where applicable.

## 4. Primary IEMOCAP Validation Protocol

The archived primary result table is indexed by five folds:

- `Ses01`
- `Ses02`
- `Ses03`
- `Ses04`
- `Ses05`

Accordingly, the final paper-aligned implementation should use **five-fold leave-one-session-out evaluation** for the archived primary result set. One complete IEMOCAP session is the held-out test group in each fold.

Development data are further divided at the dialog level to avoid overlap among training, validation, and calibration partitions. Fold-specific target statistics must be fitted only on the training portion and then applied to validation, calibration, and test data.

## 5. Exact Sample Provenance

If the reported experiment used a fixed 5,479-utterance IEMOCAP subset, the exact utterance identifiers are part of the reproducibility record. The final release should therefore include the exact subset manifest used by the reported run, or a deterministic documented rule that reconstructs the identical set from the official corpus.

Do not claim a paper-exact rerun if the exact subset cannot be reconstructed.

## 6. Preprocessing

### Audio

The paper-aligned notebook:

- converts audio to mono when required;
- resamples to 16 kHz;
- retains variable-length utterances; and
- performs dynamic padding within minibatches through the model feature extractor.

No fixed 10-second or 12-second truncation should be documented for the paper-aligned path unless it is actually present in the final canonical notebook.

### Text

The paper-aligned notebook:

- lowercases and normalizes transcript text;
- normalizes/removes common filled pauses;
- preserves selected non-verbal tags where configured; and
- tokenizes with a maximum of 128 wordpieces.

## 7. Model

The final canonical implementation uses:

- Wav2Vec 2.0 Base acoustic encoder;
- DistilBERT Base Uncased text encoder;
- latent projection dimension 256;
- four-head bidirectional cross-modal attention;
- multitask emotion and continuous proxy-distress objectives; and
- post-hoc calibration fitted on the calibration partition only.

See `DERS-X-B.ipynb` for the executable architecture and `Methodology.txt` for the plain-text summary.

## 8. Randomness and Training Configuration

The notebook defines the primary random seeds as:

- 13
- 29
- 47

For the paper-aligned profile, use the parameters encoded in the final canonical notebook rather than stale values in legacy/example configuration files.

The notebook records per-run configuration, environment information, split identifiers, metrics, and prediction artifacts in its run directory. Preserve these outputs for auditability.

## 9. Environment Setup

### Conda

```bash
conda env create -f environment.yml
conda activate dersx_env
```

### Pip alternative

```bash
python -m pip install -r requirements.txt
```

`environment.yml` is the authoritative repository environment. Do not publish a second conflicting software-version table in this document.

## 10. Verify Archived Results Without Retraining

From the repository root:

```bash
python scripts-show_results.py --method csv --results_dir .
python scripts-verify_results.py --results_dir .
```

The verification script checks:

- the five expected session fold identifiers;
- fold-averaged Macro-F1;
- fold-averaged UAR;
- fold-averaged QWK; and
- fold-averaged regression MAE,

against the corresponding values in `paper_results.yaml` within small absolute tolerances that account for the rounding precision of the archived CSV.

The script intentionally does **not** claim to reconstruct pooled metrics, Pearson correlation, or calibrated ECE from files that do not contain the complete data required for those calculations.

## 11. Fresh End-to-End Rerun

1. Obtain the third-party datasets from the official sources.
2. Create the software environment.
3. Open `DERS-X-B.ipynb`.
4. Set dataset paths.
5. Provide the exact IEMOCAP subset manifest when required for paper-exact reproduction.
6. Confirm that the notebook's primary evaluation groups are `Ses01` through `Ses05` rather than individual speaker IDs.
7. Select the paper-aligned profile.
8. Execute the notebook sequentially.
9. Preserve generated split IDs, predictions, metrics, environment report, and logs.
10. Compare generated summaries with `paper_results.yaml` while keeping fold-level and pooled summaries distinct.

## 12. Complete Prediction Export

To independently reconstruct pooled held-out metrics, `results-utterance_predictions.csv` must contain the complete held-out prediction set. A short illustrative preview is not sufficient for pooled-metric verification.

The final release should therefore replace any preview-only prediction file with the complete export from the retained analysis archive, provided that doing so does not violate dataset licensing restrictions.

## 13. Hardware and Numerical Variation

The notebook records the GPU model, CUDA runtime, CPU count, RAM, and peak allocated GPU memory in a generated environment report. This should be preserved with full reruns.

Floating-point differences may arise across GPU architectures, CUDA/cuDNN versions, and library builds. Such differences should be distinguished from changes in the evaluation protocol, data split, preprocessing, or model configuration.

## 14. Archival Release

After all repository files are synchronized:

1. create a versioned GitHub release;
2. archive that release with Zenodo; and
3. cite the version-specific Zenodo DOI in the manuscript's Code/Data Availability statement.

Further, pooled metrics are reported from paper_results.yaml but cannot be independently reconstructed from the repository. Moreover, I have used all available IEMOCAP utterances