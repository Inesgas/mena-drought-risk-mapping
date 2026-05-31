import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mena_drought_risk_mapping.composite import (
    add_composite_drought_index,
    classify_composite_drought_score,
)


class CompositeDroughtTests(unittest.TestCase):
    def test_composite_score_increases_with_stress(self):
        df = pd.DataFrame(
            {
                "ndvi_anom_3m": [0.10, -0.20],
                "rainfall_anom_3m": [20.0, -40.0],
                "lst_c_anom_3m": [-1.0, 5.0],
            }
        )

        scored = add_composite_drought_index(df)

        self.assertLess(
            scored.loc[0, "composite_drought_score"],
            scored.loc[1, "composite_drought_score"],
        )
        self.assertIn("composite_vegetation_stress", scored.columns)
        self.assertIn("composite_drought_label", scored.columns)

    def test_composite_score_uses_crop_weight_when_available(self):
        df = pd.DataFrame(
            {
                "ndvi_anom_3m": [-0.05, -0.20, -0.20],
                "rainfall_anom_3m": [-10.0, -40.0, -40.0],
                "lst_c_anom_3m": [1.0, 5.0, 5.0],
                "crop_season_weight": [1.0, 1.0, 0.35],
            }
        )

        scored = add_composite_drought_index(df)

        self.assertGreater(
            scored.loc[1, "composite_crop_weighted_score"],
            scored.loc[2, "composite_crop_weighted_score"],
        )

    def test_composite_class_thresholds(self):
        self.assertEqual(classify_composite_drought_score(0.80), 3)
        self.assertEqual(classify_composite_drought_score(0.60), 2)
        self.assertEqual(classify_composite_drought_score(0.30), 1)
        self.assertEqual(classify_composite_drought_score(0.10), 0)


if __name__ == "__main__":
    unittest.main()
