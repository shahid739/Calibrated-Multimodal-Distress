# DERS-X Experimental Setup (paper-aligned)

## Evaluation unit

The primary IEMOCAP analysis is **10-fold leave-one-speaker-out (LOSO)**. One individual speaker is held out in each fold. IEMOCAP has 10 speakers arranged in five dyadic sessions, but the manuscript's evaluation unit is the **speaker**, not the session.

The held-out speaker contributes no data to target construction, parameter learning, validation/early stopping, calibration, or hyperparameter selection. Development partitions are dialog-disjoint.

## Analytic samples

- IEMOCAP: 5,479 utterances after the manuscript preprocessing/selection procedure.
- MSP-Podcast: 24,500 retained utterances after the agreement filter (SD < 0.3 on dimensional ratings).

Because the manuscript does not publish the ten individual held-out-speaker result rows, repository artifacts must not invent them.

## Preprocessing

- Audio: mono, 16 kHz.
- Text: lowercased and normalized; maximum 128 WordPiece tokens.
- Empty/near-empty normalized transcripts: fallback token sequence.
- Target statistics and quartile thresholds: fitted on the training partition only within each LOSO fold.

## Model

### Acoustic branch

- Wav2Vec 2.0 Base.
- Learned scalar mixture across 12 Transformer states.
- Projection to 256 dimensions.
- Attentive statistics pooling.

### Text branch

- DistilBERT-base-uncased.
- Projection to 256 dimensions.
- Token sequence participates in cross-modal interaction.

### Fusion

- Four-head bidirectional cross-modal attention.
- Residual connections / normalization as described in the manuscript.
- Fused representation feeds the regression and auxiliary emotion heads.

### Context variant

The manuscript reports a **two-layer Transformer** over utterance representations for the full-context variant. The current public notebook must be checked against this description before claiming paper-exact reproduction; see `NOTEBOOK_ALIGNMENT_REQUIRED.md`.

## Objectives and optimization

- Regression objective: continuous proxy-distress.
- Auxiliary task: nine-class emotion recognition.
- `lambda_emo = 1.0`
- `lambda_reg = 0.5`
- AdamW.
- Encoder LR: `1e-5`.
- Newly initialized layers LR: `1e-4`.
- Warmup: first 10% of optimization steps.
- Weight decay: 0.01.
- Gradient clipping: norm 1.0.
- Effective batch size: 8.
- Dropout: 0.2.
- Epoch budget: up to 20.
- Early stopping: patience 3.
- Seeds: 13, 29, 47.

## Calibration

### Auxiliary emotion
Temperature scaling is fitted only on the calibration partition. Reported ECE: 0.084 -> 0.031.

### Binned proxy-distress
The manuscript describes variance-aware regression uncertainty followed by post-hoc variance recalibration on the calibration partition. Reported ECE: 0.072 -> 0.041.

These are distinct outputs and procedures.

## Robustness and degradation

The manuscript reports:

- MUSAN additive noise at 20, 15, 10, and 5 dB SNR;
- AMR-NB compression at 12.2 kbps;
- 10% VoIP packet loss with mean burst length 3 packets;
- transcript WER corruption at 10%, 20%, 30%;
- substitution/deletion/insertion proportions 60%/20%/20% using a Wav2Vec 2.0 ASR-derived phoneme-confusion process;
- combined 15 dB + 15% WER, 10 dB + 25% WER, and 5 dB + 35% WER conditions;
- five realizations per condition with seeds 13, 29, 47, 101, and 202.

Paper-exact code must require the paper-specified noise/corruption mechanisms instead of silently substituting approximations.

## Reported hardware

The manuscript reports:

- NVIDIA RTX 4090 GPU;
- Intel Xeon Gold 6230 CPU;
- 32 GB RAM;
- CUDA 11.8;
- cuDNN 8.7.0.

`environment.yml` is a recommended reconstruction of the software environment. For an archival rerun, also preserve the automatically generated environment report from the actual execution host.
