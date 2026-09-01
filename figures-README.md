# Figures Directory

This directory contains figures from the paper "DERS-X."

## List of Figures

### Figure 1: Modality Comparison
**File:** `figure_1.png`
**Description:** Utterance-level Macro-F1 and dialog-level QWK for acoustic-only, linguistic-only, and multimodal DERS-X variants under the IEMOCAP proxy-distress setting. Multimodal fusion outperforms both unimodal baselines.
- Acoustic Only: Macro-F1 = 0.72, Dialog QWK = 0.78
- Linguistic Only: Macro-F1 = 0.75, Dialog QWK = 0.71
- Multimodal DERS-X: Macro-F1 = 0.80, Dialog QWK = 0.81


### Figure 2: Cross-Corpus Generalization
**File:** `figure_2.png`
**Description:** Macro-F1 under in-domain and cross-corpus evaluation across IEMOCAP and MSP-Podcast.
- IEMOCAP → IEMOCAP: 0.80
- IEMOCAP → MSP-Podcast: 0.68 (15% drop)
- MSP-Podcast → MSP-Podcast: 0.76
- MSP-Podcast → IEMOCAP: 0.64 (20% drop)


### Figure 3: Degradation Robustness
**File:** `figure_3.png`
**Description:** Impact of additive pink noise on model performance, showing Macro-F1 across SNR levels.
- Clean: 0.738
- 20 dB: 0.729
- 15 dB: 0.704
- 10 dB: 0.661
- 5 dB: 0.588
- 0 dB: 0.555


### Figure 4: Attention Shift
**File:** `figure_4.png`
**Description:** Cross-modal attention shift from audio toward text under acoustic degradation.
- Clean condition: audio share = 54.7 ± 3.2%
- 10dB SNR: audio share = 34.9 ± 4.1%
