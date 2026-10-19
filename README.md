# Reference-Free Hygroscopic Calibration of Low-Cost IoT Networks for Forecasting Indoor Particulate Matter Exposure

**Authors:** Cristobal Chumaceiro Rangel, Andres Aharhel Mercado-Velazquez, Ponciano Jorge Escamilla-Ambrosio, and Stefan Poslad

---

This repository contains the code and reproduction pipeline for the study. Below is an overview of the directory structure and instructions for downloading the raw dataset and executing the notebooks.

## Directory Structure

### `/data/`
This directory stores all datasets generated throughout the sequential pipeline (initially empty except for the external meteorological file `01_raw/exo_filter/EGLC.csv`):
- `01_raw/`: Raw sensor node (`node_data/`), reference station (`reference_data/`), and meteorological (`exo_filter/EGLC.csv`) files.
- `02_interim/`: Synchronised and quality-controlled 1-minute and 15-minute master datasets.
- `03_calibration/`: Wind-filtered training pools, train/validation splits, and tuned hyperparameter configurations for calibration.
- `04_calibrated_master/`: Final hygroscopically calibrated 1-minute and 15-minute master datasets.
- `05_forecasting/`: Chronological train/validation/test splits and tuned hyperparameter configurations for indoor forecasting.
- `06_outputs/`: Generated evaluation tables and figures.

### `/notebooks/`
This directory contains the six Jupyter notebooks used for data processing, calibration, and forecasting, designed to be executed in sequential order:
1. `phase_0_data_preparation.ipynb`: Quality control, spike filtering, resampling, and temporal synchronisation.
2. `phase_1.1_data_exploration_and_training_pool.ipynb`: Exploratory data analysis and wind-isolated training pool construction.
3. `phase_1.2_calibration_modelling_and_tuning.ipynb`: Köhler feature engineering, physical parameter derivation, and Random Forest hyperparameter tuning.
4. `phase_1.3_calibration_production.ipynb`: Fleet-wide calibration execution, regional scaling, and baseline evaluation.
5. `phase_2.1_forecasting_exploration.ipynb`: Feature selection, lookback window analysis, and walk-forward hyperparameter tuning for XGBoost and LSTM models.
6. `phase_2.2_production.ipynb`: Holdout test evaluation and outdoor baseline ablation study.

---

## Reproduction Guide

### 1. Environment & Prerequisites
- **Python Version:** `3.13.7` (specified in `.python-version`)
- **Git LFS:** Required by `prepare_data.py` to pull the raw sensor CSVs from the upstream data repository (`git lfs install`).

Install the pinned Python dependencies:
```bash
pip install -r requirements.txt
```

### 2. Download and Filter Raw Data
Run the data preparation script to clone the upstream QMUL Air Quality Monitoring System (AQMS) dataset ([`AndresMercad0/qm-airquality-network-data`](https://github.com/AndresMercad0/qm-airquality-network-data) at release `v1.0.1`), pull the required files (`node_1`, `node_2`, `node_3`, `node_4`, `node_6`, `node_7`, and `node_TH2_MER`) via Git LFS, and filter them to the study window (`2025-04-16` to `2026-06-10` inclusive):
```bash
python prepare_data.py
```

### 3. Execute the Notebook Pipeline
Run all six notebooks sequentially from start to finish:
```bash
python run_notebooks.py
```

> **Note on Reproducibility & Determinism:**  
> The first part of the pipeline covering data preparation and hygroscopic calibration (`phase_0` through `phase_1.3`) is fully deterministic. When the forecasting pipeline begins (`phase_2.1_forecasting_exploration.ipynb`), the randomised search for hyperparameters and stochastic neural network training mean that future runs of the search may not always yield identical hyperparameter selections or metrics. However, the exact hyperparameter configurations reported in the paper are detailed in the supplementary material and can be used directly in `phase_2.2_production.ipynb` to guarantee consistent results.

---

## Data Attribution

The sensor data used in this study are a subset of the QM Air Quality Network Data dataset (release v1.0.1), openly available under a CC BY 4.0 licence at https://github.com/AndresMercad0/qm-airquality-network-data and archived on Zenodo at https://zenodo.org/records/23482843. This study uses the temperature, relative humidity, PM2.5 and PM10 records of Nodes 1, 2, 3, 4, 6, and 7 and the PM2.5 records of the reference station TH2, from 16 April 2025 to 10 June 2026:

> A. A. Mercado-Velazquez, S. Poslad, and P. J. Escamilla-Ambrosio, “QM Air Quality Network Data: 14 months of raw multi-tier air-quality measurements from a low-cost IoT network in London,” Oct. 2026. [Online]. Available: https://doi.org/10.5281/zenodo.23482843

Government reference data from station TH2 (Mile End Road) was obtained from the Environmental Research Group of Imperial College London, using data from the London Air Quality Network. This information is licensed under the terms of the Open Government Licence v2.0:

> Imperial College London, Environmental Research Group, “Air quality networks,” 2026. [Online]. Available: https://www.imperial.ac.uk/medicine/departments/school-public-health/environmental-research-group/research/measurement/air-quality-networks/
>
> Imperial College London, Environmental Research Group, “Environmental Research Group Application Programming Interface (ERG API), v1.3,” 2026. [Online]. Available: https://api.erg.ic.ac.uk/AirQuality/Information/Documentation/pdf

Meteorological weather observations (wind speed and direction) from London City Airport (EGLC) are managed by the UK Met Office and sourced via the Iowa Environmental Mesonet’s automated data archive:

> D. Herzmann, “IEM :: Site Info: EGLC London City,” 2026. [Online]. Available: https://mesonet.agron.iastate.edu/sites/site.php?station=EGLC&network=GB__ASOS
