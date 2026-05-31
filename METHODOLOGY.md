# Methodology

## Objective

This project maps drought-risk conditions across the MENA region using monthly satellite and climate data.

The workflow converts Earth Engine image collections into a grid-cell table, derives drought-related features, assigns an NDVI-anomaly drought class, and trains a baseline classifier using hydroclimate and spatial context variables.

## Data

The workflow uses:

- MODIS MOD13A3 NDVI for vegetation condition
- CHIRPS daily rainfall aggregated to monthly totals
- MODIS MOD11A2 land surface temperature for heat stress

The notebook analysis period is `2018-01-01` to `2024-12-31`.

Earth Engine date filters treat the end date as exclusive, so the extraction window extends one day beyond the final analysis day. This keeps `2024-12-31` inside the source-data pull while the reported analysis period remains unchanged.

## Spatial Unit

The study area is represented by a regular grid over a broad MENA bounding box.

Each monthly image is reduced over the grid, producing one row per cell per month. The table includes cell metadata, date, NDVI, rainfall, land surface temperature, and cell-center coordinates.

## Feature Engineering

The feature workflow creates:

- calendar-month climatologies by grid cell
- NDVI anomaly
- rainfall anomaly
- rolling 3-month summaries for NDVI anomaly, rainfall, and temperature
- rolling 3-month anomaly summaries for rainfall and land-surface temperature
- a rolling 6-month NDVI-anomaly summary
- drought class labels from NDVI anomaly thresholds

The drought label is a proxy label derived from vegetation stress, not an external observed drought-event inventory.

The reusable feature workflow can build climatologies from a fixed reference period through `climatology_reference_end_date`. This is recommended for evaluation runs so later test months do not influence the anomaly baseline.

## Modeling

The baseline model is a Random Forest classifier evaluated on later months from `2023-01-01` onward.

The model feature set excludes NDVI and NDVI-anomaly fields used to construct the label. It uses rainfall, rainfall anomaly, rainfall rolling summaries, temperature, temperature anomaly summaries, month, latitude, and longitude.

The reusable modeling helpers also include a spatial cell holdout split for checking whether a model generalizes to unseen grid cells, not only later months from known cells.

Prediction-confidence helpers can export predicted class probability, probability margin, entropy, and a high/medium/low confidence label for map-ready tables.

The first version does not mask MODIS quality-assurance bands. That keeps the workflow compact, but a stricter production version should add dataset-specific quality filtering before aggregation.

The reusable Earth Engine helper `mask_mod13a3_detailed_qa` is available for this stricter version. It masks MODIS vegetation-index pixels using the `DetailedQA` band before NDVI aggregation.

## Composite And Validation Enhancements

The project now includes reusable helpers for a composite drought score. The composite score combines available vegetation, rainfall, heat, soil-moisture, and evapotranspiration-deficit evidence after converting each component to a stress score between `0` and `1`.

The project also includes crop-season weighting helpers. These allow drought severity to be weighted more strongly during active growing months.

Independent validation helpers can classify SPEI values into drought classes and summarize agreement between model or composite classes and an external drought reference.

## Outputs

The notebook exports:

- a confusion matrix
- Random Forest feature importance
- annual drought-severity share
- NDVI-anomaly versus rainfall-anomaly scatter plot
- a latest-month drought prediction table
- an interactive Folium drought map

Generated artifacts are written under `outputs/`.
