"""Safe model loading and probability prediction module for SmartKrishi."""

from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any
import joblib
import pandas as pd

from ml.config import ARTIFACTS_DIR, FEATURE_COLUMNS


class ModelLoadError(RuntimeError):
    """Raised when serialized ML artifacts are missing or corrupted."""


@dataclass
class CropPrediction:
    crop_key: str
    probability: float


class CropMLPredictor:
    """Loads serialized Scikit-learn Random Forest pipeline and predicts crop probabilities."""

    def __init__(self, artifacts_dir: Path | str | None = None) -> None:
        self.artifacts_dir = Path(artifacts_dir) if artifacts_dir is not None else ARTIFACTS_DIR
        self._pipeline = None
        self._label_encoder = None
        self._metrics: dict[str, Any] | None = None

    def load(self) -> None:
        model_path = self.artifacts_dir / "crop_rf_model.joblib"
        encoder_path = self.artifacts_dir / "label_encoder.joblib"
        metrics_path = self.artifacts_dir / "model_metrics.json"

        if not model_path.exists() or not encoder_path.exists():
            raise ModelLoadError(
                f"ML model artifacts missing in {self.artifacts_dir}. Run `python -m ml.train` first."
            )

        try:
            self._pipeline = joblib.load(model_path)
            self._label_encoder = joblib.load(encoder_path)
            if metrics_path.exists():
                self._metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise ModelLoadError(f"Failed to load ML artifacts: {exc}") from exc

    def ensure_loaded(self) -> None:
        if self._pipeline is None or self._label_encoder is None:
            self.load()

    @property
    def is_loaded(self) -> bool:
        return self._pipeline is not None and self._label_encoder is not None

    def get_metrics(self) -> dict[str, Any] | None:
        if self._metrics is None:
            metrics_path = self.artifacts_dir / "model_metrics.json"
            if metrics_path.exists():
                self._metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        return self._metrics

    def predict_probabilities(
        self,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        temperature: float,
        humidity: float,
        ph: float,
        rainfall: float,
    ) -> list[CropPrediction]:
        """Return all crop class probabilities sorted descending."""
        self.ensure_loaded()

        row = pd.DataFrame(
            [
                {
                    "N": float(nitrogen),
                    "P": float(phosphorus),
                    "K": float(potassium),
                    "temperature": float(temperature),
                    "humidity": float(humidity),
                    "ph": float(ph),
                    "rainfall": float(rainfall),
                }
            ],
            columns=FEATURE_COLUMNS,
        )

        probs = self._pipeline.predict_proba(row)[0]
        classes = self._label_encoder.inverse_transform(range(len(probs)))
        predictions = [
            CropPrediction(crop_key=str(crop).strip().lower(), probability=float(prob))
            for crop, prob in zip(classes, probs)
        ]
        predictions.sort(key=lambda item: item.probability, reverse=True)
        return predictions
