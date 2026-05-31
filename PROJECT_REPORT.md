# Project Report

## Project Title

MENA Drought Risk Mapping

## Project Purpose

I built this project to map drought-risk conditions across the Middle East and North Africa using real satellite and climate data.

The goal was not only to train a model, but to create a full workflow that starts with Earth observation data and ends with outputs that can be inspected as maps, figures, and tables.

## Main Question

Can monthly satellite and climate observations be converted into a clear grid-based drought-risk map for the MENA region?

## What I Did And Why

| Step | What I Did | Why I Did It |
|---|---|---|
| Defined the study region | I used a broad MENA bounding box as the study area. | This gave the project a clear regional scope and kept the first version reproducible. |
| Built a regular grid | I divided the study area into grid cells. | A grid gives every location a stable spatial unit, which is needed before satellite data can become a modeling table. |
| Pulled vegetation data | I used MODIS NDVI from Google Earth Engine. | NDVI measures vegetation condition, which is one of the clearest signals of agricultural and ecological drought stress. |
| Pulled rainfall data | I used CHIRPS daily rainfall and aggregated it to monthly rainfall. | Rainfall is the main water-supply signal behind many drought events. |
| Pulled temperature data | I used MODIS land surface temperature. | Heat can intensify drought stress by increasing water demand and vegetation pressure. |
| Aggregated data monthly | I summarized NDVI, rainfall, and temperature by grid cell and month. | Monthly data are easier to compare across time and suitable for drought monitoring. |
| Created climatologies | I calculated normal monthly conditions for each grid cell. | Drought is about how unusual conditions are compared with normal local conditions, not only raw rainfall or temperature values. |
| Created anomalies | I calculated NDVI, rainfall, and temperature departures from normal. | Anomalies make the drought signal clearer across different climates inside the MENA region. |
| Created rolling summaries | I added 3-month and 6-month rolling indicators. | Drought builds over time, so rolling features capture accumulated stress better than one month alone. |
| Created drought classes | I assigned drought severity classes from NDVI anomaly thresholds. | This created a transparent drought label tied directly to vegetation stress. |
| Avoided label leakage | I excluded NDVI and NDVI-anomaly fields from the model predictors. | The model should learn drought conditions from rainfall, heat, season, and location, not simply repeat the rule used to create the label. |
| Trained a Random Forest model | I used Random Forest as the baseline classifier. | It works well for tabular environmental data and gives interpretable feature importance. |
| Used a later-period test split | I tested the model on later months from 2023 onward. | This checks whether the model can work on future months rather than only fitting past data. |
| Exported outputs | I set up figures, CSV tables, and an interactive map output. | The project should be understandable outside the notebook, not only through code cells. |
| Moved core logic into `src/` | I separated reusable feature and modeling helpers from the notebook. | This makes the project easier to test, reuse, and improve. |
| Added tests | I added tests for configuration, feature engineering, drought classes, and modeling splits. | Tests protect the project from silent errors when the workflow changes. |
| Added composite drought scoring | I added a reusable score that combines vegetation, rainfall, heat, soil moisture, and evapotranspiration-deficit evidence when those columns are available. | A multi-evidence score is more credible than relying on NDVI anomaly alone. |
| Added crop-season weighting | I added helpers to weight drought scores during active growing months. | Agricultural drought is most important when crops are actively growing. |
| Added independent validation helpers | I added SPEI drought-class and agreement-summary helpers. | The NDVI-based drought label should be compared with an independent drought indicator. |
| Added prediction-confidence outputs | I added probability, margin, entropy, and confidence-label outputs for model predictions. | A useful drought map should show how certain each prediction is. |
| Added MODIS quality-mask helper | I added an Earth Engine helper for masking MODIS `DetailedQA` vegetation-index pixels. | Quality masking improves the reliability of NDVI-based drought labels. |

## Novelty Applied So Far

The main novelty has now been implemented in the reusable project code. The final maps still need to be regenerated after Earth Engine authentication or from an existing processed export.

