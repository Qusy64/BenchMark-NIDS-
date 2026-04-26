# Deep Learning NIDS Reproducibility Experiments

This repository contains Google Colab-ready source notebooks for evaluating deep learning-based Network Intrusion Detection Systems (NIDS) on CICIDS-2017 and CSE-CIC-IDS-2018.

## Notebooks

1. `notebooks/01_CICIDS2017_PyTorch.ipynb` - CICIDS-2017 experiments in PyTorch
2. `notebooks/02_CICIDS2017_TensorFlow.ipynb` - CICIDS-2017 experiments in TensorFlow/Keras
3. `notebooks/03_CSE_CIC_IDS2018_PyTorch.ipynb` - CSE-CIC-IDS-2018 experiments in PyTorch
4. `notebooks/04_CSE_CIC_IDS2018_TensorFlow.ipynb` - CSE-CIC-IDS-2018 experiments in TensorFlow/Keras

Each notebook evaluates:

- MLP baseline
- 1D CNN baseline for tabular features
- Framework-style MLP (`INSOMNIA-style` for CICIDS-2017, `CADE-style` for CSE-CIC-IDS-2018)
- Dataset-specific improved MLP

## Running on Google Colab

Open a notebook in Google Colab and run the cells in order. Each notebook creates:

- `/content/data`
- `/content/results`

Datasets are not stored in this repository. The notebooks install `kagglehub`, download the dataset from Kaggle, recursively copy downloaded files into `/content/data`, and load CSV files from `/content/data`.

Dataset sources:

- CICIDS-2017 notebooks: `bertvankeulen/cicids-2017`
- CSE-CIC-IDS-2018 notebooks: `solarmainframe/ids-intrusion-csv`

If Kaggle authentication is required in your Colab runtime, configure Kaggle credentials before running the kagglehub download cell.

## Reproducibility Protocol

Experiments use the training seeds and weight initialization tuples from “Randomness Unmasked: Towards Reproducible and Fair Evaluation of Shift-Aware Deep Learning NIDS”.

Training seeds:

```python
[57, 305, 5, 9667, 405, 750, 1038, 840, 63, 988]
```

Weight initialization tuples:

```python
W1 = [1004, 77, 259, 35]
W2 = [8, 358, 200, 35]
W3 = [487, 22, 900, 7]
```

Every model runs `10 training seeds x 3 weight initialization tuples = 30 runs`.

## Results

Each notebook saves:

- `/content/results/<notebook_name>_per_run_results.csv`
- `/content/results/<notebook_name>_aggregated_results.csv`

Interpret model performance using aggregate statistics: mean, min, max, and standard deviation. Do not report or compare models using only a single run.
