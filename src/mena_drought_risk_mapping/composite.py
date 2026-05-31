from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .config import ProjectConfig


DEFAULT_COMPOSITE_WEIGHTS = {
    "vegetation": 0.35,
    "rainfall": 0.25,
    "heat": 0.20,
    "soil_moisture": 0.10,
    "evapotranspiration": 0.10,
}


@dataclass(frozen=True)
class CompositeDroughtConfig:
    vegetation_column: str = "ndvi_anom_3m"
    rainfall_column: str = "rainfall_anom_3m"
    heat_column: str = "lst_c_anom_3m"
    soil_moisture_column: str | None = "soil_moisture_anomaly"
    evapotranspiration_deficit_column: str | None = "et_deficit"
    crop_weight_column: str | None = "crop_season_weight"
    output_prefix: str = "composite"
    weights: dict[str, float] = field(
        default_factory=lambda: DEFAULT_COMPOSITE_WEIGHTS.copy()
    )


def classify_composite_drought_score(score: float) -> float:
    if pd.isna(score):
        return np.nan
    if score >= 0.75:
        return 3
    if score >= 0.50:
        return 2
    if score >= 0.25:
        return 1
    return 0


def _robust_stress_score(
    values: pd.Series,
    reference_values: pd.Series,
    high_values_mean_more_stress: bool,
) -> pd.Series:
    stress_values = values if high_values_mean_more_stress else -values
    reference_stress_values = (
        reference_values if high_values_mean_more_stress else -reference_values
    )
    clean_reference = reference_stress_values.dropna()

    if clean_reference.empty:
        return pd.Series(np.nan, index=values.index, dtype=float)

    lower = clean_reference.quantile(0.05)
    upper = clean_reference.quantile(0.95)
    if np.isclose(lower, upper):
        return pd.Series(0.0, index=values.index, dtype=float)

    return ((stress_values - lower) / (upper - lower)).clip(lower=0, upper=1)


def add_composite_drought_index(
    df: pd.DataFrame,
    config: CompositeDroughtConfig | None = None,
    reference_df: pd.DataFrame | None = None,
    class_names: dict[int, str] | None = None,
) -> pd.DataFrame:
    config = config or CompositeDroughtConfig()
    out = df.copy()
    reference = reference_df if reference_df is not None else out

    components = {
        "vegetation": (config.vegetation_column, False),
        "rainfall": (config.rainfall_column, False),
        "heat": (config.heat_column, True),
        "soil_moisture": (config.soil_moisture_column, False),
        "evapotranspiration": (config.evapotranspiration_deficit_column, True),
    }

    active_components: list[str] = []
    for component_name, (column, high_values_mean_more_stress) in components.items():
        if column is None or column not in out.columns:
            continue
        if column not in reference.columns:
            raise ValueError(f"Reference table is missing column: {column}")

        stress_column = f"{config.output_prefix}_{component_name}_stress"
        out[stress_column] = _robust_stress_score(
            out[column],
            reference[column],
            high_values_mean_more_stress,
        )
        active_components.append(component_name)

    if not active_components:
        raise ValueError("No composite drought indicator columns are available.")

    active_weights = {
        component: config.weights.get(component, 0.0)
        for component in active_components
        if config.weights.get(component, 0.0) > 0
    }
    if not active_weights:
        raise ValueError("At least one active composite weight must be positive.")

    total_weight = sum(active_weights.values())
    active_weights = {
        component: weight / total_weight for component, weight in active_weights.items()
    }

    numerator = pd.Series(0.0, index=out.index, dtype=float)
    denominator = pd.Series(0.0, index=out.index, dtype=float)

    for component, weight in active_weights.items():
        stress_column = f"{config.output_prefix}_{component}_stress"
        valid = out[stress_column].notna()
        numerator = numerator.add(out[stress_column].fillna(0) * weight)
        denominator = denominator.add(valid.astype(float) * weight)

    score_column = f"{config.output_prefix}_drought_score"
    class_column = f"{config.output_prefix}_drought_class"
    label_column = f"{config.output_prefix}_drought_label"

    out[score_column] = (numerator / denominator.replace(0, np.nan)).clip(
        lower=0, upper=1
    )
    out[class_column] = out[score_column].apply(classify_composite_drought_score)
    out[label_column] = out[class_column].map(class_names or ProjectConfig().class_names)

    if config.crop_weight_column and config.crop_weight_column in out.columns:
        out[f"{config.output_prefix}_crop_weighted_score"] = out[score_column] * out[
            config.crop_weight_column
        ].clip(lower=0, upper=1)

    return out
