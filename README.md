# Deep Learning NIDS Reproducibility Experiments

This repository contains Kaggle-ready notebooks for evaluating reproducibility and temporal robustness of deep learning-based Network Intrusion Detection Systems (NIDS) on the CICIDS-2017 dataset.

The project focuses on:
- reproducibility analysis
- variance across random seeds
- temporal distribution shift
- lightweight adaptive threshold calibration

---

# Research Scope

This study intentionally uses a simplified experimental scope to make reproducibility analysis easier and more interpretable.

## Dataset

Only one dataset is used:

- `CICIDS-2017`

Reason:
- widely used in NIDS research
- many published baselines available
- supports temporal shift evaluation naturally

---

# Temporal Shift Scenario

Main evaluation scenario:

```text
Train: Day 1-2
Test : Day 3-5
```

This simulates realistic temporal distribution shift in network traffic.

The goal is to evaluate how model performance changes when traffic behavior evolves over time.

---

# Models

The repository evaluates two baseline architectures:

1. `MLP baseline`
2. `1D CNN baseline`

## Motivation

- MLP provides a simple fully-connected baseline
- CNN provides a more structured architecture for tabular traffic features

This enables comparison between:
- shallow dense architectures
- lightweight feature-extraction architectures

---

# Frameworks

Primary implementation framework:

- `PyTorch`

Additional validation framework:

- `TensorFlow / Keras`

TensorFlow experiments are executed only on a smaller subset as a lightweight implementation consistency check.

---

# Adaptive Threshold Calibration

This repository also includes a simple contribution for improving robustness under temporal shift.

## Idea

Instead of using the default classification threshold:

```python
0.5
```

the decision threshold is calibrated using a small validation-shift set.

Example:

```text
10% labeled samples from Day 3
```

The calibrated threshold is then applied to the entire shifted test set.

## Goal

Measure how threshold adaptation affects:
- F1-score
- False Positive Rate (FPR)
- Recall
- Precision

compared to the default threshold.

---

# Reproducibility Protocol

Experiments follow a variance-aware evaluation protocol inspired by:

> “Randomness Unmasked: Towards Reproducible and Fair Evaluation of Shift-Aware Deep Learning NIDS”

## Training Seeds

```python
[57, 305, 5, 9667, 405, 111, 222, 333, 444, 555]
```

Total:
- 10 training seeds

## Weight Initialization Tuples

```python
W1 = [1004, 77, 259, 35]
W2 = [8, 358, 200, 35]
W3 = [487, 22, 900, 7]
```

Each model runs:

```text
10 training seeds × 3 weight initialization tuples
= 30 runs
```

---

# Running on Kaggle

Open a notebook on Kaggle and run all cells.

Each notebook automatically creates:

```text
/kaggle/working/data
/kaggle/working/results
```

Datasets are not stored in this repository.

The notebooks:
1. install `kagglehub`
2. download the dataset from Kaggle
3. recursively copy files into `/kaggle/working/data`
4. load CSV files from `/kaggle/working/data`

Dataset source:

- `bertvankeulen/cicids-2017`

---

# Output Results

Generated CSV files are saved under:

```text
/kaggle/working/results/*.csv
```

After saving a Kaggle notebook version, outputs can be downloaded from:
- Kaggle Output tab
- Kaggle CLI

Example:

```bash
kaggle kernels output <username>/<kernel-name> -p ./output
```

---

# Result Interpretation

Model performance must be evaluated using aggregate statistics.

Report:
- mean
- standard deviation
- minimum
- maximum

Do NOT compare models using only a single run.

Recommended reporting format:

```text
F1 = 0.842 ± 0.031
```

This provides a fairer evaluation of:
- reproducibility
- training stability
- robustness under temporal shift

---

# Repository Structure

```text
notebooks/
├── 01_CICIDS2017_PyTorch.ipynb
├── 02_CICIDS2017_TensorFlow.ipynb
```

## Notebook Description

### `01_CICIDS2017_PyTorch.ipynb`

Main experiment notebook:
- MLP baseline
- CNN baseline
- temporal shift evaluation
- adaptive threshold calibration
- variance analysis

### `02_CICIDS2017_TensorFlow.ipynb`

Smaller TensorFlow/Keras validation notebook for framework consistency checking.