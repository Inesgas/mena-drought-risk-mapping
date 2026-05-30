# Novelty And Enhancement Brief

Reviewed on 2026-05-30.

## Current Position

The project already has a useful baseline: it turns Earth Engine observations into grid-month features, assigns transparent NDVI-anomaly drought classes, trains a leakage-aware tabular baseline that excludes NDVI label-construction fields, and exports map-ready outputs.

The current novelty is best framed as a reproducible MENA regional prototype that is being extended toward a validated, multi-evidence drought-risk product. The reusable code now includes composite drought scoring, crop-season weighting, spatial holdout testing, MODIS quality-mask helpers, independent validation helpers, and prediction-confidence outputs.

## Best Novelty Angles

1. **Composite drought evidence for MENA**
   - Operational MENA drought work has used convergence of evidence across precipitation, vegetation, soil moisture, and evapotranspiration anomalies. This project can become more novel by comparing the current NDVI-label baseline with a composite drought indicator inspired by that approach.
   - Reference: [NASA NTRS, Composite Drought Indicator for operational MENA monitoring](https://ntrs.nasa.gov/citations/20230006708).

2. **Crop-season-aware drought severity**
   - A month with vegetation stress should not count the same everywhere. Weight severity by active growing season, crop type, or crop calendar where agricultural risk is the main question.
   - Candidate sources: [FAO Crop Calendar](https://www.fao.org/sustainable-development-goals-helpdesk/transform/article-detail/crop-calendar/en), [ESA WorldCereal global maps](https://esa-worldcereal.org/en/products/global-maps).

3. **Water productivity and evapotranspiration context**
   - MENA drought risk is tightly coupled to water productivity and irrigation. FAO WaPOR adds evapotranspiration, reference evapotranspiration, relative soil moisture, biomass, phenology, and water productivity layers over Africa and the Near East.
   - Reference: [FAO WaPOR data](https://www.fao.org/in-action/remote-sensing-for-water-productivity/wapor-data/en).

4. **Independent drought-index validation**
   - The current label is derived from NDVI anomaly, so validation should include independent drought indices. SPEI is useful because it combines precipitation and atmospheric demand across multiple accumulation windows.
   - Reference: [Global SPEI database](https://spei.csic.es/database.html).

5. **Generalization testing, not just later-month testing**
   - A temporal split tests future months for known grid cells. A spatial holdout tests whether the model generalizes to unseen grid cells. Both views are useful, and disagreement between them can reveal spatial overfitting.

6. **Uncertainty and confidence layers**
   - A practical drought map should show both predicted class and confidence. Random Forest class probabilities can produce a low-confidence mask, entropy score, or "needs review" class for ambiguous grid cells.

## Data Enhancements

| Theme | Candidate Addition | Why It Helps |
|---|---|---|
| Vegetation quality | MOD13A3 `DetailedQA` mask | Reduces cloud/aerosol/low-quality VI artifacts before NDVI anomaly labels are created. |
| Meteorological drought | CHIRPS SPI or SPEI comparison | Adds an independent precipitation/climate drought lens. |
| Heat and atmospheric demand | ERA5-Land temperature, PET/ET-related bands | Moves beyond surface temperature toward evaporative stress. Note ERA5-Land has documented evapotranspiration-band issues that must be handled carefully. |
| Soil moisture | SMAP or modeled root-zone soil moisture | Adds direct water-availability signal, especially useful before vegetation response appears. |
| Agriculture focus | Crop calendar, cropland mask, irrigation mask | Separates agricultural drought from natural dryland vegetation dynamics. |
| Risk framing | Exposure/vulnerability layers | Turns hazard mapping into risk mapping if population, cropland, irrigation, or food-security exposure is added. |

References for candidate sources: [MOD13A3 in Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD13A3), [CHIRPS Daily in Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/UCSB-CHG_CHIRPS_DAILY), [ERA5-Land Monthly Aggregated in Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_MONTHLY_AGGR), [SMAP on Drought.gov](https://www.drought.gov/data-maps-tools/soil-moisture-active-passive-smap).

## Method Enhancements

1. **Use a fixed climatology reference window**
   - Build climatologies from training or historical reference months only, then apply them to later evaluation months.
   - This project already supports `climatology_reference_end_date` in `add_drought_features`.

2. **Add anomaly-window predictors**
   - Raw 3-month rainfall and temperature summaries are useful, but drought interpretation usually needs departures from normal. The reusable core now includes `rainfall_anom_3m` and `lst_c_anom_3m`.

3. **Add spatial holdout evaluation**
   - Evaluate whether model performance survives when entire grid cells are held out. The reusable core now includes `cell_holdout_split`.

4. **Report class probability and uncertainty**
   - Export `predicted_probability`, `prediction_margin`, or entropy with the latest map table.

5. **Benchmark with constrained models**
   - Compare Random Forest with calibrated logistic regression, gradient boosting, and an XGBoost/LightGBM-style model if those dependencies are acceptable. Keep the Random Forest as the explainable baseline.

6. **Add external validation views**
   - Compare predicted class with SPEI/SPI, WaPOR relative soil moisture, or national drought bulletins where available.

## Practical Roadmap

| Priority | Enhancement | Effort | Value |
|---|---:|---:|---:|
| P0 | Apply MODIS QA masking before NDVI labels | Medium | High |
| P0 | Wire notebook to reusable `src/` helpers | Low | High |
| P0 | Use training/reference-period climatology in notebook | Low | High |
| P1 | Export prediction confidence and uncertainty | Low | Medium |
| P1 | Run spatial holdout and temporal holdout model reports | Low | High |
| P1 | Add SPEI/SPI comparison table or map layer | Medium | High |
| P2 | Add WaPOR ET, biomass, phenology, and relative soil moisture | Medium | High |
| P2 | Add crop calendar or crop-mask weighting | Medium | High |
| P3 | Run and report the composite drought indicator baseline | Medium | Very high |
| P3 | Add impact/exposure layers for risk mapping | High | Very high |

## Implementation Status

| Enhancement | Status |
|---|---|
| MODIS quality-mask helper | Implemented in reusable Earth Engine helper code. |
| Fixed-reference climatology | Implemented in feature workflow. |
| Rolling anomaly predictors | Implemented in feature workflow. |
| Spatial holdout split | Implemented in modeling workflow. |
| Prediction confidence | Implemented in modeling workflow. |
| SPEI validation helper | Implemented in validation workflow. |
| Crop-season weighting | Implemented in crop-calendar workflow. |
| Composite drought indicator | Implemented in composite workflow. |
| Final regenerated maps and reports | Requires Earth Engine authentication or processed input data. |

## Recommended Novelty Statement

This project can be positioned as a reproducible MENA drought-risk mapping prototype that integrates open Earth observation data, leakage-aware anomaly engineering, spatial-temporal validation, and map-ready outputs. Its clearest novelty path is to evolve from NDVI-proxy drought classes into a crop-season-aware, multi-evidence drought indicator that combines vegetation stress, rainfall deficits, heat stress, evapotranspiration or soil moisture, and uncertainty.
