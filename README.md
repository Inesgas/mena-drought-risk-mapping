# Drought Risk Mapping for the MENA Region

This project demonstrates a portfolio-style geospatial machine-learning workflow for drought analysis in the Middle East and North Africa (MENA). The strongest notebook uses real Earth observation data from Google Earth Engine, engineers monthly drought features, trains a baseline Random Forest classifier, and prepares outputs that can be turned into maps, figures, and tables.

## Recommended notebook

Use `drought_risk_mapping_MENA_real_data_portfolio.ipynb` as the primary notebook.

Older draft notebooks have been archived under `archive/notebooks/` to keep the root folder clean:

- `archive/notebooks/drought_risk_mapping_mena_real_data.ipynb.ipynb`: similar real-data variant with output-folder setup
- `archive/notebooks/drought_risk_mapping_MENA_portfolio_prototype.ipynb`: prototype with simulated data
- `archive/notebooks/drought_risk_mapping_MENA.ipynb`: earlier prototype draft

The repository also preserves a legacy `notebooks/` folder from the earlier GitHub history.

## What the project currently does

The real-data workflow is built around:

- MODIS MOD13A3 NDVI
- CHIRPS daily rainfall
- MODIS MOD11A2 land surface temperature
- Google Earth Engine for remote-sensing access and aggregation
- pandas and NumPy for tabular processing
- scikit-learn for baseline classification
- matplotlib and Folium for communication outputs

## Current repository improvements

This repository now includes the standard files and folders the notebooks were implicitly expecting:

- `README.md`
- `requirements.txt`
- `.gitignore`
- `scripts/project_setup.py`
- `scripts/environment_check.py`
- `outputs/`
- `data/`
- `assets/screenshots/`
- `PROJECT_DETAILS.txt`

The main real-data notebook now saves core portfolio assets directly into the standard folders:

- confusion matrix figure
- feature-importance figure
- annual drought-share figure
- NDVI vs rainfall anomaly scatter plot
- latest predictions CSV
- interactive HTML drought map

## Quick start

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment.
3. Install dependencies with `pip install -r requirements.txt`.
4. Run `python scripts/project_setup.py` to create the standard project folders if needed.
5. Run `python scripts/environment_check.py` to check package availability.
6. Start Jupyter and open `drought_risk_mapping_MENA_real_data_portfolio.ipynb`.
7. Authenticate Earth Engine if your environment has not been initialized yet.

## Expected outputs

As you polish the notebook, save final assets into:

- `outputs/figures/` for charts
- `outputs/maps/` for HTML maps
- `outputs/tables/` for CSV exports
- `assets/screenshots/` for recruiter-friendly screenshots

## Key strengths

- Clear end-to-end story from satellite data to drought-risk classification
- Good portfolio positioning for climate, geospatial, and machine-learning roles
- Explainable baseline model and transparent drought labeling logic
- Strong upgrade path toward better boundaries, better labels, and better benchmarking

## Current limitations

- The project is still notebook-first and not yet packaged as a reusable Python pipeline
- There are still archived overlapping notebooks from earlier drafting stages
- The machine-learning validation is a baseline split, not yet a spatial or temporal backtesting design

## Next best upgrades

1. Replace the simple bounding-box grid with administrative or agro-ecological boundaries.
2. Add stronger validation and benchmark Random Forest against XGBoost.
3. Move reusable functions into a small `src/` package when the workflow stabilizes.
4. Rename the main notebook to a shorter final production name if you want a more polished public repo.
