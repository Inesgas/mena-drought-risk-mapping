from __future__ import annotations

import numpy as np
import pandas as pd

from .config import ProjectConfig


def classify_spei_drought(value: float) -> float:
    if pd.isna(value):
        return np.nan
    if value <= -2.0:
        return 3
    if value <= -1.5:
        return 2
    if value <= -1.0:
        return 1
    return 0


def add_spei_validation_class(
    df: pd.DataFrame,
    spei_column: str = "spei",
    class_column: str = "spei_drought_class",
    label_column: str = "spei_drought_label",
    class_names: dict[int, str] | None = None,
) -> pd.DataFrame:
    if spei_column not in df.columns:
        raise ValueError(f"Input table is missing SPEI column: {spei_column}")

    out = df.copy()
    out[class_column] = out[spei_column].apply(classify_spei_drought)
    out[label_column] = out[class_column].map(class_names or ProjectConfig().class_names)
    return out


def external_validation_summary(
    df: pd.DataFrame,
    predicted_class_column: str,
    reference_class_column: str,
) -> dict[str, float | int]:
    missing = {predicted_class_column, reference_class_column} - set(df.columns)
    if missing:
        raise ValueError("Input table is missing columns: " + ", ".join(sorted(missing)))

    valid = df[[predicted_class_column, reference_class_column]].dropna()
    if valid.empty:
        raise ValueError("No valid prediction/reference rows are available.")

    y_pred = valid[predicted_class_column].astype(int)
    y_ref = valid[reference_class_column].astype(int)
    labels = sorted(set(y_pred) | set(y_ref))

    agreement = float((y_ref == y_pred).mean())
    recalls = []
    f1_scores = []

    for label in labels:
        true_positive = int(((y_ref == label) & (y_pred == label)).sum())
        false_positive = int(((y_ref != label) & (y_pred == label)).sum())
        false_negative = int(((y_ref == label) & (y_pred != label)).sum())

        reference_count = true_positive + false_negative
        if reference_count > 0:
            recalls.append(true_positive / reference_count)

        precision_denominator = true_positive + false_positive
        recall_denominator = true_positive + false_negative
        precision = (
            true_positive / precision_denominator
            if precision_denominator > 0
            else 0.0
        )
        recall = true_positive / recall_denominator if recall_denominator > 0 else 0.0
        if precision + recall == 0:
            f1_scores.append(0.0)
        else:
            f1_scores.append(2 * precision * recall / (precision + recall))

    return {
        "n_rows": int(len(valid)),
        "agreement": agreement,
        "balanced_agreement": float(np.mean(recalls)),
        "macro_f1": float(np.mean(f1_scores)),
    }


def validation_confusion_table(
    df: pd.DataFrame,
    predicted_class_column: str,
    reference_class_column: str,
) -> pd.DataFrame:
    missing = {predicted_class_column, reference_class_column} - set(df.columns)
    if missing:
        raise ValueError("Input table is missing columns: " + ", ".join(sorted(missing)))

    valid = df[[predicted_class_column, reference_class_column]].dropna()
    return pd.crosstab(
        valid[reference_class_column].astype(int),
        valid[predicted_class_column].astype(int),
        rownames=["reference_class"],
        colnames=["predicted_class"],
        dropna=False,
    )
