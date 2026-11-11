"""Dataset validation module for SmartKrishi ML pipeline."""

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import pandas as pd

from ml.config import FEATURE_BOUNDS, FEATURE_COLUMNS, TARGET_COLUMN, VALIDATION_REPORT_PATH


@dataclass
class ValidationReport:
    total_rows: int
    valid_rows: int
    dropped_rows: int
    duplicate_rows: int
    missing_values_by_column: dict[str, int]
    out_of_range_by_column: dict[str, int]
    unique_labels: list[str]
    label_counts: dict[str, int]
    passed: bool
    notes: list[str]


def validate_crop_dataset(
    df: pd.DataFrame,
    save_report_path: Path | str | None = VALIDATION_REPORT_PATH,
) -> tuple[pd.DataFrame, ValidationReport]:
    """
    Validate schema, missing/NULL values, duplicates, and domain bounds.

    Returns the cleaned DataFrame (dropping only rows missing target or violating hard domain bounds)
    and a detailed ValidationReport documenting what was checked.
    """
    working = df.copy()
    total_rows = len(working)
    notes: list[str] = []

    missing_values_by_column = {
        col: int(working[col].isna().sum()) for col in FEATURE_COLUMNS + [TARGET_COLUMN]
    }
    total_missing = sum(missing_values_by_column.values())
    if total_missing == 0:
        notes.append("Zero missing/NULL values detected across all feature and target columns.")
    else:
        notes.append(
            f"Detected {total_missing} missing/NULL cells; rows missing target or features are dropped before splitting."
        )
        working = working.dropna(subset=FEATURE_COLUMNS + [TARGET_COLUMN])

    for col in FEATURE_COLUMNS:
        working[col] = pd.to_numeric(working[col], errors="coerce")
    coerced_missing = int(working[FEATURE_COLUMNS].isna().sum().sum())
    if coerced_missing > 0:
        notes.append(f"Dropped {coerced_missing} non-numeric cells coerced to NaN.")
        working = working.dropna(subset=FEATURE_COLUMNS)

    working[TARGET_COLUMN] = working[TARGET_COLUMN].astype(str).str.strip().str.lower()

    out_of_range_by_column: dict[str, int] = {}
    valid_mask = pd.Series(True, index=working.index)
    for col, (low, high) in FEATURE_BOUNDS.items():
        col_bad = (working[col] < low) | (working[col] > high)
        out_of_range_by_column[col] = int(col_bad.sum())
        valid_mask &= ~col_bad

    invalid_range_count = int((~valid_mask).sum())
    if invalid_range_count > 0:
        notes.append(f"Dropped {invalid_range_count} rows outside agronomic domain bounds.")
        working = working.loc[valid_mask].copy()
    else:
        notes.append("All records fall within documented physical/agronomic domain bounds.")

    duplicate_rows = int(working.duplicated().sum())
    if duplicate_rows > 0:
        notes.append(f"Found {duplicate_rows} exact duplicate rows; keeping intact or deduplicate if needed.")
    else:
        notes.append("Zero exact duplicate rows detected.")

    label_series = working[TARGET_COLUMN].value_counts().sort_index()
    label_counts = {str(k): int(v) for k, v in label_series.items()}
    unique_labels = sorted(label_counts.keys())

    report = ValidationReport(
        total_rows=total_rows,
        valid_rows=len(working),
        dropped_rows=total_rows - len(working),
        duplicate_rows=duplicate_rows,
        missing_values_by_column=missing_values_by_column,
        out_of_range_by_column=out_of_range_by_column,
        unique_labels=unique_labels,
        label_counts=label_counts,
        passed=len(working) > 0 and len(unique_labels) >= 2,
        notes=notes,
    )

    if save_report_path is not None:
        report_path = Path(save_report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")

    return working.reset_index(drop=True), report
