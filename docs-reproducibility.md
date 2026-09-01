# Reproducibility Guide

## Software Versions

| Package | Version |
|---------|---------|
| Python | 3.9.18 |
| PyTorch | 2.0.1 |
| torchaudio | 2.0.2 |
| transformers | 4.31.0 |
| datasets | 2.12.0 |
| scikit-learn | 1.3.0 |
| numpy | 1.24.3 |
| pandas | 2.0.3 |
| CUDA | 11.8 |
| cuDNN | 8.7.0 |

## Random Seeds

Fixed random seeds for reproducibility:
- 13, 29, 47 (primary)
- 101, 202 (optional)

## Data Splits

- LOSO: Leave-One-Speaker-Out (10 speakers)
- Remaining: 80% train, 10% validation, 10% calibration
- Split at dialog level to prevent leakage

## Preprocessing

### Audio
- Resample to 16 kHz
- Mono channel
- Max length: 10 seconds (truncate/pad)

### Text
- Lowercase
- Normalize filled pauses
- Max length: 128 wordpiece tokens

## Getting Results

```bash
# Run full experiment
