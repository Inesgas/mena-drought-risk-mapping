# Geospatial drought risk mapping for the MENA region using real satellite data and machine learning

## Overview
This project builds a clean GeoAI workflow that turns satellite observations into drought-risk predictions and interactive spatial outputs for the MENA region.

The notebook uses real Earth observation data from Google Earth Engine, engineers monthly geospatial features, trains a baseline Random Forest classifier, and produces a stakeholder-friendly interactive drought map.

## Why this project matters
Drought monitoring often sits between two worlds: remote sensing and decision support. This project connects them in one reproducible workflow.

It demonstrates how to:
- extract and aggregate satellite data,
- engineer drought-relevant features,
- train an interpretable machine-learning baseline,
- and communicate the results spatially.

## Main outputs
- Exploratory charts showing NDVI, rainfall, temperature, and drought patterns
- Classification results, confusion matrix, and feature importance
- Interactive drought map for the latest available month
- Exported CSV table of latest predictions
- Reusable portfolio assets for GitHub

## Data sources
- **MODIS MOD13A3** for NDVI
- **CHIRPS Daily** for rainfall
- **MODIS MOD11A2** for land surface temperature

All data are accessed through **Google Earth Engine**.

## Tools
- Python
- Google Earth Engine
- geemap
- pandas
- NumPy
- scikit-learn
- matplotlib
- Folium

## Repository structure
```text
mena-drought-risk-mapping/
│
├── README.md
├── requirements.txt
├── .gitignore
├── notebooks/
│   └── drought_risk_mapping_MENA_real_data_portfolio.ipynb
├── outputs/
│   ├── figures/
│   ├── maps/
│   └── tables/
├── assets/
│   └── screenshots/
└── data/
    └── README.md
```

## Method summary
1. Define the MENA study area and build a grid.
2. Pull NDVI, rainfall, and land surface temperature from Earth Engine.
3. Aggregate monthly values to grid cells.
4. Engineer anomalies and rolling features.
5. Create transparent drought classes from NDVI anomaly.
6. Train a Random Forest baseline.
7. Visualize the latest drought predictions on an interactive map.

## Example deliverables to show recruiters
- A screenshot of the final interactive drought map in `assets/screenshots/`
- The exported HTML map in `outputs/maps/`
- One confusion matrix figure and one feature importance figure in `outputs/figures/`
- A short project summary in your README header

## How to run
1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies from `requirements.txt`.
4. Authenticate Google Earth Engine if needed.
5. Run the notebook in `notebooks/`.

## Notes
- This project is a strong portfolio prototype, not yet an operational production system.
- The current version uses a broad spatial grid over MENA. A stronger future version would use real administrative or agro-ecological boundaries.
- The best next upgrade is comparing Random Forest with XGBoost before trying more complex models.

## Best portfolio description
Built an end-to-end drought risk mapping workflow for the MENA region using real MODIS, CHIRPS, and land-surface-temperature data from Google Earth Engine, engineered monthly geospatial features, trained a Random Forest classifier, and produced stakeholder-friendly interactive maps and exportable portfolio assets.
