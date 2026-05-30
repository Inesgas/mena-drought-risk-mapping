import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mena_drought_risk_mapping.config import ProjectConfig


class ConfigTests(unittest.TestCase):
    def test_extraction_end_date_includes_final_analysis_day(self):
        config = ProjectConfig(end_date="2024-12-31")

        self.assertEqual(config.extraction_end_date, "2025-01-01")


if __name__ == "__main__":
    unittest.main()
