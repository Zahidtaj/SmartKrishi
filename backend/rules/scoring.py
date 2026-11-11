"""Configurable prototype suitability scoring weights and normalization helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoringWeights:
    """Configurable illustrative scoring weights (sum = 1.00)."""
    location: float = 0.20
    soil: float = 0.20
    water: float = 0.20
    seasonal: float = 0.15
    climatic: float = 0.15
    nutrient: float = 0.10


DEFAULT_WEIGHTS = ScoringWeights()

ML_BLEND_FACTOR = 0.20  # Bounded ML influence; agronomic rules govern 80% + hard constraints.


def range_proximity_score(value: float | None, low: float, high: float, tolerance: float) -> float:
    """
    Score 0.0-1.0 based on whether `value` lies inside [low, high] or smoothly decays within `tolerance`.
    Returns 0.50 when `value` is None (missing measurement).
    """
    if value is None:
        return 0.50
    if low <= value <= high:
        return 1.0
    distance = (low - value) if value < low else (value - high)
    if tolerance <= 0:
        return 0.0
    return max(0.0, round(1.0 - (distance / tolerance), 4))


def classify_suitability(score_pct: float, conflict_flags: list[str], reduced_info: bool) -> str:
    """Map illustrative percentage score and conflicts into human-readable suitability categories."""
    if conflict_flags:
        if score_pct >= 55.0:
            return "Conditionally Suitable (Verify Constraints)"
        return "Low Suitability (Constraint Conflicts)"
    if reduced_info:
        if score_pct >= 72.0:
            return "Provisional Match (Limited Soil/Climate Data)"
        return "Moderate Provisional Match"
    if score_pct >= 80.0:
        return "Highly Suitable (Prototype Match)"
    if score_pct >= 62.0:
        return "Suitable (Prototype Match)"
    return "Moderately Suitable"
