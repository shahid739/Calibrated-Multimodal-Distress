# Changelog

All notable repository-level reproducibility and documentation are recorded here.

## [1.0.0] - 2026-09-01

### Reproducibility release preparation

- Added/updated the public DERS-X reference notebook and archived result artifacts.
- Standardized the repository README around the manuscript's reproducibility requirements.
- Added explicit dataset access, installation, usage, methodology, citation, license, and contribution guidance.
- Designated `paper_results.yaml` as the machine-readable registry of manuscript-aligned numerical results.
- Added reviewer-facing result-display and artifact-consistency checks.
- Clarified that fold-averaged, pooled, dialog-level, and calibration quantities are different summaries and must not be interchanged.
- Added repository/provenance checks to identify validation-protocol or documentation drift before archival release.

### Archival note

The final citable release should be archived in a long-term repository such as Zenodo after the manuscript, code, environment, and result artifacts have been synchronized. The version-specific DOI should then be recorded in the manuscript's Code/Data Availability statement.

> Numerical manuscript results are maintained in `paper_results.yaml` rather than duplicated in this changelog.
