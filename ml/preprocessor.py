"""Data preprocessing module enforcing split-before-fit to prevent data leakage."""

from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from ml.config import FEATURE_COLUMNS, RANDOM_STATE, TARGET_COLUMN, TEST_SIZE


@dataclass
class SplitDatasets:
    X_train_raw: pd.DataFrame
    X_test_raw: pd.DataFrame
    X_train_scaled: np.ndarray
    X_test_scaled: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray
    scaler: StandardScaler
    label_encoder: LabelEncoder
    feature_names: list[str]
    class_names: list[str]


def split_and_preprocess(
    df: pd.DataFrame,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
) -> SplitDatasets:
    """
    Perform stratified train/test split FIRST, then fit scaler and label encoder on training split only.
    """
    X = df[FEATURE_COLUMNS].copy()
    y_raw = df[TARGET_COLUMN].copy()

    X_train, X_test, y_train_raw, y_test_raw = train_test_split(
        X,
        y_raw,
        test_size=test_size,
        random_state=random_state,
        stratify=y_raw,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(y_train_raw)
    y_test = label_encoder.transform(y_test_raw)

    return SplitDatasets(
        X_train_raw=X_train.reset_index(drop=True),
        X_test_raw=X_test.reset_index(drop=True),
        X_train_scaled=X_train_scaled,
        X_test_scaled=X_test_scaled,
        y_train=y_train,
        y_test=y_test,
        scaler=scaler,
        label_encoder=label_encoder,
        feature_names=list(FEATURE_COLUMNS),
        class_names=[str(c) for c in label_encoder.classes_],
    )
