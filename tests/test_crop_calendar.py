import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mena_drought_risk_mapping.crop_calendar import (
    add_crop_season_weight,
    month_in_season,
    weight_score_by_crop_season,
)


class CropCalendarTests(unittest.TestCase):
    def test_month_in_season_handles_wrapped_season(self):
        self.assertTrue(month_in_season(12, 11, 3))
        self.assertTrue(month_in_season(2, 11, 3))
        self.assertFalse(month_in_season(7, 11, 3))

    def test_add_crop_season_weight_from_active_months(self):
        df = pd.DataFrame({"month": [1, 6], "value": [10, 20]})

        weighted = add_crop_season_weight(df, active_months=[11, 12, 1, 2, 3])

        self.assertTrue(weighted.loc[0, "is_active_crop_season"])
        self.assertFalse(weighted.loc[1, "is_active_crop_season"])
        self.assertEqual(weighted.loc[0, "crop_season_weight"], 1.0)
        self.assertEqual(weighted.loc[1, "crop_season_weight"], 0.35)

    def test_weight_score_by_crop_season(self):
        df = pd.DataFrame(
            {
                "composite_drought_score": [0.8, 0.8],
                "crop_season_weight": [1.0, 0.25],
            }
        )

        weighted = weight_score_by_crop_season(df)

        self.assertEqual(weighted.loc[0, "crop_weighted_drought_score"], 0.8)
        self.assertEqual(weighted.loc[1, "crop_weighted_drought_score"], 0.2)


if __name__ == "__main__":
    unittest.main()
