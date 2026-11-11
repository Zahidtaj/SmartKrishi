"""Configuration constants for the SmartKrishi ML pipeline."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "datasets" / "raw" / "crop_recommendation.csv"
VALIDATION_REPORT_PATH = PROJECT_ROOT / "datasets" / "processed" / "dataset_validation_report.json"
PROVENANCE_PATH = PROJECT_ROOT / "datasets" / "metadata" / "crop_recommendation_provenance.json"
ARTIFACTS_DIR = PROJECT_ROOT / "ml" / "artifacts"

FEATURE_COLUMNS = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
TARGET_COLUMN = "label"

FEATURE_BOUNDS = {
    "N": (0.0, 300.0),
    "P": (0.0, 300.0),
    "K": (0.0, 400.0),
    "temperature": (-5.0, 60.0),
    "humidity": (0.0, 100.0),
    "ph": (0.0, 14.0),
    "rainfall": (0.0, 5000.0),
}

RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5
