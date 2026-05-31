from __future__ import annotations

import numpy as np
import pandas as pd


def month_in_season(month: int, start_month: int, end_month: int) -> bool:
    for value, name in [
        (month, "month"),
        (start_month, "start_month"),
        (end_month, "end_month"),
    ]:
        if value < 1 or value > 12:
            raise ValueError(f"{name} must be between 1 and 12.")

    if start_month <= end_month:
        return start_month <= month <= end_month
    return month >= start_month or month <= end_month


def add_crop_season_weight(
    df: pd.DataFrame,
    active_months: list[int] | tuple[int, ...] | set[int] | None = None,
    start_month_column: str | None = None,
    end_month_column: str | None = None,
    month_column: str = "month",
    date_column: str = "date",
    output_column: str = "crop_season_weight",
    active_column: str = "is_active_crop_season",
    active_weight: float = 1.0,
    inactive_weight: float = 0.35,
) -> pd.DataFrame:
    out = df.copy()

    if month_column not in out.columns:
        if date_column not in out.columns:
            raise ValueError(f"Input table needs either {month_column} or {date_column}.")
        out[month_column] = pd.to_datetime(out[date_column]).dt.month

    if active_months is not None:
        month_set = {int(month) for month in active_months}
        for month in month_set:
            if month < 1 or month > 12:
                raise ValueError("active_months values must be between 1 and 12.")
        active_mask = out[month_column].isin(month_set)
    elif start_month_column and end_month_column:
        missing = {start_month_column, end_month_column} - set(out.columns)
        if missing:
            raise ValueError(
                "Input table is missing crop season columns: "
                + ", ".join(sorted(missing))
            )
        active_mask = out.apply(
            lambda row: month_in_season(
                int(row[month_column]),
                int(row[start_month_column]),
                int(row[end_month_column]),
            ),
            axis=1,
        )
    else:
        raise ValueError(
            "Provide either active_months or start_month_column and end_month_column."
        )

    out[active_column] = active_mask.astype(bool)
    out[output_column] = np.where(out[active_column], active_weight, inactive_weight)
    return out


def weight_score_by_crop_season(
    df: pd.DataFrame,
    score_column: str = "composite_drought_score",
    weight_column: str = "crop_season_weight",
    output_column: str = "crop_weighted_drought_score",
) -> pd.DataFrame:
    missing = {score_column, weight_column} - set(df.columns)
    if missing:
        raise ValueError("Input table is missing columns: " + ", ".join(sorted(missing)))

    out = df.copy()
    out[output_column] = out[score_column] * out[weight_column].clip(lower=0, upper=1)
    return out
