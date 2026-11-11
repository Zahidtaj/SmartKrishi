"""Training entry point for the SmartKrishi Random Forest crop classifier."""

from pathlib import Path
from typing import Any
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from ml.config import ARTIFACTS_DIR, DATASET_PATH, RANDOM_STATE
from ml.data_loader import load_crop_dataset
from ml.data_validator import validate_crop_dataset
from ml.evaluate import evaluate_classifier
from ml.preprocessor import split_and_preprocess
from ml.serializer import save_artifacts


def build_rf_pipeline(random_state: int = RANDOM_STATE) -> Pipeline:
    """Construct a clean, reproducible Scikit-learn pipeline (scaler + regularized RandomForest)."""
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=150,
                    max_depth=14,
                    min_samples_leaf=2,
                    random_state=random_state,
                    n_jobs=1,
                ),
            ),
        ]
    )


def run_training_pipeline(
    dataset_path: Path | str | None = DATASET_PATH,
    artifacts_dir: Path | str | None = ARTIFACTS_DIR,
) -> dict[str, Any]:
    """Execute load -> validate -> split -> train -> evaluate -> serialize."""
    raw_df = load_crop_dataset(dataset_path)
    clean_df, validation_report = validate_crop_dataset(raw_df)
    if not validation_report.passed:
        raise RuntimeError("Dataset validation failed; aborting training.")

    splits = split_and_preprocess(clean_df)
    pipeline = build_rf_pipeline()
    pipeline.fit(splits.X_train_raw, splits.y_train)

    metrics, confusion_payload = evaluate_classifier(
        pipeline=pipeline,
        X_train=splits.X_train_raw,
        y_train=splits.y_train,
        X_test=splits.X_test_raw,
        y_test=splits.y_test,
        class_names=splits.class_names,
        feature_names=splits.feature_names,
    )

    saved_paths = save_artifacts(
        pipeline=pipeline,
        label_encoder=splits.label_encoder,
        metrics=metrics,
        confusion_payload=confusion_payload,
        output_dir=artifacts_dir,
    )

    return {
        "validation_rows": validation_report.valid_rows,
        "metrics": metrics,
        "artifacts": {k: str(v) for k, v in saved_paths.items()},
    }


if __name__ == "__main__":
    summary = run_training_pipeline()
    m = summary["metrics"]
    print(
        f"Training complete on {summary['validation_rows']} valid records | "
        f"Test Accuracy={m['test_accuracy']:.4f}, Macro F1={m['macro_f1']:.4f}, "
        f"CV F1={m['cv_macro_f1_mean']:.4f} +/- {m['cv_macro_f1_std']:.4f}"
    )
