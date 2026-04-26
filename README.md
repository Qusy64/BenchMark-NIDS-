# Deep Learning NIDS Reproducibility Experiments

This repository contains Kaggle-ready source notebooks for evaluating deep learning-based Network Intrusion Detection Systems (NIDS) on CICIDS-2017 and CSE-CIC-IDS-2018.

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

## Running on Kaggle

Open a notebook on Kaggle and run all cells. Each notebook creates:

- `/kaggle/working/data`
- `/kaggle/working/results`

Datasets are not stored in this repository. The notebooks install `kagglehub`, download the dataset from Kaggle, recursively copy downloaded files into `/kaggle/working/data`, and load CSV files from `/kaggle/working/data`.

Dataset sources:

- CICIDS-2017 notebooks: `bertvankeulen/cicids-2017`
- CSE-CIC-IDS-2018 notebooks: `solarmainframe/ids-intrusion-csv`

Results are saved under `/kaggle/working/results`. After you save a Kaggle notebook version, download results from the Kaggle Output tab or with:

```bash
kaggle kernels output <username>/<kernel-name> -p ./output
```

If Kaggle authentication is required in your Kaggle notebook, configure Kaggle credentials before running the kagglehub download cell.

## Reproducibility Protocol

Experiments use the training seeds and weight initialization tuples from “Randomness Unmasked: Towards Reproducible and Fair Evaluation of Shift-Aware Deep Learning NIDS”.

Training seeds:

```python
[57, 305, 5, 9667, 405]
```

Weight initialization tuples:

```python
W1 = [1004, 77, 259, 35]
W2 = [8, 358, 200, 35]
W3 = [487, 22, 900, 7]
```

Every model runs `5 training seeds x 3 weight initialization tuples = 15 runs`.

## Results

Each notebook saves generated CSV result files under:

- `/kaggle/working/results/*.csv`

Interpret model performance using aggregate statistics: mean, min, max, and standard deviation. Do not report or compare models using only a single run.
