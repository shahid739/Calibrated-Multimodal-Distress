# Note for Reviewers: Results 

## Where Results Come From


### Source of Each Number:

| Metric | Paper Value | Code Location | How Generated |
|--------|-------------|---------------|---------------|
| Fold-averaged Macro-F1 | 0.755 ± 0.030 | `src/metrics.py` → `eval_emotion_metrics()` | Run on 5 LOSO folds, average across folds |
| Pooled held-out Macro-F1 | 0.814 | `src/metrics.py` → `eval_emotion_metrics()` | Run on concatenated predictions |
| Pearson r | 0.712 ± 0.006 | `src/metrics.py` → `eval_distress_metrics()` | Calculated on held-out fold predictions |
| Dialog QWK | 0.809 ± 0.003 | `src/metrics.py` → `quadratic_weighted_kappa()` | Aggregated per dialog |
| ECE | 0.031 ± 0.001 | `src/metrics.py` → `expected_calibration_error()` | After temperature scaling on validation set |

## Verify for Yourself

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shahid739/Calibrated-Multimodal-Distress.git
   cd DERS-X-Benchmark