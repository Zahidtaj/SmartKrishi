"""Configurable agricultural rule engine evaluating region, soil, pH, NPK, season, water, and climate."""

from dataclasses import dataclass
from typing import Any

from backend.models import Crop, Location, RegionalCropRule
from backend.rules.scoring import (
    DEFAULT_WEIGHTS,
    ML_BLEND_FACTOR,
    ScoringWeights,
    classify_suitability,
    range_proximity_score,
)


@dataclass
class EvaluatedCropCandidate:
    crop: Crop
    hard_excluded: bool
    exclusion_reason_en: str | None
    exclusion_reason_kn: str | None
    illustrative_score: float
    suitability_category: str
    ml_probability: float | None
    dimension_scores: dict[str, float]
    reasons_en: list[str]
    reasons_kn: list[str]
    limitations_en: list[str]
    limitations_kn: list[str]
    conflict_flags: list[str]


def _water_level_rank(water_availability: str) -> int:
    mapping = {
        "Rainfed": 1,
        "Limited irrigation": 2,
        "Moderate irrigation": 3,
        "Assured irrigation": 4,
    }
    return mapping.get(water_availability, 1)


def evaluate_crop_against_rules(
    crop: Crop,
    location: Location | None,
    rules: list[RegionalCropRule],
    inputs: dict[str, Any],
    ml_probability: float | None,
    reduced_info: bool,
    weights: ScoringWeights = DEFAULT_WEIGHTS,
) -> EvaluatedCropCandidate:
    """Evaluate a single crop against documented agronomic rules and hard constraints."""
    req = crop.requirement
    if req is None:
        return EvaluatedCropCandidate(
            crop=crop,
            hard_excluded=True,
            exclusion_reason_en="Agronomic requirement profile missing.",
            exclusion_reason_kn="ಬೆಳೆ ಅಗತ್ಯ ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ.",
            illustrative_score=0.0,
            suitability_category="Unavailable",
            ml_probability=ml_probability,
            dimension_scores={},
            reasons_en=[],
            reasons_kn=[],
            limitations_en=[],
            limitations_kn=[],
            conflict_flags=["missing_profile"],
        )

    reasons_en: list[str] = []
    reasons_kn: list[str] = []
    limitations_en: list[str] = []
    limitations_kn: list[str] = []
    conflict_flags: list[str] = []

    state = inputs["state"]
    season = inputs["season"]
    soil_type = inputs["soil_type"]
    water_avail = inputs["water_availability"]
    ph = inputs.get("ph")
    n_val = inputs.get("nitrogen")
    p_val = inputs.get("phosphorus")
    k_val = inputs.get("potassium")
    temp = inputs.get("temperature")
    humidity = inputs.get("humidity")
    rainfall = inputs.get("rainfall")

    # 1. Regional Rule Evaluation (hard guard against non-Karnataka/restricted crops)
    zone_code = location.zone_code if location else None
    active_rules = [r for r in rules if r.is_active and r.state.lower() == state.lower()]
    restricted_rules = [r for r in active_rules if r.suitability_level == "restricted"]
    if restricted_rules and not [r for r in active_rules if r.suitability_level != "restricted"]:
        return EvaluatedCropCandidate(
            crop=crop,
            hard_excluded=True,
            exclusion_reason_en=restricted_rules[0].rule_notes_en,
            exclusion_reason_kn=restricted_rules[0].rule_notes_kn,
            illustrative_score=0.0,
            suitability_category="Regionally Restricted",
            ml_probability=ml_probability,
            dimension_scores={},
            reasons_en=[],
            reasons_kn=[],
            limitations_en=[restricted_rules[0].rule_notes_en],
            limitations_kn=[restricted_rules[0].rule_notes_kn],
            conflict_flags=["region_restricted"],
        )

    zone_season_matches = [
        r for r in active_rules
        if (r.agro_climatic_zone is None or r.agro_climatic_zone == zone_code)
        and r.season == season
        and r.suitability_level in ("recommended", "conditional")
    ]
    zone_any_season = [
        r for r in active_rules
        if (r.agro_climatic_zone is None or r.agro_climatic_zone == zone_code)
        and r.suitability_level in ("recommended", "conditional")
    ]

    if zone_season_matches:
        location_score = 1.0
        reasons_en.append(
            f"Documented for {location.agro_climatic_zone if location else state} ({zone_code or state}) in {season}."
        )
        reasons_kn.append(
            f"{location.agro_climatic_zone if location else state} ವಲಯದ {season} ಹಂಗಾಮಿಗೆ ದಾಖಲಿತ ಬೆಳೆಯಾಗಿದೆ."
        )
    elif zone_any_season:
        location_score = 0.60
    else:
        location_score = 0.25
        conflict_flags.append("zone_unverified")
        limitations_en.append(
            f"Not listed as a primary zone crop for {zone_code or state}; confirm adaptability with local KVK/RSK."
        )
        limitations_kn.append(
            f"ಈ ಕೃಷಿ-ಹವಾಮಾನ ವಲಯಕ್ಕೆ ಪ್ರಮುಖ ಬೆಳೆಯಾಗಿ ದಾಖಲಾಗಿಲ್ಲ; ಸ್ಥಳೀಯ ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರದಲ್ಲಿ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ."
        )

    # 2. Season Compatibility (Hard exclusion for incompatible non-perennial seasonal crops)
    if season in req.suitable_seasons:
        seasonal_score = 1.0
        reasons_en.append(f"Compatible with {season} sowing season.")
        reasons_kn.append(f"{season} ಬಿತ್ತನೆ ಹಂಗಾಮಿಗೆ ಸೂಕ್ತವಾಗಿದೆ.")
    elif "Perennial" in req.suitable_seasons and season in ("Kharif", "Rabi"):
        seasonal_score = 0.70
        limitations_en.append(
            f"{crop.name_en} is a multi-season/perennial crop ({crop.growing_duration_days_min}-{crop.growing_duration_days_max} days)."
        )
        limitations_kn.append(
            f"{crop.name_kn} ಬಹುವಾರ್ಷಿಕ/ದೀರ್ಘಾವಧಿ ಬೆಳೆಯಾಗಿದೆ ({crop.growing_duration_days_min}-{crop.growing_duration_days_max} ದಿನಗಳು)."
        )
    else:
        return EvaluatedCropCandidate(
            crop=crop,
            hard_excluded=True,
            exclusion_reason_en=f"Season mismatch: {crop.name_en} is documented for {', '.join(req.suitable_seasons)}, not {season}.",
            exclusion_reason_kn=f"ಹಂಗಾಮು ಹೊಂದಿಕೆಯಾಗುತ್ತಿಲ್ಲ: {crop.name_kn} ಬೆಳೆಗೆ {', '.join(req.suitable_seasons)} ಹಂಗಾಮು ಸೂಕ್ತ.",
            illustrative_score=0.0,
            suitability_category="Season Mismatch",
            ml_probability=ml_probability,
            dimension_scores={},
            reasons_en=[],
            reasons_kn=[],
            limitations_en=[],
            limitations_kn=[],
            conflict_flags=["season_mismatch"],
        )

    # 3. Water Availability Compatibility (Hard exclusion if high-water crop under rainfed dry conditions)
    supported_water = req.supported_water_levels
    user_water_rank = _water_level_rank(water_avail)
    min_req_rank = min(_water_level_rank(w) for w in supported_water) if supported_water else 1
    eff_rainfall = rainfall if rainfall is not None else (location.normal_annual_rainfall_mm if location else None)

    if water_avail in supported_water:
        water_score = 1.0
        reasons_en.append(
            f"Water demand ({crop.water_requirement_level}: {crop.water_requirement_mm_min}-{crop.water_requirement_mm_max} mm) matches {water_avail.lower()}."
        )
        reasons_kn.append(
            f"ನೀರಿನ ಅಗತ್ಯ ({crop.water_requirement_mm_min}-{crop.water_requirement_mm_max} ಮಿ.ಮೀ) ಲಭ್ಯವಿರುವ {water_avail} ಸ್ಥಿತಿಗೆ ಹೊಂದುತ್ತದೆ."
        )
    elif water_avail == "Rainfed" and eff_rainfall is not None and eff_rainfall >= 1500 and crop.water_requirement_level != "High":
        water_score = 0.75
    elif user_water_rank < min_req_rank:
        # High-water crops like Sugarcane, Banana, Rice in Rainfed dryland cannot override water deficit
        if crop.water_requirement_level == "High" and water_avail in ("Rainfed", "Limited irrigation"):
            # Allow Rainfed rice ONLY in heavy rainfall Coastal/Malnad zones (>1400mm)
            if crop.crop_key == "rice" and zone_code in ("KA-Z9", "KA-Z10") and (eff_rainfall or 0) >= 1400 and water_avail == "Rainfed":
                water_score = 0.75
                limitations_en.append("Rainfed paddy depends strictly on timely high monsoon rainfall in coastal/malnad belts.")
                limitations_kn.append("ಮಳೆಯಾಶ್ರಿತ ಭತ್ತವು ಮಲೆನಾಡು/ಕರಾವಳಿಯ ಸಮಯೋಚಿತ ಭಾರಿ ಮಳೆಯನ್ನು ಅವಲಂಬಿಸಿದೆ.")
            else:
                return EvaluatedCropCandidate(
                    crop=crop,
                    hard_excluded=True,
                    exclusion_reason_en=f"Water constraint: {crop.name_en} requires {', '.join(supported_water)}, incompatible with {water_avail}.",
                    exclusion_reason_kn=f"ನೀರಿನ ಕೊರತೆ: {crop.name_kn} ಬೆಳೆಗೆ {', '.join(supported_water)} ಅಗತ್ಯವಿದ್ದು, {water_avail} ಸ್ಥಿತಿಗೆ ಸೂಕ್ತವಲ್ಲ.",
                    illustrative_score=0.0,
                    suitability_category="Water Deficit Conflict",
                    ml_probability=ml_probability,
                    dimension_scores={},
                    reasons_en=[],
                    reasons_kn=[],
                    limitations_en=[],
                    limitations_kn=[],
                    conflict_flags=["water_deficit"],
                )
        water_score = 0.40
        conflict_flags.append("water_caution")
        limitations_en.append(
            f"Requires {', '.join(supported_water)}; {water_avail} may cause moisture stress during critical stages."
        )
        limitations_kn.append(
            f"{crop.name_kn} ಬೆಳೆಗೆ {', '.join(supported_water)} ಅಗತ್ಯವಿದೆ; ಪ್ರಸ್ತುತ ನೀರಿನ ಲಭ್ಯತೆಯಲ್ಲಿ ತೇವಾಂಶ ಕೊರತೆಯಾಗಬಹುದು."
        )
    else:
        water_score = 0.85

    # 4. Soil Type + Soil pH Compatibility
    soil_type_score = 1.0 if soil_type in req.suitable_soil_types else (0.65 if "Loamy" in req.suitable_soil_types and soil_type in ("Red", "Alluvial") else 0.30)
    if soil_type in req.suitable_soil_types:
        reasons_en.append(f"{soil_type} soil matches documented soil texture suitability.")
        reasons_kn.append(f"{soil_type} ಮಣ್ಣು ಈ ಬೆಳೆಗೆ ಪೂರಕವಾಗಿದೆ.")
    else:
        limitations_en.append(
            f"{soil_type} soil is outside preferred textures ({', '.join(req.suitable_soil_types)}); drainage or tilth management may be needed."
        )
        limitations_kn.append(
            f"{soil_type} ಮಣ್ಣು ಆದ್ಯತೆಯ ಮಣ್ಣಿನ ವರ್ಗದಲ್ಲಿಲ್ಲ ({', '.join(req.suitable_soil_types)}); ಮಣ್ಣು ಸುಧಾರಣೆ ಅಗತ್ಯವಾಗಬಹುದು."
        )

    if ph is not None:
        if req.ph_optimal_min <= ph <= req.ph_optimal_max:
            ph_score = 1.0
            reasons_en.append(f"Soil pH {ph:.1f} is in optimal range ({req.ph_optimal_min:.1f}-{req.ph_optimal_max:.1f}).")
            reasons_kn.append(f"ಮಣ್ಣಿನ ಪಿಎಚ್ {ph:.1f} ಉತ್ತಮ ವ್ಯಾಪ್ತಿಯಲ್ಲಿದೆ ({req.ph_optimal_min:.1f}-{req.ph_optimal_max:.1f}).")
        elif req.ph_min <= ph <= req.ph_max:
            ph_score = 0.72
            reasons_en.append(f"Soil pH {ph:.1f} is within tolerable bounds ({req.ph_min:.1f}-{req.ph_max:.1f}).")
            reasons_kn.append(f"ಮಣ್ಣಿನ ಪಿಎಚ್ {ph:.1f} ಸಹನೀಯ ವ್ಯಾಪ್ತಿಯಲ್ಲಿದೆ.")
        else:
            ph_score = 0.15
            conflict_flags.append("ph_out_of_range")
            limitations_en.append(
                f"Soil pH {ph:.1f} falls outside tolerated range ({req.ph_min:.1f}-{req.ph_max:.1f}); soil amendment verification required."
            )
            limitations_kn.append(
                f"ಮಣ್ಣಿನ ಪಿಎಚ್ {ph:.1f} ಸೂಕ್ತ ವ್ಯಾಪ್ತಿಯಿಂದ ({req.ph_min:.1f}-{req.ph_max:.1f}) ಹೊರಗಿದೆ; ಮಣ್ಣು ಸುಧಾರಣೆ ಅಗತ್ಯ."
            )
    else:
        ph_score = 0.50
        limitations_en.append("Soil pH was not provided; pH compatibility could not be verified.")
        limitations_kn.append("ಮಣ್ಣಿನ ಪಿಎಚ್ ಮೌಲ್ಯ ನೀಡದ ಕಾರಣ ಆಮ್ಲೀಯತೆ ಹೊಂದಾಣಿಕೆ ಪರಿಶೀಲಿಸಲಾಗಿಲ್ಲ.")

    soil_score = round((soil_type_score * 0.55) + (ph_score * 0.45), 4)

    # 5. Nutrient (NPK) Compatibility
    n_score = range_proximity_score(n_val, req.nitrogen_min, req.nitrogen_max, tolerance=45.0)
    p_score = range_proximity_score(p_val, req.phosphorus_min, req.phosphorus_max, tolerance=35.0)
    k_score = range_proximity_score(k_val, req.potassium_min, req.potassium_max, tolerance=35.0)
    nutrient_score = round((n_score + p_score + k_score) / 3.0, 4)

    if n_val is not None and p_val is not None and k_val is not None:
        if nutrient_score >= 0.75:
            reasons_en.append(f"Available NPK ({n_val:.0f}/{p_val:.0f}/{k_val:.0f} kg/ha) aligns well with crop demand.")
            reasons_kn.append(f"ಲಭ್ಯವಿರುವ ಎನ್.ಪಿ.ಕೆ ({n_val:.0f}/{p_val:.0f}/{k_val:.0f} ಕೆಜಿ/ಹೆ) ಬೆಳೆಯ ಬೇಡಿಕೆಗೆ ಹೊಂದಿಕೆಯಾಗುತ್ತದೆ.")
        elif nutrient_score < 0.50:
            limitations_en.append("Entered NPK values deviate notably from standard crop nutrient bands; plan balanced fertilization via Soil Health Card.")
            limitations_kn.append("ನೀಡಿದ ಎನ್.ಪಿ.ಕೆ ಮೌಲ್ಯಗಳು ಬೆಳೆಯ ಪ್ರಮಾಣಿತ ಪೋಷಕಾಂಶ ವ್ಯಾಪ್ತಿಗಿಂತ ಭಿನ್ನವಾಗಿವೆ.")
    else:
        limitations_en.append("Full soil NPK test values were not supplied; nutrient suitability is provisional.")
        limitations_kn.append("ಸಂಪೂರ್ಣ ಎನ್.ಪಿ.ಕೆ ಮಣ್ಣು ಪರೀಕ್ಷೆ ಮೌಲ್ಯಗಳಿಲ್ಲದ ಕಾರಣ ಪೋಷಕಾಂಶ ಹೊಂದಾಣಿಕೆ ತಾತ್ಕಾಲಿಕವಾಗಿದೆ.")

    # 6. Climatic Compatibility (Temperature, Humidity, Rainfall)
    t_score = range_proximity_score(temp, req.temp_min_c, req.temp_max_c, tolerance=7.0)
    h_score = range_proximity_score(humidity, req.humidity_min_pct, req.humidity_max_pct, tolerance=20.0)
    r_score = range_proximity_score(eff_rainfall, req.rainfall_min_mm, req.rainfall_max_mm, tolerance=400.0)
    climatic_score = round((t_score * 0.40) + (h_score * 0.25) + (r_score * 0.35), 4)

    if temp is not None and (temp < req.temp_min_c - 6 or temp > req.temp_max_c + 6):
        conflict_flags.append("temperature_extreme")
        limitations_en.append(
            f"Temperature {temp:.1f}°C is outside documented crop range ({req.temp_min_c:.0f}-{req.temp_max_c:.0f}°C)."
        )
        limitations_kn.append(
            f"ತಾಪಮಾನ {temp:.1f}°C ಈ ಬೆಳೆಯ ಸೂಕ್ತ ವ್ಯಾಪ್ತಿಯಿಂದ ({req.temp_min_c:.0f}-{req.temp_max_c:.0f}°C) ಹೊರಗಿದೆ."
        )
    elif temp is not None and t_score >= 0.8:
        reasons_en.append(f"Ambient temperature ({temp:.1f}°C) suits documented crop thermal range.")
        reasons_kn.append(f"ತಾಪಮಾನ ({temp:.1f}°C) ಈ ಬೆಳೆಯ ಬೆಳವಣಿಗೆಗೆ ಅನುಕೂಲಕರವಾಗಿದೆ.")

    if rainfall is None and location and location.normal_annual_rainfall_mm is not None:
        limitations_en.append(
            f"Seasonal rainfall not entered; evaluated using taluk reference annual normal ({location.normal_annual_rainfall_mm:.0f} mm/yr)."
        )
        limitations_kn.append(
            f"ಮಳೆ ಪ್ರಮಾಣ ನೀಡದ ಕಾರಣ ತಾಲ್ಲೂಕಿನ ವಾರ್ಷಿಕ ಸರಾಸರಿ ಮಳೆ ({location.normal_annual_rainfall_mm:.0f} ಮಿ.ಮೀ) ಉಲ್ಲೇಖಿಸಲಾಗಿದೆ."
        )

    # Composite Rule Score (0-100)
    rule_composite = (
        location_score * weights.location
        + soil_score * weights.soil
        + water_score * weights.water
        + seasonal_score * weights.seasonal
        + climatic_score * weights.climatic
        + nutrient_score * weights.nutrient
    )

    # Blend ML probability ONLY for crops present in the ML dataset and when full/climate+soil features exist,
    # keeping ML bounded so it never overrides hard agronomic constraints.
    if crop.in_ml_dataset and ml_probability is not None and not reduced_info:
        blended = (rule_composite * (1.0 - ML_BLEND_FACTOR)) + (ml_probability * ML_BLEND_FACTOR)
        if ml_probability >= 0.15:
            reasons_en.append(f"Random Forest pattern alignment: {ml_probability * 100:.1f}% relative class probability.")
            reasons_kn.append(f"ಎಂಎಲ್ ಮಾದರಿ ಪೂರಕತೆ: {ml_probability * 100:.1f}% ಸಾಪೇಕ್ಷ ಸಂಭವನೀಯತೆ.")
    else:
        blended = rule_composite
        if not crop.in_ml_dataset:
            limitations_en.append(
                "Evaluated by Karnataka agronomic rules (this regional staple is outside the 22-crop public ML CSV)."
            )
            limitations_kn.append(
                "ಕರ್ನಾಟಕ ಕೃಷಿ ನಿಯಮಗಳ ಆಧಾರದ ಮೇಲೆ ಮೌಲ್ಯಮಾಪನ ಮಾಡಲಾಗಿದೆ (22 ಬೆಳೆಗಳ ಎಂಎಲ್ ದತ್ತಾಂಶದ ಹೊರಗಿನ ಸ್ಥಳೀಯ ಬೆಳೆ)."
            )

    if conflict_flags:
        blended = min(blended, 0.64)

    illustrative_score = round(max(0.0, min(100.0, blended * 100.0)), 1)

    if not limitations_en:
        limitations_en.append("Verify local pest incidence, seed variety availability, and market demand before sowing.")
        limitations_kn.append("ಬಿತ್ತನೆಗೆ ಮುನ್ನ ಸ್ಥಳೀಯ ಕೀಟ ಬಾಧೆ, ಬೀಜ ಲಭ್ಯತೆ ಮತ್ತು ಮಾರುಕಟ್ಟೆ ಬೇಡಿಕೆ ಪರಿಶೀಲಿಸಿ.")

    suitability_category = classify_suitability(illustrative_score, conflict_flags, reduced_info)

    return EvaluatedCropCandidate(
        crop=crop,
        hard_excluded=False,
        exclusion_reason_en=None,
        exclusion_reason_kn=None,
        illustrative_score=illustrative_score,
        suitability_category=suitability_category,
        ml_probability=round(ml_probability, 4) if ml_probability is not None else None,
        dimension_scores={
            "location": round(location_score * 100.0, 1),
            "soil": round(soil_score * 100.0, 1),
            "water": round(water_score * 100.0, 1),
            "seasonal": round(seasonal_score * 100.0, 1),
            "climatic": round(climatic_score * 100.0, 1),
            "nutrient": round(nutrient_score * 100.0, 1),
        },
        reasons_en=reasons_en,
        reasons_kn=reasons_kn,
        limitations_en=limitations_en,
        limitations_kn=limitations_kn,
        conflict_flags=conflict_flags,
    )
