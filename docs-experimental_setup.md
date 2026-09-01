# Experimental Setup

## Datasets

### IEMOCAP

- Primary multimodal benchmark.
- Five sessions, each containing a dyadic interaction pair.
- The archived primary result table is indexed by five held-out session folds (`Ses01`-`Ses05`).
- Raw corpus files are obtained from the official USC distribution and are not redistributed in this repository.

### MSP-Podcast

- Used for cross-corpus/dimensional-affect analyses where reported.
- Raw corpus files are obtained from the official distributor.

### MUSAN

- Used for controlled acoustic degradation/noise experiments where reported.

## Primary Evaluation Protocol

The primary archived IEMOCAP evaluation is **five-fold leave-one-session-out**:

1. Hold out one full session as the test fold.
2. Remove the held-out session from model-development data.
3. Split the remaining development dialogs into training, validation, and calibration partitions without dialog overlap.
4. Fit target statistics using training data only.
5. Fit post-hoc calibration using calibration data only.
6. Evaluate once on the held-out session.

The final canonical notebook must use the same grouping unit as the archived results.

## Model Configuration

The paper-aligned reference implementation uses:

- acoustic encoder: `facebook/wav2vec2-base`;
- text encoder: `distilbert-base-uncased`;
- audio sample rate: 16 kHz;
- maximum text length: 128 wordpieces;
- latent dimension: 256;
- fusion attention heads: 4;
- dropout: 0.2;
- effective batch size: 8 in the paper-aligned profile;
- encoder learning rate: 1e-5;
- new-layer learning rate: 1e-4;
- weight decay: 0.01;
- warmup ratio: 0.10;
- gradient clipping: 1.0; and
- primary seeds: 13, 29, 47.

The executable notebook is the source of truth for the final training configuration.

## Recorded Computational Cost

The canonical result registry currently records:

| Quantity | Recorded value |
|---|---:|
| Trainable parameters | 162.4 million |
| Total parameters | 164.1 million |
| Peak GPU memory | 11.4 GB |
| Total inference latency | 0.60 s per utterance (reported reference value) |
| Real-time factor | 0.05 (reported reference value) |

These values are taken from `paper_results.yaml` and should not be replaced by conflicting estimates in documentation.

## Computing Environment

The notebook automatically records runtime information, including:

- operating system/platform;
- Python version;
- PyTorch version;
- CUDA availability/runtime;
- GPU device name;
- CPU count;
- system RAM; and
- allocated/reserved GPU memory.

Full reruns should retain the generated environment report with the result archive. CUDA-capable NVIDIA hardware is recommended for neural training. Historical development may have used more than one GPU class; the exact device for a specific rerun should be taken from that run's environment report rather than inferred from this document.

## Software Environment

Use `environment.yml` as the authoritative Conda environment definition:

```bash
conda env create -f environment.yml
conda activate dersx_env
```

`requirements.txt` is provided as a pip-compatible convenience list. Avoid maintaining a second conflicting table of package versions in this file.
