"""Transparent weighted suitability scoring for observation-based recommendations."""

from backend.rules.agronomic_rules import RuleEvaluation

OBSERVATION_WEIGHTS = {
    "location": 0.20,
    "soil_land": 0.25,
    "water": 0.25,
    "seasonal": 0.15,
    "climate": 0.08,
    "priority_history": 0.07,
}


def compute_observation_score(ev: RuleEvaluation) -> tuple[float, str, dict[str, float]]:
    """Compute bounded illustrative suitability score (0-100) and transparent category."""
    dims = {
        "location": round(ev.location_score, 2),
        "soil_land": round(ev.soil_land_score, 2),
        "water": round(ev.water_score, 2),
        "seasonal": round(ev.seasonal_score, 2),
        "climate": round(ev.climate_score, 2),
        "priority_history": round(ev.priority_score, 2),
    }

    if ev.hard_rejected:
        return 0.0, "Not Recommended", dims

    raw = (
        dims["location"] * OBSERVATION_WEIGHTS["location"]
        + dims["soil_land"] * OBSERVATION_WEIGHTS["soil_land"]
        + dims["water"] * OBSERVATION_WEIGHTS["water"]
        + dims["seasonal"] * OBSERVATION_WEIGHTS["seasonal"]
        + dims["climate"] * OBSERVATION_WEIGHTS["climate"]
        + dims["priority_history"] * OBSERVATION_WEIGHTS["priority_history"]
    )

    # Guardrail caps for critical physical/water conflicts
    if "severe_water_shortage" in ev.conflict_flags:
        raw = min(raw, 42.0)
    if "waterlogging_risk" in ev.conflict_flags:
        raw = min(raw, 54.0)
    if "rocky_stony_root_limit" in ev.conflict_flags:
        raw = min(raw, 52.0)
    if "insufficient_assured_water" in ev.conflict_flags:
        raw = min(raw, 56.0)
    if "slope_erosion_risk" in ev.conflict_flags:
        raw = min(raw, 58.0)

    final_score = round(max(5.0, min(100.0, raw)), 2)

    if final_score >= 76.0 and not any(
        f in ev.conflict_flags for f in ("severe_water_shortage", "waterlogging_risk", "rocky_stony_root_limit")
    ):
        category = "Highly Suitable (Prototype Fit)"
    elif final_score >= 60.0:
        category = "Suitable with Precautions"
    elif final_score >= 45.0:
        category = "Marginally Suitable (Caution)"
    else:
        category = "Not Recommended"

    return final_score, category, dims
