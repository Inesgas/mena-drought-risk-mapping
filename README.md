# MENA Drought Risk Mapping

This project maps drought-risk conditions across the Middle East and North Africa using Google Earth Engine satellite and climate data.

It is the monitoring companion to:

- [MENA Drought Early Warning](https://github.com/Inesgas/mena-drought-early-warning)

This repository focuses on current drought-risk mapping. The early-warning repository extends the workflow into 1-month and 3-month forecasting.

## Project Question

Can monthly satellite and climate observations be transformed into a clear grid-based drought-risk map for the MENA region?

## Data Sources

The workflow uses:

- MODIS NDVI: `MODIS/061/MOD13A3`
- CHIRPS rainfall: `UCSB-CHG/CHIRPS/DAILY`
- MODIS land surface temperature: `MODIS/061/MOD11A2`
- Google Earth Engine for data access and spatial aggregation

## Workflow

1. Define the MENA study area.
2. Build a regular grid over the region.
3. Extract monthly NDVI, rainfall, and land-surface-temperature values.
4. Convert Earth Engine outputs into a pandas table.
5. Build climatologies, anomalies, rolling summaries, and drought classes.
6. Train a Random Forest baseline using hydroclimate and context variables, then test it on later months.
7. Export figures, tables, and an interactive drought map.

## Main Notebook

Open:

```text
notebooks/drought_risk_mapping_mena_real_data.ipynb
```

This notebook runs the Earth Engine extraction, feature engineering, baseline model, and output export.

## Project Review

A short narrative review of the workflow is available in:

```text
PROJECT_REVIEW.md
```

## Reusable Python Core

The reusable pieces live under:

```text
src/mena_drought_risk_mapping/
```

They cover:

- project configuration
- month generation and output folders
- drought class labels
- feature engineering
- temporal splitting and evaluation helpers

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/project_setup.py
python scripts/environment_check.py
python -m unittest discover -s tests
```

Authenticate Earth Engine before running the notebook extraction cells.

## Outputs

Generated outputs are written under:

- `outputs/figures/`
- `outputs/maps/`
- `outputs/tables/`
- `assets/screenshots/`

Local raw/intermediate data and generated output files are ignored by Git.

## Method Notes

- Drought classes are derived from NDVI anomaly thresholds.
- The baseline model excludes NDVI-derived label-construction fields from predictors.
- Random Forest is used as an interpretable tabular baseline and is evaluated on a later-period test set.
- The current spatial unit is a regular grid, not an administrative or agro-ecological boundary.
- The drought label is a proxy label, not an external observed drought-event inventory.
- The notebook keeps the first extraction compact; larger runs should move the Earth Engine table export out of interactive memory.
