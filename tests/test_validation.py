import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mena_drought_risk_mapping.validation import (
    add_spei_validation_class,
    classify_spei_drought,
    external_validation_summary,
    validation_confusion_table,
)


class ValidationTests(unittest.TestCase):
    def test_spei_class_thresholds(self):
        self.assertEqual(classify_spei_drought(-2.1), 3)
        self.assertEqual(classify_spei_drought(-1.6), 2)
        self.assertEqual(classify_spei_drought(-1.1), 1)
        self.assertEqual(classify_spei_drought(-0.5), 0)

    def test_add_spei_validation_class(self):
        df = pd.DataFrame({"spei": [-2.1, -0.5]})

        classified = add_spei_validation_class(df)

        self.assertEqual(classified["spei_drought_class"].tolist(), [3, 0])
        self.assertIn("spei_drought_label", classified.columns)

    def test_external_validation_summary(self):
        df = pd.DataFrame(
            {
                "predicted_class": [0, 1, 2, 3],
                "spei_drought_class": [0, 1, 1, 3],
            }
        )

        summary = external_validation_summary(
            df, "predicted_class", "spei_drought_class"
        )
        table = validation_confusion_table(df, "predicted_class", "spei_drought_class")

        self.assertEqual(summary["n_rows"], 4)
        self.assertAlmostEqual(summary["agreement"], 0.75)
        self.assertEqual(table.loc[0, 0], 1)


if __name__ == "__main__":
    unittest.main()
