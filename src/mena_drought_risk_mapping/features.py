from __future__ import annotations

import numpy as np
import pandas as pd

from .config import ProjectConfig


REQUIRED_FEATURE_INPUTS = [
    "cell_id",
    "date",
    "ndvi",
    "rainfall",
    "lst_c",
    "lat",
    "lon",
]


def classify_drought_from_ndvi(anomaly: float) -> float:
    if pd.isna(anomaly):
        return np.nan
    if anomaly <= -0.14:
        return 3
    if anomaly <= -0.08:
        return 2
    if anomaly <= -0.04:
        return 1
    return 0


def validate_feature_input(df: pd.DataFrame) -> None:
    missing_columns = sorted(set(REQUIRED_FEATURE_INPUTS) - set(df.columns))
    if missing_columns:
        raise ValueError(
            "Input table is missing required columns: " + ", ".join(missing_columns)
        )


def _add_monthly_climatology_and_anomaly(
    df: pd.DataFrame,
    column: str,
    reference_end_date: str | None = None,
) -> pd.DataFrame:
    climatology_name = f"{column}_climatology"
    anomaly_name = f"{column}_anomaly"
    reference_df = df

    if reference_end_date is not None:
        reference_df = df[df["date"] <= pd.Timestamp(reference_end_date)]
        if reference_df.empty:
            raise ValueError(
                f"No rows are available for climatology through {reference_end_date}."
            )

    climatology = (
        reference_df.groupby(["cell_id", "month"])[column]
        .mean()
        .rename(climatology_name)
        .reset_index()
    )
    df = df.merge(climatology, on=["cell_id", "month"], how="left", validate="many_to_one")
    df[anomaly_name] = df[column] - df[climatology_name]
    return df


def _add_grouped_rolling_mean(
    df: pd.DataFrame,
    source_column: str,
    window: int,
    new_column: str,
) -> pd.DataFrame:
    df[new_column] = (
        df.groupby("cell_id")[source_column]
        .transform(lambda series: series.rolling(window, min_periods=1).mean())
    )
    return df


def add_drought_features(
    df: pd.DataFrame,
    config: ProjectConfig,
    climatology_reference_end_date: str | None = None,
) -> pd.DataFrame:
    validate_feature_input(df)

    feature_df = df.dropna(subset=["ndvi", "rainfall", "lst_c"]).copy()
    feature_df["date"] = pd.to_datetime(feature_df["date"])
    feature_df["month"] = feature_df["date"].dt.month
    feature_df["year"] = feature_df["date"].dt.year
    feature_df = feature_df.sort_values(["cell_id", "date"]).reset_index(drop=True)

    for base_column in ["ndvi", "rainfall", "lst_c"]:
        feature_df = _add_monthly_climatology_and_anomaly(
            feature_df,
            base_column,
            climatology_reference_end_date,
        )

    feature_df = _add_grouped_rolling_mean(feature_df, "ndvi_anomaly", 3, "ndvi_anom_3m")
    feature_df = _add_grouped_rolling_mean(feature_df, "ndvi_anomaly", 6, "ndvi_anom_6m")
    feature_df = _add_grouped_rolling_mean(feature_df, "rainfall", 3, "rainfall_3m")
    feature_df = _add_grouped_rolling_mean(feature_df, "lst_c", 3, "lst_3m")

    feature_df["drought_class"] = feature_df["ndvi_anomaly"].apply(classify_drought_from_ndvi)
    feature_df["drought_label"] = feature_df["drought_class"].map(config.class_names)

    return feature_df


def default_model_features() -> list[str]:
    return [
        "rainfall",
        "rainfall_3m",
        "rainfall_anomaly",
        "lst_c",
        "lst_3m",
        "month",
        "lat",
        "lon",
    ]
