"""Reusable helpers for the MENA drought-risk mapping project."""

from .config import ProjectConfig
from .composite import (
    CompositeDroughtConfig,
    add_composite_drought_index,
    classify_composite_drought_score,
)
from .crop_calendar import add_crop_season_weight, month_in_season
from .features import (
    add_drought_features,
    classify_drought_from_ndvi,
    default_model_features,
)
from .modeling import (
    add_prediction_confidence,
    cell_holdout_split,
    temporal_train_test_split,
)
from .validation import add_spei_validation_class, external_validation_summary

__all__ = [
    "CompositeDroughtConfig",
    "ProjectConfig",
    "add_composite_drought_index",
    "add_crop_season_weight",
    "add_drought_features",
    "add_prediction_confidence",
    "add_spei_validation_class",
    "cell_holdout_split",
    "classify_composite_drought_score",
    "classify_drought_from_ndvi",
    "default_model_features",
    "external_validation_summary",
    "month_in_season",
    "temporal_train_test_split",
]
