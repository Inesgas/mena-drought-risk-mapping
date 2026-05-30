# Authentication And Verification

## Why Authentication Is Needed

The project uses Google Earth Engine to pull MODIS, CHIRPS, and land-surface-temperature data. Earth Engine access is tied to a Google account and, in many setups, a Google Cloud project.

The local code can be tested without Earth Engine, but the real satellite extraction and final map regeneration require authenticated Earth Engine access.

## Earth Engine Setup

From the project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
earthengine authenticate
python scripts/environment_check.py
```

If the notebook still fails at initialization, use this in the notebook:

```python
import ee

ee.Authenticate()
ee.Initialize(project="your-google-cloud-project-id")
```

Replace `your-google-cloud-project-id` with a Google Cloud project where Earth Engine is enabled.

## Running The Project

1. Run the setup script.

```powershell
python scripts/project_setup.py
```

2. Run the tests.

```powershell
python -m unittest discover -s tests
```

3. Open and run the notebook from top to bottom.

```powershell
jupyter notebook notebooks/drought_risk_mapping_mena_real_data.ipynb
```

4. Check that outputs are created under:

```text
outputs/figures/
outputs/maps/
outputs/tables/
```

## Applying The Research Enhancements

After an extracted table is available as a CSV, run:

```powershell
python scripts/apply_research_enhancements.py --input data/processed/extracted_monthly_grid.csv --output data/processed/enhanced_monthly_grid.csv --climatology-reference-end-date 2022-12-31 --active-months 11,12,1,2,3,4
```

If the table includes a SPEI column, add:

```powershell
--spei-column spei
```

## Output Checks

| Check | What To Look For |
|---|---|
| Extracted columns | `cell_id`, `date`, `ndvi`, `rainfall`, `lst_c`, `lat`, `lon` exist. |
| NDVI range | NDVI values are normally between `-1` and `1` after scaling. |
| Missing values | Missing data are limited and explainable. |
| Drought classes | The output is not collapsed into one class only. |
| Temporal test | Later months are held out for evaluation. |
| Spatial test | Some grid cells are held out completely. |
| Confidence | Latest predictions include probability, margin, entropy, and confidence label. |
| Composite score | `composite_drought_score` exists and varies across grid cells/months. |
| Independent validation | SPEI/SPI/WaPOR or bulletin comparison is reported if data are available. |

## Credibility Checklist

The project is credible when these conditions are met:

1. Earth Engine extraction runs successfully.
2. MODIS quality masking is applied before NDVI aggregation.
3. NDVI, rainfall, and temperature values have plausible ranges.
4. Climatology uses a fixed reference period.
5. NDVI-derived label fields are excluded from model predictors.
6. Temporal validation is reported.
7. Spatial holdout validation is reported.
8. Prediction confidence is exported with the latest map table.
9. Independent validation is included when external drought data are available.
10. Limitations are clearly stated.

