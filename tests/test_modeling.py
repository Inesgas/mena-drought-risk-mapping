import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mena_drought_risk_mapping.modeling import (
    add_prediction_confidence,
    cell_holdout_split,
    temporal_train_test_split,
)


class FakeProbabilityModel:
    classes_ = [0, 1, 2]

    def predict_proba(self, x):
        return [
            [0.80, 0.15, 0.05],
            [0.40, 0.35, 0.25],
        ]


class ModelingTests(unittest.TestCase):
    def test_temporal_train_test_split_keeps_later_rows_for_testing(self):
        df = pd.DataFrame(
            {
                "date": pd.to_datetime(["2020-01-01", "2021-01-01", "2022-01-01"]),
                "value": [1, 2, 3],
            }
        )

        split = temporal_train_test_split(df, test_start_date="2022-01-01")

        self.assertEqual(split.train["value"].tolist(), [1, 2])
        self.assertEqual(split.test["value"].tolist(), [3])

    def test_cell_holdout_split_keeps_cells_out_of_training(self):
        df = pd.DataFrame(
            {
                "cell_id": [1, 1, 2, 2, 3, 3, 4, 4],
                "date": pd.date_range("2020-01-01", periods=8, freq="MS"),
                "value": range(8),
            }
        )

        split = cell_holdout_split(df, holdout_fraction=0.25, random_state=7)

        train_cells = set(split.train["cell_id"])
        test_cells = set(split.test["cell_id"])
        self.assertTrue(test_cells)
        self.assertTrue(train_cells.isdisjoint(test_cells))
        self.assertEqual(train_cells | test_cells, {1, 2, 3, 4})

    def test_cell_holdout_split_requires_multiple_cells(self):
        df = pd.DataFrame({"cell_id": [1, 1], "value": [1, 2]})

        with self.assertRaisesRegex(ValueError, "At least two unique cells"):
            cell_holdout_split(df)

    def test_add_prediction_confidence_outputs_probability_and_margin(self):
        df = pd.DataFrame({"x": [1.0, 2.0]})

        scored = add_prediction_confidence(
            FakeProbabilityModel(),
            df,
            ["x"],
            class_names={0: "Normal / Wet", 1: "Mild Drought", 2: "Moderate Drought"},
        )

        self.assertEqual(scored.loc[0, "predicted_class"], 0)
        self.assertEqual(scored.loc[0, "predicted_confidence"], "High")
        self.assertEqual(scored.loc[1, "predicted_confidence"], "Low")
        self.assertIn("predicted_prob_class_2", scored.columns)


if __name__ == "__main__":
    unittest.main()
