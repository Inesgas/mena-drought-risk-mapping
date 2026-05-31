# Full Research Roadmap

## Research Aim

Develop a credible MENA drought-risk mapping workflow that combines open Earth observation data, transparent drought indicators, machine-learning classification, spatial-temporal validation, and map-ready outputs.

The project should evolve from a vegetation-stress prototype into a multi-evidence drought-risk system.

## Core Research Questions

1. Can monthly Earth observation data identify drought-risk patterns across the MENA region?
2. How well do rainfall, heat, seasonality, and location explain vegetation-stress drought classes?
3. Does model performance hold across both future months and unseen grid cells?
4. How does the NDVI-based drought signal compare with independent drought indicators such as SPEI, SPI, soil moisture, or WaPOR water-productivity layers?
5. Does crop-season weighting make the drought map more relevant for agricultural risk?
6. Can prediction confidence be mapped alongside drought class to make the output more reliable for interpretation?

## Hypotheses

| Hypothesis | Expected Evidence |
|---|---|
| Vegetation stress can be mapped from monthly satellite observations. | NDVI anomalies show meaningful drought-class variation across space and time. |
| Hydroclimate features explain part of the vegetation-stress signal. | Rainfall anomaly, rolling rainfall, temperature anomaly, and seasonality rank highly in model importance. |
| Temporal performance will be stronger than spatial holdout performance. | Later-month testing performs better than unseen-cell testing if the model relies on location-specific patterns. |
| A composite drought indicator is more credible than an NDVI-only label. | Composite scores align better with independent indicators and known drought periods. |
| Crop-season weighting improves agricultural interpretation. | Active-season drought scores better highlight agriculturally relevant stress periods. |
| Confidence mapping improves practical usability. | Low-confidence areas can be separated from high-confidence drought predictions. |

## Implemented Research Enhancements

| Enhancement | Implementation | Purpose |
|---|---|---|
| MODIS QA helper | `mask_mod13a3_detailed_qa` in `earth_engine.py` | Allows NDVI extraction to reject lower-quality MODIS pixels. |
| Fixed-reference climatology | `climatology_reference_end_date` in `add_drought_features` | Reduces leakage from evaluation months into anomaly baselines. |
| Rolling anomaly predictors | `rainfall_anom_3m`, `lst_c_anom_3m` | Captures accumulated departures from normal conditions. |
| Spatial holdout testing | `cell_holdout_split` | Tests generalization to unseen grid cells. |
| Composite drought score | `add_composite_drought_index` | Combines vegetation, rainfall, heat, soil moisture, and evapotranspiration evidence when available. |
| Crop-season weighting | `add_crop_season_weight` | Gives stronger weight to drought stress during active growing months. |
| SPEI validation class | `add_spei_validation_class` | Supports independent drought-index comparison. |
| Prediction confidence | `add_prediction_confidence` | Adds class probability, margin, entropy, and confidence label to map outputs. |
| Enhancement script | `scripts/apply_research_enhancements.py` | Applies the research enhancements to an extracted CSV table. |

## Phase 1: Reproducible Baseline

**Objective:** Keep the existing drought-risk mapping workflow clean, runnable, and explainable.

| Task | Output | Success Check |
|---|---|---|
| Run environment check | Dependency and Earth Engine status | `scripts/environment_check.py` completes. |
| Run the notebook end to end | Figures, map, latest prediction table | Output files are created under `outputs/`. |
| Confirm feature table columns | Processed table | Required feature columns exist and have plausible ranges. |
| Confirm class distribution | Drought-class counts | Classes are not collapsed into one dominant class only. |
| Run tests | Test report | All tests pass. |

## Phase 2: Data Quality And Leakage Control

**Objective:** Improve the trustworthiness of the satellite signal before modeling.

| Task | Method | Reason |
|---|---|---|
| Add MODIS QA masking | Use `DetailedQA` bits before NDVI reduction. | Poor-quality NDVI can create false drought labels. |
| Check NDVI scaling | Confirm NDVI values are near `-1` to `1`. | Prevents interpretation errors from unscaled MODIS values. |
| Use fixed climatology period | Build climatology only from reference months. | Keeps future test months out of anomaly baselines. |
| Save processed extraction table | Export CSV to `data/processed/`. | Makes results auditable and reproducible. |

## Phase 3: Stronger Feature Engineering

**Objective:** Move from simple monthly values to drought-relevant stress indicators.

