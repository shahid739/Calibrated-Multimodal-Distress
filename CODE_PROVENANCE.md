# Code and Result Provenance

This file defines which repository artifacts should be treated as authoritative.

## Authoritative hierarchy

| Priority | Artifact | Role |
|---:|---|---|
| 1 | `paper_results.yaml` | Canonical registry of reported numerical results. |
| 2 | `results-fold_results.csv` | Archived five-session primary fold table. |
| 3 | `DERS-X-B.ipynb` | Canonical executable reference implementation after validation-protocol synchronization. |
| 4 | `environment.yml` | Authoritative Conda environment specification. |
| 5 | `docs-reproducibility.md` | Human-readable reproduction workflow. |


## Primary validation grouping

The archived fold table contains exactly five identifiers: `Ses01`, `Ses02`, `Ses03`, `Ses04`, and `Ses05`. The final canonical implementation should therefore use the same **leave-one-session-out** grouping for the archived primary analysis.

Individual-speaker folds such as `Ses01F` or `Ses01M` represent a different validation protocol and must not be described as the source of the five archived session-level rows unless separate speaker-level results are explicitly reported.

## Audio preprocessing

For the canonical paper-aligned path, documentation should follow the executable notebook. The current reference implementation uses 16-kHz audio and dynamic minibatch padding. Stale references to fixed 10-second or 12-second truncation should be removed unless the final canonical notebook actually applies such truncation.

## Legacy/example configurations

The flat `configs-*.yaml` files may be retained for demonstrations or older workflows, but they should not be presented as paper-exact if their encoder names, duration limits, batch sizes, or validation protocol differ from the canonical notebook.

## Result verification boundaries

`scripts-verify_results.py` verifies the internal consistency of archived fold summaries. It should not claim to regenerate pooled metrics from an incomplete prediction sample, and it should not compare a fold-level QWK value against a pooled QWK key or a fold-level ECE column against a post-temperature-scaling ECE value unless those quantities are demonstrably identical.

## Files that must come from the retained analysis archive

The following cannot be safely reconstructed from summary statistics alone:

1. the exact IEMOCAP utterance/subset; and
2. the complete held-out prediction.

