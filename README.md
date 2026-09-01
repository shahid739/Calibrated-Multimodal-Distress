# DERS-X: A Reproducible Benchmark Protocol for Calibrated Multimodal Proxy-Distress Affect Modeling on Speech Corpora

## Title
**DERS-X:** A Reproducible Benchmark Protocol for Calibrated Multimodal Proxy-Distress Affect Modeling on Speech Corpora

## Description
This repository contains the implementation of **DERS-X (Distress Emotion Recognition System - Extended)**, a reproducible benchmark protocol for calibrated multimodal affect modeling from speech and text. The framework integrates:
- **Wav2Vec 2.0** acoustic representations
- **DistilBERT** transcript representations
- **Bidirectional cross-modal attention** for dynamic feature fusion
- **Joint continuous proxy-distress regression** with auxiliary nine-class emotion recognition
- **Post-hoc temperature scaling** and **variance-aware calibration** for uncertainty quantification

### Key Contributions
1. **Leakage-Controlled Benchmark Protocol** – Fold-specific target construction, strict dialog-level splitting, dedicated calibration partitions, and explicit reporting hierarchy
2. **Reliability-Sensitive Attention Diagnostic** – Systematic analysis showing cross-modal attention shifts from 55% audio/45% text in clean conditions to 35% audio/65% text at 10dB SNR
3. **Systematic Degradation Benchmark** – Controlled acoustic noise, channel distortion, and ASR transcription errors with five perturbation realizations per condition
4. **Calibration Analysis on Primary Output** – Variance-aware calibration for binned proxy-distress output with comparison against temperature scaling

### Empirical Results
Under strict speaker-independent leave-one-speaker-out (LOSO) evaluation on IEMOCAP, DERS-X achieves:
- **Fold-averaged Macro-F1:** 0.738 ± 0.014 (four-level proxy-distress)
- **Pooled held-out Macro-F1:** 0.814
- **Pearson correlation:** 0.712 ± 0.006 (continuous proxy-distress regression)
- **Dialog-level QWK:** 0.808 ± 0.012
- **Auxiliary Emotion Macro-F1:** 0.700 ± 0.028
- **ECE reduction:** 0.084 → 0.031 ± 0.001 (temperature scaling)

> **Note:** The fold-averaged Macro-F1 of 0.738 ± 0.014 is calculated from the five held-out session values: 0.722, 0.735, 0.730, 0.748, and 0.755. The pooled held-out Macro-F1 is 0.814.

## Dataset Information

| Dataset | Description | Access / URL |
|---------|-------------|--------------|
| **IEMOCAP** | Interactive Emotional Dyadic Motion Capture Database – acted and improvised dyadic interactions with categorical emotion labels and dimensional affect ratings | [https://sail.usc.edu/iemocap/](https://sail.usc.edu/iemocap/) |
| **MSP-Podcast** | Naturalistic podcast speech with continuous arousal-valence annotations | [https://lab-msp.com/MSP/MSP-Conversation.html](https://lab-msp.com/MSP/MSP-Conversation.html) |
| **MUSAN** | Music, Speech, and Noise Corpus (used for degradation experiments) | [https://www.openslr.org/17/](https://www.openslr.org/17/) |

### Dataset Statistics

| Dataset | Utterances | Sessions | Speakers | Labels |
|---------|------------|----------|----------|--------|
| IEMOCAP | 10,039 | 5 | 10 | 9 emotion classes + activation |
| MSP-Podcast | 24,500 | N/A | Multiple | Arousal-valence (dimensional) |

---

## Reproducing Results

### Prerequisites

1. **Install dependencies:**
   ```bash
   conda env create -f environment.yml
   conda activate dersx