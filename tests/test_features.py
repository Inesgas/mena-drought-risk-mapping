import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mena_drought_risk_mapping.config import ProjectConfig
from mena_drought_risk_mapping.features import (
    add_drought_features,
    classify_drought_from_ndvi,
    default_model_features,
    validate_feature_input,
)


class FeatureTests(unittest.TestCase):
    def test_drought_class_thresholds(self):
        self.assertEqual(classify_drought_from_ndvi(-0.15), 3)
        self.assertEqual(classify_drought_from_ndvi(-0.10), 2)
        self.assertEqual(classify_drought_from_ndvi(-0.05), 1)
        self.assertEqual(classify_drought_from_ndvi(-0.01), 0)
        self.assertTrue(np.isnan(classify_drought_from_ndvi(np.nan)))

    def test_add_drought_features_uses_cell_month_climatology(self):
        df = pd.DataFrame(
            {
                "cell_id": [1, 1, 1],
                "date": ["2020-01-01", "2021-01-01", "2021-02-01"],
                "ndvi": [0.40, 0.20, 0.50],
                "rainfall": [10.0, 30.0, 20.0],
                "lst_c": [25.0, 35.0, 30.0],
                "lat": [20.0, 20.0, 20.0],
                "lon": [30.0, 30.0, 30.0],
            }
        )

        features = add_drought_features(df, ProjectConfig())
        jan_2021 = features.loc[features["date"] == pd.Timestamp("2021-01-01")].iloc[0]

        self.assertAlmostEqual(jan_2021["ndvi_climatology"], 0.30)
        self.assertAlmostEqual(jan_2021["ndvi_anomaly"], -0.10)
        self.assertIn("ndvi_anom_6m", features.columns)
        self.assertIn("rainfall_anom_3m", features.columns)
        self.assertIn("lst_c_anom_3m", features.columns)
        self.assertEqual(jan_2021["drought_class"], 2)

    def test_reference_end_date_prevents_future_climatology_leakage(self):
        df = pd.DataFrame(
            {
                "cell_id": [1, 1],
                "date": ["2020-01-01", "2021-01-01"],
                "ndvi": [0.40, 0.20],
                "rainfall": [10.0, 30.0],
                "lst_c": [25.0, 35.0],
                "lat": [20.0, 20.0],
                "lon": [30.0, 30.0],
            }
        )

        features = add_drought_features(
            df,
            ProjectConfig(),
            climatology_reference_end_date="2020-12-31",
        )
        jan_2021 = features.loc[features["date"] == pd.Timestamp("2021-01-01")].iloc[0]

        self.assertAlmostEqual(jan_2021["ndvi_climatology"], 0.40)
        self.assertAlmostEqual(jan_2021["ndvi_anomaly"], -0.20)

    def test_validate_feature_input_reports_missing_columns(self):
        with self.assertRaisesRegex(ValueError, "lst_c"):
            validate_feature_input(
                pd.DataFrame(
                    {
                        "cell_id": [1],
                        "date": ["2020-01-01"],
                        "ndvi": [0.4],
                        "rainfall": [10.0],
                        "lat": [20.0],
                        "lon": [30.0],
                    }
                )
            )

    def test_default_model_features_exclude_ndvi_label_fields(self):
        features = default_model_features()
        self.assertNotIn("ndvi", features)
        self.assertNotIn("ndvi_anomaly", features)
        self.assertIn("rainfall_anomaly", features)
        self.assertIn("rainfall_anom_3m", features)
        self.assertIn("lst_c_anomaly", features)
        self.assertIn("lst_c_anom_3m", features)


if __name__ == "__main__":
    unittest.main()