| Applied Novelty | Status | Why It Matters |
|---|---|---|
| Leakage-aware drought modeling | Applied | The model avoids using NDVI fields that directly define the target label. |
| Fixed-reference climatology support | Applied in reusable code | This allows climatologies to be built from a historical reference period instead of using future evaluation months. |
| Rolling anomaly predictors | Applied in reusable code | The model can now use rolling rainfall and temperature anomalies, not only raw rolling values. |
| Spatial holdout testing | Applied in reusable code | The project can now test whether the model generalizes to unseen grid cells. |
| MODIS QA masking helper | Applied in reusable code | The notebook can now mask lower-quality MODIS vegetation pixels before aggregation. |
| Composite drought score | Applied in reusable code | The project can combine vegetation, rainfall, heat, soil moisture, and evapotranspiration evidence. |
| Crop-season weighting | Applied in reusable code | Agricultural drought severity can now be weighted by active growing months. |
| SPEI-style validation | Applied in reusable code | Model or composite classes can now be compared with an independent drought index. |
| Prediction confidence | Applied in reusable code | Map-ready tables can include probability, margin, entropy, and confidence labels. |
| Full research roadmap | Applied in documentation | The project now has a complete plan from baseline workflow to final validated research output. |

## What Still Requires A Data Run

The methods are implemented, but the final real-data outputs must be regenerated after Earth Engine authentication or from an existing extracted table.

| Output Task | Current Status | Why It Is Still Needed |
|---|---|---|
| Rerun Earth Engine extraction with QA masking | Requires authentication | This creates cleaner NDVI, rainfall, and temperature inputs. |
| Regenerate feature table with fixed climatology | Requires processed data | This applies the leakage-control feature settings to the real table. |
| Export composite drought score | Requires processed data | This creates the multi-evidence drought score for real grid-month rows. |
| Export crop-weighted drought score | Requires crop months or crop calendar | This makes the output more agricultural. |
| Export prediction confidence | Requires trained model and latest feature table | This adds uncertainty information to the map. |
| Compare with SPEI, SPI, WaPOR, or bulletins | Requires external validation data | This supports scientific credibility. |

## Are The Outputs Good?

The code outputs are in good shape at the structural level:

- the reusable Python helpers run successfully;
- the feature-engineering tests pass;
- the modeling tests pass;
- the composite-score tests pass;
- the crop-season tests pass;
- the validation tests pass;
- the documentation now explains the workflow and improvement path;
- the project is organized clearly around a notebook, reusable code, tests, and outputs.

The final map and model-result quality cannot be fully judged from the repository alone because the generated figures, CSV outputs, and interactive map are not committed. To judge the analytical quality, the notebook needs to be run with Earth Engine access and the exported results need to be reviewed.

The correct conclusion is:

The project foundation is good, but the final drought map should be treated as a prototype until the notebook is rerun with quality masking, independent validation, and confidence reporting.

## Main Strengths

1. The project uses real Earth observation data rather than simulated data.
2. The workflow is transparent and easy to explain.
3. The drought labels are simple and interpretable.
4. The model avoids direct NDVI label leakage.
5. The project produces map-ready outputs, not only model scores.
6. The reusable code and tests make the project easier to improve.

## Main Limitations

1. The drought label is based on NDVI anomaly, not an independent observed drought-event inventory.
2. MODIS quality masking still needs to be applied before relying on the vegetation signal.
3. The broad grid is useful for a prototype but less precise than administrative or agro-ecological boundaries.
4. Temporal testing alone is not enough; spatial holdout testing should also be run.
5. The map should include confidence or uncertainty before being used for decision support.

## Recommended Next Steps

| Priority | Next Step | Reason |
|---|---|---|
| 1 | Apply MODIS quality masking in the Earth Engine extraction. | This improves the reliability of NDVI anomalies and drought labels. |
| 2 | Update the notebook to use the reusable `src/` feature and modeling helpers. | This keeps the notebook consistent with the tested code. |
| 3 | Use a fixed climatology reference period in the notebook. | This reduces the risk of future information influencing evaluation months. |
| 4 | Run both temporal and spatial holdout evaluations. | This shows whether the model works across time and across unseen locations. |
| 5 | Export prediction confidence with the latest drought map. | This makes the map more honest and useful. |
| 6 | Add SPEI, SPI, WaPOR, or soil-moisture comparison layers. | This moves the project from a vegetation-stress proxy toward a stronger drought-risk product. |
| 7 | Add crop calendar or crop-mask weighting. | This makes the drought signal more relevant for agriculture. |

## Final Interpretation

This project is a strong first version of a MENA drought-risk mapping workflow. It is clear, reproducible, and built on real satellite and climate data.

The main scientific weakness is that the current drought label comes from NDVI anomaly only. That is acceptable for a transparent prototype, but a stronger final version should use multiple drought indicators and independent validation.

The most valuable enhancement path is to turn the project into a multi-evidence drought-risk system that combines vegetation stress, rainfall deficit, heat stress, water productivity, soil moisture, crop season, and prediction confidence.