| Feature Group | Columns | Purpose |
|---|---|---|
| Vegetation stress | `ndvi_anomaly`, `ndvi_anom_3m`, `ndvi_anom_6m` | Measures current and accumulated vegetation departure. |
| Rainfall stress | `rainfall_anomaly`, `rainfall_anom_3m` | Measures water-supply deficit. |
| Heat stress | `lst_c_anomaly`, `lst_c_anom_3m` | Measures thermal pressure. |
| Crop-season stress | `crop_season_weight`, `crop_weighted_drought_score` | Focuses interpretation on agricultural growing periods. |
| Composite stress | `composite_drought_score`, component stress columns | Combines multiple drought signals. |

## Phase 4: Model Evaluation

**Objective:** Show whether the model works beyond the data it was trained on.

| Evaluation | What It Tests | Required Output |
|---|---|---|
| Temporal split | Future months in known grid cells | Classification report and confusion matrix. |
| Spatial holdout split | Unseen grid cells | Classification report and confusion matrix. |
| Feature importance | Main explanatory drivers | Ranked feature-importance table and plot. |
| Confidence analysis | Prediction reliability | Probability, margin, entropy, confidence class. |
| Error analysis | Where the model fails | Confusion by class, month, and region. |

## Phase 5: Independent Validation

**Objective:** Avoid relying only on the NDVI-derived drought label.

| Validation Source | Comparison | Why It Helps |
|---|---|---|
| SPEI | Compare composite or predicted class with SPEI drought class. | Adds a meteorological drought benchmark. |
| SPI | Compare rainfall-only drought severity with model outputs. | Shows whether rainfall deficits explain vegetation stress. |
| WaPOR relative soil moisture | Compare water-stress signal with mapped drought. | Adds agricultural water-availability evidence. |
| WaPOR evapotranspiration and biomass | Compare water use and vegetation production with drought score. | Improves interpretation in irrigated and rainfed systems. |
| National drought bulletins | Compare known events with mapped classes. | Adds contextual credibility. |

## Phase 6: Composite Drought Indicator

**Objective:** Build a multi-evidence drought score that can sit beside the model output.

Recommended component structure:

| Component | Direction | Example Column |
|---|---|---|
| Vegetation stress | Lower anomaly means more stress | `ndvi_anom_3m` |
| Rainfall deficit | Lower anomaly means more stress | `rainfall_anom_3m` |
| Heat stress | Higher anomaly means more stress | `lst_c_anom_3m` |
| Soil moisture deficit | Lower anomaly means more stress | `soil_moisture_anomaly` |
| Evapotranspiration deficit | Higher deficit means more stress | `et_deficit` |

The implemented composite function rescales available components into stress scores between `0` and `1`, applies normalized weights, and assigns drought classes from the final score.

## Phase 7: Crop And Exposure Context

**Objective:** Move from hazard mapping toward risk mapping.

| Addition | Purpose |
|---|---|
| Crop calendar | Identify months when vegetation stress matters most for crops. |
| Cropland mask | Separate agricultural drought from natural dryland vegetation dynamics. |
| Irrigation mask | Interpret drought differently in irrigated and rainfed areas. |
| Population or cropland exposure | Estimate who or what is exposed to drought hazard. |
| Administrative boundaries | Produce summaries useful for policy reporting. |

## Phase 8: Final Outputs

The final project should export:

1. Processed monthly feature table.
2. Drought-class distribution table.
3. Temporal validation report.
4. Spatial holdout validation report.
5. Independent validation summary.
6. Composite drought-score table.
7. Latest drought prediction table with confidence columns.
8. Feature-importance plot.
9. Confusion matrix.
10. Annual drought-severity share plot.
11. Interactive drought map.
12. Interactive confidence or uncertainty map.

## Credibility Checklist

| Check | Required For Credibility |
|---|---|
| Real data extraction runs successfully | Yes |
| MODIS QA mask is applied | Yes |
| NDVI scaling is correct | Yes |
| Climatology uses a reference period | Yes |
| NDVI-derived predictors are excluded from the model | Yes |
| Temporal split is reported | Yes |
| Spatial holdout split is reported | Yes |
| Prediction confidence is exported | Yes |
| Independent drought validation is included | Strongly recommended |
| Limitations are stated clearly | Yes |

## Suggested Final Research Claim

This project presents a reproducible MENA drought-risk mapping workflow using open Earth observation data. It combines vegetation, rainfall, and heat indicators with leakage-aware feature engineering, temporal and spatial validation, composite drought scoring, crop-season weighting, and confidence reporting. The current NDVI-based label is treated as a transparent vegetation-stress proxy, while independent validation with drought indices or water-productivity data is used to strengthen scientific credibility.

