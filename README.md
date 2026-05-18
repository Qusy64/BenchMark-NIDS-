# Deep Learning NIDS Reproducibility Experiments

This repository contains Kaggle-ready notebooks for evaluating reproducibility and temporal robustness of deep learning-based Network Intrusion Detection Systems (NIDS) on the CICIDS-2017 dataset.

The current experiments compare standard fixed-threshold inference with an adaptive threshold estimation method based on Extreme Value Theory (EVT).

The project focuses on:
- reproducibility analysis
- variance across random seeds
- temporal distribution shift
- binary intrusion detection on CICIDS-2017
- adaptive EVT threshold estimation under shifted traffic

---

# Research Scope

This study intentionally uses a compact experimental scope so the reproducibility analysis remains interpretable.

## Dataset

Only one dataset is used:

- `CICIDS-2017`

Reason:
- widely used in NIDS research
- many published baselines are available
- naturally supports day-based temporal shift evaluation

Datasets are not stored in this repository.

---

# Task Definition

The notebooks evaluate binary intrusion detection:

```text
Benign -> 0
Attack -> 1
```

This makes the following metrics meaningful for a security setting:
- Recall: attack detection rate
- False Positive Rate (FPR): benign traffic incorrectly flagged as attack
- Precision
- F1-score
- ROC-AUC

---

# Temporal Shift Scenario

Main evaluation scenario:

```text
Train       : Day 1-2
Calibration : 10% labeled samples from the first shifted day
Test        : remaining samples from Day 3-5
```

This simulates realistic temporal distribution shift in network traffic.

The calibration split is used only for adaptive threshold estimation. The final evaluation is performed on the remaining shifted test samples.

---

# Models

The repository evaluates two baseline architectures:

1. `MLP baseline`
2. `1D CNN baseline`

## Motivation

- MLP provides a simple fully-connected baseline.
- 1D CNN provides a lightweight feature-extraction architecture for tabular traffic features.

This enables comparison between:
- shallow dense architectures
- lightweight convolutional architectures
- PyTorch and TensorFlow/Keras implementations

---

# Frameworks

The current notebooks are split by framework and model:

```text
notebooks/split/
├── CICIDS2017_PyTorch_MLP.ipynb
├── CICIDS2017_PyTorch_CNN.ipynb
├── CICIDS2017_TensorFlow_MLP.ipynb
└── CICIDS2017_TensorFlow_CNN.ipynb
```

PyTorch and TensorFlow/Keras now follow the same high-level protocol:
- CICIDS-2017 temporal split
- binary NIDS labels
- fixed threshold baseline
- EVT adaptive threshold comparison
- repeated runs across seeds and weight initialization tuples

---

# Threshold Methods

Each notebook compares two threshold strategies.

## 1. Fixed Threshold

The baseline decision threshold is:

```python
0.5
```

This is the standard fixed-threshold inference rule.

## 2. EVT Adaptive Threshold

The improved method uses adaptive EVT-based threshold estimation inspired by:

> Adaptive Threshold Estimation via Extreme Value Theory

The implementation:
1. Sorts anomaly scores from the validation-shift set.
2. Selects the top 10% scores as the tail region.
3. Defines a high threshold `u`.
4. Fits a Generalized Pareto Distribution (GPD) to tail excesses with:

```python
scipy.stats.genpareto.fit(..., floc=0)
```

5. Iteratively removes the largest tail samples as possible intrusion contamination.
6. Re-fits the GPD after each removal.
7. Chooses the pruning level that minimizes the Kolmogorov-Smirnov statistic.
8. Computes the final EVT threshold using the target false alarm probability:

```text
alpha0 = 0.05
```

The EVT strategy is reported as:

```text
evt_adaptive_threshold
```

The fixed strategy is reported as:

```text
default_0.5
```

---

# Reproducibility Protocol

Experiments follow a variance-aware evaluation protocol inspired by:

> Randomness Unmasked: Towards Reproducible and Fair Evaluation of Shift-Aware Deep Learning NIDS

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

Each threshold strategy runs:

```text
10 training seeds x 3 weight initialization tuples = 30 runs
```

Each notebook evaluates:

```text
30 fixed-threshold runs + 30 EVT-threshold runs = 60 evaluations
```

---

# Running on Kaggle

Open a notebook on Kaggle and attach the CICIDS-2017 dataset using **Add Input**.

The notebooks expect the dataset files to be visible under:

```text
/kaggle/input
```

Each notebook then automatically creates:

```text
/kaggle/working/data
/kaggle/working/results
/kaggle/working/results/plots
```

The notebooks:
1. read attached dataset files from `/kaggle/input`
2. copy Monday-Friday CICIDS-2017 CSV files into `/kaggle/working/data`
3. load CSV files from `/kaggle/working/data`
4. build the temporal train/calibration/test split
5. run fixed-threshold and EVT-threshold experiments
6. save CSV results and diagnostic plots

Dataset source used during development:

- `bertvankeulen/cicids-2017`

Note: Kaggle may block `kagglehub.dataset_download()` in non-interactive runs, so the notebooks use Add Input instead of automatic download.

---

# Output Results

Generated CSV files are saved under:

```text
/kaggle/working/results/*.csv
```

Important output files include:

```text
*_results.csv
*_detailed_results.csv
*_aggregated_results.csv
*_before_after_threshold_comparison.csv
```

Diagnostic plots are saved under:

```text
/kaggle/working/results/plots
```

Plots include:
- anomaly score distribution
- GPD fitting curve
- KS statistic vs removed outliers
- confusion matrices

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

Do not compare models using only a single run.

Recommended reporting format:

```text
F1 = 0.842 +/- 0.031
```

For threshold comparison, use:

```text
*_before_after_threshold_comparison.csv
```

Key delta columns:
- `delta_f1_evt_minus_default`
- `delta_fpr_evt_minus_default`

Interpretation:
- positive `delta_f1_evt_minus_default` means EVT improved mean F1.
- negative `delta_fpr_evt_minus_default` means EVT reduced mean false positives.

---

# Repository Structure

```text
notebooks/
└── split/
    ├── CICIDS2017_PyTorch_MLP.ipynb
    ├── CICIDS2017_PyTorch_CNN.ipynb
    ├── CICIDS2017_TensorFlow_MLP.ipynb
    └── CICIDS2017_TensorFlow_CNN.ipynb
```

## Notebook Description

### `CICIDS2017_PyTorch_MLP.ipynb`

PyTorch MLP baseline with fixed threshold vs EVT adaptive threshold.

### `CICIDS2017_PyTorch_CNN.ipynb`

PyTorch 1D CNN baseline with fixed threshold vs EVT adaptive threshold.

### `CICIDS2017_TensorFlow_MLP.ipynb`

TensorFlow/Keras MLP baseline with fixed threshold vs EVT adaptive threshold.

### `CICIDS2017_TensorFlow_CNN.ipynb`

TensorFlow/Keras 1D CNN baseline with fixed threshold vs EVT adaptive threshold.
