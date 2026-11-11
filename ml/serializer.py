"""Artifact serialization module for SmartKrishi ML model and evaluation reports."""

from pathlib import Path
from typing import Any
import json
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

from ml.config import ARTIFACTS_DIR


def save_artifacts(
    pipeline: Pipeline,
    label_encoder: LabelEncoder,
    metrics: dict[str, Any],
    confusion_payload: dict[str, Any],
    output_dir: Path | str | None = None,
) -> dict[str, Path]:
    """Persist trained model pipeline, label encoder, metrics JSON, and confusion matrix JSON."""
    target_dir = Path(output_dir) if output_dir is not None else ARTIFACTS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    model_path = target_dir / "crop_rf_model.joblib"
    encoder_path = target_dir / "label_encoder.joblib"
    metrics_path = target_dir / "model_metrics.json"
    cm_path = target_dir / "confusion_matrix.json"

    joblib.dump(pipeline, model_path)
    joblib.dump(label_encoder, encoder_path)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    cm_path.write_text(json.dumps(confusion_payload, indent=2), encoding="utf-8")

    return {
        "model": model_path,
        "label_encoder": encoder_path,
        "metrics": metrics_path,
        "confusion_matrix": cm_path,
    }
