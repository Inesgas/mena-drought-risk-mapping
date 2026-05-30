import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mena_drought_risk_mapping.modeling import temporal_train_test_split


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


if __name__ == "__main__":
    unittest.main()
