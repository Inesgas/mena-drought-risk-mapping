from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from mena_drought_risk_mapping.composite import add_composite_drought_index
from mena_drought_risk_mapping.config import ProjectConfig
from mena_drought_risk_mapping.crop_calendar import add_crop_season_weight
from mena_drought_risk_mapping.features import add_drought_features
from mena_drought_risk_mapping.validation import add_spei_validation_class


def parse_active_months(value: str) -> list[int]:
    return [int(month.strip()) for month in value.split(",") if month.strip()]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Apply research enhancements to an extracted drought table."
    )
    parser.add_argument("--input", required=True, help="Input CSV with extracted rows.")
    parser.add_argument("--output", required=True, help="Output enhanced CSV path.")
    parser.add_argument(
        "--climatology-reference-end-date",
        default=None,
        help="Last date allowed in climatology reference calculations.",
    )
    parser.add_argument(
        "--active-months",
        default=None,
        help="Comma-separated crop-season months, for example 11,12,1,2,3,4.",
    )
    parser.add_argument(
        "--spei-column",
        default=None,
        help="Optional SPEI column to classify for independent validation.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    df = pd.read_csv(input_path)
    enhanced = add_drought_features(
        df,
        ProjectConfig(),
        climatology_reference_end_date=args.climatology_reference_end_date,
    )

    if args.active_months:
        enhanced = add_crop_season_weight(
            enhanced,
            active_months=parse_active_months(args.active_months),
        )

    enhanced = add_composite_drought_index(enhanced)

    if args.spei_column:
        enhanced = add_spei_validation_class(enhanced, spei_column=args.spei_column)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    enhanced.to_csv(output_path, index=False)
    print(f"Wrote enhanced table: {output_path}")


if __name__ == "__main__":
    main()
