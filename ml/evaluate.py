"""Model evaluation module for SmartKrishi Random Forest classifier."""

from typing import Any
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline

from ml.config import CV_FOLDS, RANDOM_STATE


def evaluate_classifier(
    pipeline: Pipeline,
    X_train,
    y_train: np.ndarray,
    X_test,
    y_test: np.ndarray,
    class_names: list[str],
    feature_names: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Evaluate trained pipeline on held-out test set and cross-validation on training set.
    Returns (metrics_dict, confusion_matrix_dict).
    """
    y_train_pred = pipeline.predict(X_train)
    y_test_pred = pipeline.predict(X_test)

    train_accuracy = float(accuracy_score(y_train, y_train_pred))
    test_accuracy = float(accuracy_score(y_test, y_test_pred))
    macro_precision = float(precision_score(y_test, y_test_pred, average="macro", zero_division=0))
    macro_recall = float(recall_score(y_test, y_test_pred, average="macro", zero_division=0))
    macro_f1 = float(f1_score(y_test, y_test_pred, average="macro", zero_division=0))
    weighted_f1 = float(f1_score(y_test, y_test_pred, average="weighted", zero_division=0))

    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="f1_macro")

    per_class = classification_report(
        y_test,
        y_test_pred,
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )

    rf_step = pipeline.named_steps.get("classifier")
    feature_importances: dict[str, float] = {}
    if rf_step is not None and hasattr(rf_step, "feature_importances_"):
        feature_importances = {
            name: round(float(val), 6)
            for name, val in zip(feature_names, rf_step.feature_importances_)
        }

    cm = confusion_matrix(y_test, y_test_pred)

    metrics = {
        "model_type": "RandomForestClassifier",
        "train_samples": int(len(y_train)),
        "test_samples": int(len(y_test)),
        "num_classes": len(class_names),
        "train_accuracy": round(train_accuracy, 6),
        "test_accuracy": round(test_accuracy, 6),
        "macro_precision": round(macro_precision, 6),
        "macro_recall": round(macro_recall, 6),
        "macro_f1": round(macro_f1, 6),
        "weighted_f1": round(weighted_f1, 6),
        "cv_folds": CV_FOLDS,
        "cv_macro_f1_mean": round(float(np.mean(cv_scores)), 6),
        "cv_macro_f1_std": round(float(np.std(cv_scores)), 6),
        "overfitting_gap": round(train_accuracy - test_accuracy, 6),
        "feature_importances": feature_importances,
        "per_class_metrics": {
            cls: {
                "precision": round(float(per_class[cls]["precision"]), 4),
                "recall": round(float(per_class[cls]["recall"]), 4),
                "f1_score": round(float(per_class[cls]["f1-score"]), 4),
                "support": int(per_class[cls]["support"]),
            }
            for cls in class_names
            if cls in per_class
        },
    }

    confusion_payload = {
        "labels": class_names,
        "matrix": cm.tolist(),
    }

    return metrics, confusion_payload
