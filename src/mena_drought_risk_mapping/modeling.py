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


def cell_holdout_split(
    df: pd.DataFrame,
    holdout_fraction: float = 0.2,
    cell_column: str = "cell_id",
    random_state: int = 42,
) -> TemporalSplit:
    if cell_column not in df.columns:
        raise ValueError(f"Input table is missing the cell column: {cell_column}")
    if not 0 < holdout_fraction < 1:
        raise ValueError("holdout_fraction must be greater than 0 and less than 1.")

    cells = np.array(sorted(pd.unique(df[cell_column].dropna())))
    if cells.size < 2:
        raise ValueError("At least two unique cells are required for a holdout split.")

    rng = np.random.default_rng(random_state)
    holdout_size = max(1, int(round(cells.size * holdout_fraction)))
    holdout_cells = set(rng.choice(cells, size=holdout_size, replace=False))

    test_mask = df[cell_column].isin(holdout_cells)
    train_df = df[~test_mask].copy()
    test_df = df[test_mask].copy()
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


def classify_prediction_confidence(probability: float, margin: float) -> str:
    if probability >= 0.70 and margin >= 0.20:
        return "High"
    if probability >= 0.50 and margin >= 0.10:
        return "Medium"
    return "Low"


def add_prediction_confidence(
    model,
    df: pd.DataFrame,
    feature_columns: list[str],
    class_names: dict[int, str] | None = None,
    prefix: str = "predicted",
) -> pd.DataFrame:
    if not hasattr(model, "predict_proba"):
        raise ValueError("Model must provide predict_proba for confidence outputs.")

    out = df.copy()
    probabilities = np.asarray(model.predict_proba(out[feature_columns]), dtype=float)
    classes = np.asarray(getattr(model, "classes_", np.arange(probabilities.shape[1])))

    top_indices = probabilities.argmax(axis=1)
    top_probabilities = probabilities[np.arange(len(probabilities)), top_indices]
    sorted_probabilities = np.sort(probabilities, axis=1)
    second_probabilities = (
        sorted_probabilities[:, -2]
        if probabilities.shape[1] > 1
        else np.zeros(len(probabilities))
    )
    margins = top_probabilities - second_probabilities

    safe_probabilities = np.clip(probabilities, 1e-12, 1.0)
    entropy = -np.sum(probabilities * np.log(safe_probabilities), axis=1)
    if probabilities.shape[1] > 1:
        entropy = entropy / np.log(probabilities.shape[1])

    class_column = f"{prefix}_class"
    label_column = f"{prefix}_label"
    probability_column = f"{prefix}_probability"
    margin_column = f"{prefix}_margin"
    entropy_column = f"{prefix}_entropy"
    confidence_column = f"{prefix}_confidence"

    out[class_column] = classes[top_indices]
    out[probability_column] = top_probabilities
    out[margin_column] = margins
    out[entropy_column] = entropy
    out[confidence_column] = [
        classify_prediction_confidence(probability, margin)
        for probability, margin in zip(top_probabilities, margins)
    ]

    if class_names is not None:
        out[label_column] = out[class_column].map(class_names)

    for class_index, class_value in enumerate(classes):
        out[f"{prefix}_prob_class_{class_value}"] = probabilities[:, class_index]

    return out
