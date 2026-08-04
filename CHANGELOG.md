# Changelog

## [1.0.0] - 2026-08-04

### Added
- Initial release of DERS-X framework
- Wav2Vec 2.0 acoustic encoder
- DistilBERT text encoder
- Cross-modal attention fusion
- Distress Representation Block (DRB)
- Multi-task learning (emotion + distress)
- Temperature scaling calibration
- LOSO cross-validation
- Ablation experiments (audio-only, text-only, sliding window, etc.)
- Full reproducibility support
- Comprehensive documentation

### Datasets
- IEMOCAP support
- MSP-Podcast support (cross-corpus)
- CREMA-D support (cross-corpus)
- MELD support (cross-corpus)

### Metrics
- Emotion: Macro-F1, Accuracy, UAR, ECE
- Distress: MAE, RMSE, Pearson r, Spearman ρ, QWK

### Performance
- Macro-F1: 0.827 ± 0.008
- QWK: 0.834 ± 0.007
- Pearson r: 0.743 ± 0.009
- ECE: 0.027 ± 0.003