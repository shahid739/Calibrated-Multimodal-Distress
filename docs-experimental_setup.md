# Experimental Setup

## Datasets

### IEMOCAP
- 10 speakers (5 male, 5 female)
- 5 sessions
- 5,479 utterances after preprocessing
- 9 emotion classes mapped to 4 categories
- Continuous activation ratings (EmoAct 1-5)

### MSP-Podcast
- 24,500 utterances (after SD < 0.3 agreement filter)
- Naturalistic podcast speech
- Continuous arousal-valence annotations

### CREMA-D & MELD
- Used for cross-corpus validation
- Mapped to shared distress proxy

## Evaluation Protocol

### Leave-One-Speaker-Out (LOSO)
- 10 folds (one per speaker)
- 80% training, 10% validation, 10% calibration
- Stratified splits

### Metrics

| Task | Metrics |
|------|---------|
| Emotion Classification | Macro-F1, Accuracy, UAR, ECE |
| Distress Regression | MAE, RMSE, Pearson r, Spearman ρ |
| Ordinal Distress | QWK, Macro-F1, UAR |

### Baselines

| Model | Description |
|-------|-------------|
| Audio Only | Wav2Vec 2.0 features only |
| Text Only | DistilBERT features only |
| Early Fusion | Feature concatenation |
| Late Fusion | Prediction averaging |
| MulT | Multimodal Transformer [Tsai et al.] |
| TACFN | Adaptive Cross-modal Fusion [Liu et al.] |
| Mamba-SER | State Space Models [Phukan et al.] |

## Implementation Details

- Hardware: NVIDIA RTX 4090 / H100 SXM5
- Training Time: ~8.2 hours per fold (H100)
- Parameters: 1.07B total
- Memory: 11.2 GB GPU memory