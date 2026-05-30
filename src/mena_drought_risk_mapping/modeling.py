from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class TemporalSplit:
    train: pd.DataFrame
    test: pd.DataFrame


def temporal_train_test_split(
    df: pd.DataFrame,
    test_start_date: str,
    date_column: str = "date",
) -> TemporalSplit:
    dates = pd.to_datetime(df[date_column])
    test_start = pd.Timestamp(test_start_date)
    train_df = df[dates < test_start].copy()
    test_df = df[dates >= test_start].copy()
    return TemporalSplit(train=train_df, test=test_df)


def fit_random_forest(
    train_df: pd.DataFrame,
    feature_columns: list[str],
    target_column: str = "drought_class",
    random_state: int = 42,
) -> object:
    from sklearn.ensemble import RandomForestClassifier

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_leaf=3,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(train_df[feature_columns], train_df[target_column])
    return model


def evaluate_predictions(
    y_true: pd.Series | np.ndarray,
    y_pred: pd.Series | np.ndarray,
) -> dict[str, float]:
    from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro")),
    }


def feature_importance_series(model, feature_columns: list[str]) -> pd.Series:
    return pd.Series(model.feature_importances_, index=feature_columns).sort_values(
        ascending=False
    )
