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
- a rolling 6-month NDVI-anomaly summary
- drought class labels from NDVI anomaly thresholds

The drought label is a proxy label derived from vegetation stress, not an external observed drought-event inventory.

## Modeling

The baseline model is a Random Forest classifier evaluated on later months from `2023-01-01` onward.

The model feature set excludes NDVI and NDVI-anomaly fields used to construct the label. It uses rainfall, rainfall anomaly, rainfall rolling summaries, temperature, temperature rolling summaries, month, latitude, and longitude.

The first version does not mask MODIS quality-assurance bands. That keeps the workflow compact, but a stricter production version should add dataset-specific quality filtering before aggregation.

## Outputs

The notebook exports:

- a confusion matrix
- Random Forest feature importance
- annual drought-severity share
- NDVI-anomaly versus rainfall-anomaly scatter plot
- a latest-month drought prediction table
- an interactive Folium drought map

Generated artifacts are written under `outputs/`.
