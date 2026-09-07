# DERS-X Reproducibility Guide (paper-aligned)

## 1. What is preserved here

`paper_results.yaml` and the `results-*.csv` files preserve numerical values explicitly reported by the current manuscript. These artifacts are intended for transparent manuscript/repository consistency checking.

The manuscript's primary protocol is **10-fold leave-one-speaker-out (LOSO)** on IEMOCAP. It reports aggregate means/standard deviations but does not publish the ten separate held-out-speaker metric rows. Consequently, this repository does not fabricate missing fold rows.

## 2. What `scripts-verify_results.py` verifies

The verifier checks agreement among the machine-readable result registry and manuscript-facing CSV tables. It does not train the model and does not prove that every number can be regenerated from raw data on the current machine.

Run:

```bash
python scripts-verify_results.py --results_dir .
```

## 3. Repository audit

After replacing old files, run:

```bash
python scripts-repository_audit.py --repo .
```

For notebook-level implementation checks:

```bash
python scripts-repository_audit.py --repo . --strict-notebook
```

The strict audit is expected to fail until every item in `NOTEBOOK_ALIGNMENT_REQUIRED.md` is implemented/restored and verified.

## 4. Data requirements

The repository does not redistribute IEMOCAP, MSP-Podcast, or MUSAN.

Obtain:

- IEMOCAP from the official USC distribution;
- MSP-Podcast from its official provider;
- MUSAN from OpenSLR.

Set the corresponding paths in the notebook.

## 5. Exact IEMOCAP sample

The manuscript reports 5,479 IEMOCAP utterances. The current notebook includes an audit against the reported class counts. If the documented preprocessing rules do not uniquely reproduce all 5,479 rows, a paper-exact run requires an exact utterance-ID manifest.

Do not create a synthetic manifest. Deposit the genuine retained ID list from the original analysis if it is available.

## 6. Primary split construction

Each IEMOCAP fold holds out one individual speaker. The held-out speaker must be absent from training, validation, and calibration. Development splits are dialog-disjoint.

Target standardization and quartile thresholds are fitted on training data only. The same fold-specific parameters are applied to all non-training partitions.

## 7. Paper-exact profile

Use the notebook's `paper_exact` profile for the complete 10-speaker x 3-seed primary plan and the full robustness/ablation scope. The default fast/budget profile is not a substitute for the complete paper evaluation.

## 8. Result aggregation

Keep these summaries separate:

- fold-averaged LOSO metrics;
- pooled held-out metrics;
- seed-wise metrics;
- utterance-level metrics;
- dialog-level metrics.

The archived paper-facing values are in `paper_results.yaml`.

## 9. Calibration

Temperature scaling for auxiliary emotion and variance-aware calibration for binned proxy-distress must be treated as separate analyses. Calibration parameters are fitted on calibration data only.

## 10. Degradation reproducibility

A paper-exact robustness rerun requires the mechanisms described in the manuscript: MUSAN noise, codec-accurate AMR-NB, bursty VoIP packet loss, and the stated ASR/phoneme-confusion transcript corruption procedure. The current notebook has some approximations that are documented in `NOTEBOOK_ALIGNMENT_REQUIRED.md`; do not describe those approximations as paper-exact.

## 11. Recommended retained outputs

For each final run, preserve:

- environment report;
- exact split/utterance identifiers;
- target statistics and thresholds;
- checkpoints or checkpoint hashes;
- held-out continuous predictions;
- held-out binned predictions;
- auxiliary emotion logits/probabilities;
- calibrated predictions;
- degradation seeds and perturbation metadata;
- aggregate tables and figures.

For full reconstruction of pooled metrics, publish the held-out prediction export when dataset licensing permits publication of identifiers.

## 12. Archival release

After the final repository is validated, create an immutable tagged release and archive it (for example through Zenodo), then add the resulting DOI to the manuscript and `CITATION.cff` if appropriate.
