"""Dataset loading module for SmartKrishi ML pipeline."""

from pathlib import Path
import pandas as pd

from ml.config import DATASET_PATH, FEATURE_COLUMNS, TARGET_COLUMN


def load_crop_dataset(dataset_path: Path | str | None = None) -> pd.DataFrame:
    """Load the raw crop recommendation CSV dataset and verify required columns."""
    path = Path(dataset_path) if dataset_path is not None else DATASET_PATH
    if not path.exists():
        raise FileNotFoundError(f"Crop dataset not found at {path}")

    df = pd.read_csv(path)
    expected_columns = set(FEATURE_COLUMNS + [TARGET_COLUMN])
    missing_columns = expected_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing_columns)}")

    return df
