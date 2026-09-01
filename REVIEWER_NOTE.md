# Note for Reviewers: Reproducibility and Result Provenance

## Canonical Result Sources

The repository uses the following hierarchy:

1. `paper_results.yaml` - canonical machine-readable registry of manuscript/repository values.
2. `results-fold_results.csv` - archived five-fold IEMOCAP session-level summary.
3. `results-utterance_predictions.csv` - held-out prediction export; pooled-metric reconstruction requires the complete export.
4. `results-ablation_summary.csv` - archived ablation summary.

## Primary Archived Fold Values

The five archived IEMOCAP folds are `Ses01` through `Ses05`. The principal fold-level summaries recorded in `paper_results.yaml` are:

| Metric | Archived value |
|---|---:|
| Fold-averaged Macro-F1 | 0.738 +/- 0.014 |
| Fold-averaged UAR | 0.708 +/- 0.013 |
| Fold-averaged QWK | 0.784 +/- 0.016 |
| Regression MAE | 0.58 +/- 0.04 |

The pooled held-out Macro-F1 is recorded separately as 0.814. Fold-averaged and pooled statistics are not interchangeable.

## Validation Grouping

The archived fold identifiers are sessions (`Ses01`-`Ses05`). The final paper-aligned implementation and manuscript should therefore describe the primary archived analysis as **five-fold leave-one-session-out evaluation**.

## Quick Artifact Verification

From the repository root:

```bash
python scripts-show_results.py --method csv --results_dir .
python scripts-verify_results.py --results_dir .
```

The verification script checks internal consistency between the five fold rows and the corresponding entries in `paper_results.yaml`. This is an artifact-level consistency check; it does not claim that a new neural training run will be bit-for-bit identical across hardware/software stacks.

## End-to-End Reproduction

The executable workflow is provided in `DERS-X-B.ipynb`. A full rerun requires:

- access to the third-party corpora under their original terms;
- the final paper-aligned session-level validation implementation;
- the documented software environment; and
- the exact IEMOCAP subset manifest if the reported analysis used a fixed 5,479-utterance subset.

Raw third-party datasets are not redistributed in this repository.

## Pooled Metrics

Independent reconstruction of pooled metrics requires the complete held-out prediction export. If `results-utterance_predictions.csv` is only a short preview, it should be replaced by the complete retained export before the final archival release, subject to dataset licensing constraints.

## Citation and Archival Version

The repository includes `CITATION.cff`. After the final GitHub release is archived with Zenodo, the version-specific DOI should be cited in the manuscript's Code/Data Availability statement.
