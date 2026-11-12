"""Transparent observation-based agronomic compatibility rules and explanations."""

from dataclasses import dataclass, field
from typing import Any

from backend.models import Crop, CropRequirement, Location, RegionalCropRule


@dataclass
class EvaluationContext:
    location: Location
    season: str
    soil_color: str
    soil_texture: str
    drainage_after_rain: str
    moisture_retention: str
    soil_depth: str
    visible_stones: str
    waterlogging_issue: str
    erosion_issue: str
    land_topography: str
    water_source: str
    water_reliability: str
    intended_sowing_month: str | None
    duration_preference: str
    farming_priority: str
    previous_crop: str | None
    previous_crop_success: str | None
    drought_history: str | None
    flood_history: str | None
    pest_disease_history: str | None
    soil_observation: dict[str, Any]
    weather_intel: dict[str, Any]


@dataclass
class RuleEvaluation:
    crop: Crop
    hard_rejected: bool
    rejection_reasons_en: list[str] = field(default_factory=list)
    rejection_reasons_kn: list[str] = field(default_factory=list)
    location_score: float = 0.0
    soil_land_score: float = 0.0
    water_score: float = 0.0
    seasonal_score: float = 0.0
    climate_score: float = 0.0
    priority_score: float = 0.0
    reasons_en: list[str] = field(default_factory=list)
    reasons_kn: list[str] = field(default_factory=list)
    limitations_en: list[str] = field(default_factory=list)
    limitations_kn: list[str] = field(default_factory=list)
    missing_info_en: list[str] = field(default_factory=list)
    missing_info_kn: list[str] = field(default_factory=list)
    conflict_flags: list[str] = field(default_factory=list)
    compatibility_badges: dict[str, str] = field(default_factory=dict)


DEPTH_RANK = {"shallow": 1, "medium": 2, "deep": 3}

SOIL_COLOR_TO_BROAD_GROUPS: dict[str, set[str]] = {
    "red": {"Red", "Loamy", "Laterite", "Sandy"},
    "reddish_brown": {"Red", "Laterite", "Loamy", "Alluvial"},
    "dark_black": {"Black", "Clay"},
    "brown": {"Loamy", "Alluvial", "Black", "Red"},
    "yellowish": {"Red", "Laterite", "Sandy", "Loamy"},
    "grey": {"Clay", "Alluvial", "Black"},
    "sandy_pale": {"Sandy", "Alluvial", "Red"},
    "mixed_uncertain": set(),
}


def _effective_water_tier(ctx: EvaluationContext) -> str:
    """Derive effective moisture/irrigation regime from source, reliability, and zone rainfall."""
    annual_rain = ctx.location.normal_annual_rainfall_mm or 700.0
    if ctx.water_source == "rainfed":
        if annual_rain >= 2000.0 and ctx.season in ("Kharif", "Perennial"):
            return "rainfed_humid"
        return "rainfed_scarce" if ctx.water_reliability == "limited" or annual_rain < 650.0 else "rainfed_normal"
    if ctx.water_reliability == "throughout_season":
        return "assured"
    if ctx.water_reliability == "certain_months":
        return "moderate"
    if ctx.water_reliability == "limited":
        return "limited"
    return "uncertain"


def _effective_drainage(ctx: EvaluationContext) -> str:
    return str(ctx.soil_observation.get("effective_drainage", "unknown"))


def evaluate_crop_observation_rules(
    crop: Crop,
    req: CropRequirement,
    rules: list[RegionalCropRule],
    ctx: EvaluationContext,
) -> RuleEvaluation:
    """Evaluate a crop across all 7 transparent agronomic rule stages."""
    ev = RuleEvaluation(crop=crop, hard_rejected=False)
    badges: dict[str, str] = {}

    # =========================================================================
    # STAGE 1: Regional & Agro-Climatic Zone Compatibility
    # =========================================================================
    restricted_rules = [r for r in rules if r.suitability_level == "restricted"]
    zone_season_rules = [
        r for r in rules
        if r.agro_climatic_zone == ctx.location.zone_code
        and r.season == ctx.season
        and r.suitability_level == "recommended"
    ]
    zone_any_rules = [
        r for r in rules
        if r.agro_climatic_zone == ctx.location.zone_code
        and r.suitability_level in ("recommended", "conditional")
    ]

    if restricted_rules and not zone_any_rules:
        ev.hard_rejected = True
        ev.rejection_reasons_en.append(
            f"{crop.name_en} is outside verified Karnataka agro-climatic cultivation zones."
        )
        ev.rejection_reasons_kn.append(
            f"{crop.name_kn} ಕರ್ನಾಟಕದ ಪ್ರಮಾಣಿತ ಕೃಷಿ-ಹವಾಮಾನ ವಲಯಗಳಿಗೆ ಸೂಕ್ತವಲ್ಲ."
        )
        ev.conflict_flags.append("outside_karnataka_zone")
        badges["region"] = "not_suited"
        ev.compatibility_badges = badges
        return ev

    if zone_season_rules:
        ev.location_score = 100.0
        badges["region"] = "recommended"
        ev.reasons_en.append(
            f"Documented crop in {ctx.location.agro_climatic_zone} ({ctx.location.zone_code}) for {ctx.season} season."
        )
        ev.reasons_kn.append(
            f"{ctx.location.agro_climatic_zone} ({ctx.location.zone_code}) ವಲಯದಲ್ಲಿ {ctx.season} ಹಂಗಾಮಿಗೆ ಪ್ರಮಾಣಿತ ಬೆಳೆ."
        )
    elif zone_any_rules:
        ev.location_score = 62.0
        badges["region"] = "conditional"
        ev.limitations_en.append(
            f"Grown in {ctx.location.agro_climatic_zone}, though {ctx.season} is not its primary documented window."
        )
        ev.limitations_kn.append(
            f"ಈ ವಲಯದಲ್ಲಿ ಬೆಳೆಯಲಾಗುತ್ತದೆಯಾದರೂ {ctx.season} ಮುಖ್ಯ ಹಂಗಾಮಲ್ಲ."
        )
    else:
        ev.location_score = 22.0
        badges["region"] = "low_fit"
        ev.limitations_en.append(
            f"Not listed as a major recommended crop for {ctx.location.taluk} ({ctx.location.zone_code}) in UAS/KSDA references."
        )
        ev.limitations_kn.append(
            f"{ctx.location.taluk} ({ctx.location.zone_code}) ವಲಯಕ್ಕೆ ಪ್ರಮುಖ ಶಿಫಾರಸು ಬೆಳೆ ಪಟ್ಟಿಯಲ್ಲಿಲ್ಲ."
        )

    # =========================================================================
    # STAGE 2: Seasonal & Sowing Month Compatibility
    # =========================================================================
    if ctx.season in req.suitable_seasons:
        ev.seasonal_score = 92.0
        badges["season"] = "aligned"
        ev.reasons_en.append(f"Well aligned with {ctx.season} sowing cycle ({crop.growing_duration_days_min}-{crop.growing_duration_days_max} days).")
        ev.reasons_kn.append(f"{ctx.season} ಹಂಗಾಮಿಗೆ ಸೂಕ್ತವಾದ ಬೆಳೆ ಅವಧಿ ({crop.growing_duration_days_min}-{crop.growing_duration_days_max} ದಿನಗಳು).")
    else:
        ev.hard_rejected = True
        ev.rejection_reasons_en.append(
            f"{crop.name_en} is normally suited to {', '.join(req.suitable_seasons)}, not {ctx.season}."
        )
        ev.rejection_reasons_kn.append(
            f"{crop.name_kn} ಸಾಮಾನ್ಯವಾಗಿ {', '.join(req.suitable_seasons)} ಹಂಗಾಮಿಗೆ ಸೂಕ್ತ; {ctx.season} ಹಂಗಾಮಿಗಲ್ಲ."
        )
        ev.conflict_flags.append("season_mismatch")
        badges["season"] = "mismatch"
        ev.compatibility_badges = badges
        return ev

    if ctx.intended_sowing_month:
        if ctx.intended_sowing_month in req.sowing_months:
            ev.seasonal_score = min(100.0, ev.seasonal_score + 8.0)
            ev.reasons_en.append(f"Intended sowing month ({ctx.intended_sowing_month}) matches recommended sowing window.")
            ev.reasons_kn.append(f"ಉದ್ದೇಶಿತ ಬಿತ್ತನೆ ತಿಂಗಳು ({ctx.intended_sowing_month}) ಸೂಕ್ತ ಸಮಯಕ್ಕೆ ಹೊಂದಿಕೊಳ್ಳುತ್ತದೆ.")
        else:
            ev.seasonal_score = max(55.0, ev.seasonal_score - 22.0)
            ev.limitations_en.append(
                f"Planned month ({ctx.intended_sowing_month}) differs from typical Karnataka sowing window ({', '.join(req.sowing_months)})."
            )
            ev.limitations_kn.append(
                f"ಬಿತ್ತನೆ ತಿಂಗಳು ({ctx.intended_sowing_month}) ಸಾಮಾನ್ಯ ಶಿಫಾರಸು ತಿಂಗಳುಗಳಿಂದ ({', '.join(req.sowing_months)}) ಭಿನ್ನವಾಗಿದೆ."
            )
    else:
        ev.missing_info_en.append("Intended sowing month was not specified; verify exact planting window locally.")
        ev.missing_info_kn.append("ಬಿತ್ತನೆ ತಿಂಗಳು ನೀಡಿಲ್ಲ; ಸ್ಥಳೀಯ ಮಳೆ ಆಧರಿಸಿ ಬಿತ್ತನೆ ದಿನಾಂಕ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.")

    # =========================================================================
    # STAGE 3: Observed Soil Texture, Drainage, Depth, Stones & Topography
    # =========================================================================
    soil_points = 0.0
    soil_weights = 0.0

    # 3A. Texture
    soil_weights += 35.0
    if ctx.soil_texture == "not_sure":
        soil_points += 20.0
        ev.missing_info_en.append("Soil feel/texture was marked 'Not sure' — perform a simple moist hand-feel check before seed purchase.")
        ev.missing_info_kn.append("ಮಣ್ಣಿನ ವಿನ್ಯಾಸ ತಿಳಿದಿಲ್ಲ ಎಂದು ಗುರುತಿಸಲಾಗಿದೆ — ಬಿತ್ತನೆಗೆ ಮುನ್ನ ತೇವ ಮಣ್ಣನ್ನು ಕೈಯಿಂದ ಪರೀಕ್ಷಿಸಿ.")
    elif ctx.soil_texture == "mixed":
        soil_points += 26.0
    elif ctx.soil_texture in req.suitable_textures:
        soil_points += 35.0
        ev.reasons_en.append(f"Observed {ctx.soil_texture} soil texture matches this crop's root-zone needs.")
        ev.reasons_kn.append(f"ನಿಮ್ಮ {ctx.soil_texture} ಮಣ್ಣಿನ ವಿನ್ಯಾಸವು ಈ ಬೆಳೆಯ ಬೇರಿನ ಅಗತ್ಯಕ್ಕೆ ಹೊಂದುತ್ತದೆ.")
    else:
        soil_points += 10.0
        ev.limitations_en.append(
            f"Prefers {', '.join(req.suitable_textures)} texture rather than {ctx.soil_texture} soil."
        )
        ev.limitations_kn.append(
            f"ಈ ಬೆಳೆಗೆ {', '.join(req.suitable_textures)} ಮಣ್ಣು ಹೆಚ್ಚು ಸೂಕ್ತ; ನಿಮ್ಮಲ್ಲಿ {ctx.soil_texture} ಮಣ್ಣಿದೆ."
        )

    # 3B. Drainage & Waterlogging Safety
    soil_weights += 30.0
    eff_drainage = _effective_drainage(ctx)
    if eff_drainage == "waterlogging_prone":
        if req.waterlogging_tolerance == "high":
            soil_points += 28.0
            ev.reasons_en.append("Field retains rainwater / experiences waterlogging, which this crop tolerates better than upland crops.")
            ev.reasons_kn.append("ಜಮೀನಿನಲ್ಲಿ ಮಳೆ ನೀರು ನಿಲ್ಲುವ ಸ್ಥಿತಿಗೆ ಇತರ ಬೆಳೆಗಳಿಗಿಂತ ಇದು ಉತ್ತಮ ಸಹಿಷ್ಣುತೆ ಹೊಂದಿದೆ.")
        elif req.waterlogging_tolerance == "moderate":
            soil_points += 14.0
            ev.conflict_flags.append("drainage_caution")
            ev.limitations_en.append("Slow drainage / waterlogging reported: raised beds or drainage channels are necessary.")
            ev.limitations_kn.append("ನೀರು ನಿಲ್ಲುವ ಸಮಸ್ಯೆ ವರದಿಯಾಗಿದೆ: ಬಸಿಕಾಲುವೆ ಅಥವಾ ಏರು ಮಡಿ ವ್ಯವಸ್ಥೆ ಅಗತ್ಯ.")
        else:
            soil_points += 2.0
            ev.conflict_flags.append("waterlogging_risk")
            ev.limitations_en.append("HIGH DRAINAGE WARNING: Water stands for >=1 day / waterlogs frequently, risking severe root rot in this crop.")
            ev.limitations_kn.append("ನೀರು ನಿಲ್ಲುವ ಎಚ್ಚರಿಕೆ: 1 ದಿನಕ್ಕೂ ಹೆಚ್ಚು ನೀರು ನಿಲ್ಲುವ ಜಮೀನಿನಲ್ಲಿ ಈ ಬೆಳೆಗೆ ಬೇರು ಕೊಳೆ ರೋಗದ ಅಪಾಯ ಹೆಚ್ಚು.")
    elif eff_drainage == "slow_draining":
        if req.waterlogging_tolerance == "low":
            soil_points += 15.0
            ev.conflict_flags.append("slow_drainage_caution")
            ev.limitations_en.append("Water stays for several hours after heavy rain; keep field outlets clear to protect roots.")
            ev.limitations_kn.append("ಭಾರಿ ಮಳೆಯ ನಂತರ ನೀರು ಕೆಲ ಗಂಟೆ ನಿಲ್ಲುವುದರಿಂದ ಬಸಿಕಾಲುವೆ ಸ್ವಚ್ಛವಾಗಿರಿಸಿ.")
        else:
            soil_points += 27.0
    elif eff_drainage == "rapid_draining":
        if crop.water_requirement_level == "High":
            soil_points += 6.0
            ev.conflict_flags.append("rapid_drainage_for_high_water")
            ev.limitations_en.append("Very rapid drainage makes it difficult to sustain high-water crops without frequent irrigation.")
            ev.limitations_kn.append("ನೀರು ಅತಿ ವೇಗವಾಗಿ ಬಸಿದುಹೋಗುವ ಮಣ್ಣಿನಲ್ಲಿ ಅಧಿಕ ನೀರಿನ ಬೆಳೆಗೆ ತೇವಾಂಶ ಕಾಪಾಡುವುದು ಕಷ್ಟ.")
        else:
            soil_points += 28.0
            ev.reasons_en.append("Well-drained field protects roots and pods from stagnation.")
            ev.reasons_kn.append("ನೀರು ಬೇಗ ಬಸಿದುಹೋಗುವ ಮಣ್ಣು ಬೇರು ಕೊಳೆ ರೋಗದಿಂದ ರಕ್ಷಿಸುತ್ತದೆ.")
    elif eff_drainage == "well_drained":
        soil_points += 30.0
        ev.reasons_en.append("Moderate rainwater drainage provides balanced root aeration.")
        ev.reasons_kn.append("ಮಧ್ಯಮ ನೀರು ಬಸಿಯುವಿಕೆ ಬೇರುಗಳಿಗೆ ಉತ್ತಮ ಗಾಳಿ ಮತ್ತು ತೇವಾಂಶ ನೀಡುತ್ತದೆ.")
    else:
        soil_points += 17.0
        ev.missing_info_en.append("Post-rain drainage observation was 'Not sure'; monitor standing water after heavy showers.")
        ev.missing_info_kn.append("ಮಳೆ ನೀರು ಬಸಿಯುವಿಕೆ ತಿಳಿದಿಲ್ಲ; ಮಳೆಯ ನಂತರ ನೀರು ನಿಲ್ಲುತ್ತದೆಯೇ ಗಮನಿಸಿ.")

    # 3C. Land Topography, Depth & Visible Stones
    soil_weights += 35.0
    topo_ok = ctx.land_topography in req.suitable_land_topography
    if ctx.land_topography == "rocky_stony":
        if req.min_soil_depth == "deep":
            soil_points += 6.0
            ev.conflict_flags.append("rocky_stony_root_limit")
            ev.limitations_en.append("Rocky/stony land restricts deep rooting required for long-duration crops.")
            ev.limitations_kn.append("ಕಲ್ಲು ಮಿಶ್ರಿತ ಭೂಮಿ ಆಳವಾದ ಬೇರು ಬಿಡುವ ಬೆಳೆಗಳಿಗೆ ತೊಂದರೆಯಾಗುತ್ತದೆ.")
        else:
            soil_points += 20.0
            ev.limitations_en.append("Rocky/stony plot limits mechanization and lowers moisture buffer.")
            ev.limitations_kn.append("ಕಲ್ಲು ಮಿಶ್ರಿತ ಭೂಮಿಯಲ್ಲಿ ಉಳುಮೆ ಮತ್ತು ತೇವಾಂಶ ಸಂಗ್ರಹಣೆ ಸೀಮಿತವಾಗಿರುತ್ತದೆ.")
    elif ctx.land_topography == "steep_hilly":
        if "steep_hilly" in req.suitable_land_topography:
            soil_points += 33.0
            ev.reasons_en.append("Adapted to sloped/hilly Malnad terrain with contour bunding or shade cover.")
            ev.reasons_kn.append("ಇಳಿಜಾರು/ಬೆಟ್ಟ ಪ್ರದೇಶಕ್ಕೆ ಸೂಕ್ತವಾದ ಬೆಳೆ (ಕಾಂಟೂರ್ ಬದುಗಳೊಂದಿಗೆ).")
        else:
            soil_points += 10.0
            ev.conflict_flags.append("slope_erosion_risk")
            ev.limitations_en.append("Steep/hilly slope increases runoff erosion risk; avoid clean-tilled row cultivation without terraces.")
            ev.limitations_kn.append("ತೀವ್ರ ಇಳಿಜಾರು ಪ್ರದೇಶದಲ್ಲಿ ಮಣ್ಣು ಸವಕಳಿ ತಡೆಯಲು ಮೆಟ್ಟಿಲು/ಕಾಂಟೂರ್ ವ್ಯವಸ್ಥೆ ಅಗತ್ಯ.")
    elif topo_ok:
        soil_points += 30.0
    else:
        soil_points += 16.0
        ev.limitations_en.append(f"Usually prefers {', '.join(req.suitable_land_topography)} land compared to {ctx.land_topography.replace('_', ' ')}.")
        ev.limitations_kn.append(f"ಈ ಬೆಳೆಗೆ {ctx.land_topography.replace('_', ' ')} ಭೂಮಿಗಿಂತ ಇತರ ಭೂಸ್ವರೂಪ ಹೆಚ್ಚು ಸೂಕ್ತ.")

    # Depth / stones penalty check
    if ctx.soil_depth != "unknown":
        req_depth = DEPTH_RANK.get(req.min_soil_depth, 2)
        obs_depth = DEPTH_RANK.get(ctx.soil_depth, 2)
        if obs_depth < req_depth:
            soil_points = max(0.0, soil_points - 14.0)
            ev.conflict_flags.append("shallow_soil_constraint")
            ev.limitations_en.append(
                f"Observed {ctx.soil_depth} soil depth is below the {req.min_soil_depth} root depth typically preferred."
            )
            ev.limitations_kn.append(
                f"ಗಮನಿಸಿದ {ctx.soil_depth} ಮಣ್ಣಿನ ಆಳವು ಈ ಬೆಳೆಗೆ ಬೇಕಾದ {req.min_soil_depth} ಆಳಕ್ಕಿಂತ ಕಡಿಮೆಯಿದೆ."
            )
    else:
        ev.missing_info_en.append("Approximate soil depth was marked 'Unknown'.")
        ev.missing_info_kn.append("ಮಣ್ಣಿನ ಆಳವನ್ನು 'ತಿಳಿದಿಲ್ಲ' ಎಂದು ನಮೂದಿಸಲಾಗಿದೆ.")

    if ctx.visible_stones == "many_stony" and req.min_soil_depth == "deep":
        soil_points = max(0.0, soil_points - 8.0)
        ev.limitations_en.append("Many visible stones may obstruct deep root establishment or tuber/pod harvesting.")
        ev.limitations_kn.append("ಜಮೀನಿನಲ್ಲಿ ಹೆಚ್ಚಿನ ಕಲ್ಲುಗಳಿರುವುದು ಬೇರು ಮತ್ತು ಕಾಯಿ ಬೆಳವಣಿಗೆಗೆ ಅಡ್ಡಿಯಾಗಬಹುದು.")

    # Soil color broad note (only cautious check, never asserts NPK/fertility!)
    if ctx.soil_color == "mixed_uncertain":
        ev.missing_info_en.append("Soil colour was uncertain; visual cue omitted without guessing fertility.")
        ev.missing_info_kn.append("ಮಣ್ಣಿನ ಬಣ್ಣ ಅನಿಶ್ಚಿತವಾಗಿರುವುದರಿಂದ ಫಲವತ್ತತೆ ಊಹೆ ಮಾಡಿಲ್ಲ.")

    ev.soil_land_score = round((soil_points / soil_weights) * 100.0, 2)
    badges["soil_land"] = (
        "strong" if ev.soil_land_score >= 78 else ("moderate" if ev.soil_land_score >= 52 else "caution")
    )

    # =========================================================================
    # STAGE 4: Water Availability & Moisture Retention Compatibility
    # =========================================================================
    water_tier = _effective_water_tier(ctx)
    eff_moisture = ctx.soil_observation.get("effective_moisture_retention", "unknown")

    if water_tier in ("rainfed_scarce", "limited"):
        if crop.water_requirement_level == "High":
            # Only reject if definitely not coastal/valley heavy rain
            ev.water_score = 12.0
            ev.conflict_flags.append("severe_water_shortage")
            badges["water"] = "mismatch"
            ev.limitations_en.append(
                f"HIGH WATER WARNING: {crop.name_en} needs {crop.water_requirement_mm_min}-{crop.water_requirement_mm_max} mm, unsuitable for limited/scarce water."
            )
            ev.limitations_kn.append(
                f"ನೀರಿನ ಕೊರತೆ ಎಚ್ಚರಿಕೆ: {crop.name_kn} ಬೆಳೆಗೆ ಅಧಿಕ ನೀರು ಅಗತ್ಯವಿದ್ದು ಸೀಮಿತ ನೀರಾವರಿಗೆ ಸೂಕ್ತವಲ್ಲ."
            )
        elif crop.water_requirement_level == "Moderate":
            if req.drought_tolerance == "high":
                ev.water_score = 72.0
                badges["water"] = "moderate"
            else:
                ev.water_score = 42.0
                badges["water"] = "caution"
                ev.conflict_flags.append("moisture_stress_risk")
                ev.limitations_en.append("Limited irrigation availability may stress moderate-water crops during dry spells.")
                ev.limitations_kn.append("ಸೀಮಿತ ನೀರಾವರಿ ಲಭ್ಯತೆಯು ಒಣ ದಿನಗಳಲ್ಲಿ ಮಧ್ಯಮ ನೀರಿನ ಬೆಳೆಗೆ ಒತ್ತಡ ತರಬಹುದು.")
        else:
            ev.water_score = 96.0
            badges["water"] = "aligned"
            ev.reasons_en.append(
                f"Low water demand ({crop.water_requirement_mm_min}-{crop.water_requirement_mm_max} mm) & {req.drought_tolerance} drought tolerance fit scarce/limited water."
            )
            ev.reasons_kn.append(
                f"ಕಡಿಮೆ ನೀರಿನ ಬೇಡಿಕೆ ({crop.water_requirement_mm_min}-{crop.water_requirement_mm_max} ಮಿ.ಮೀ) ಸೀಮಿತ ನೀರಿನ ಪರಿಸ್ಥಿತಿಗೆ ಉತ್ತಮವಾಗಿ ಹೊಂದುತ್ತದೆ."
            )
    elif water_tier in ("rainfed_normal", "uncertain"):
        if crop.water_requirement_level == "High":
            ev.water_score = 26.0
            badges["water"] = "caution"
            ev.conflict_flags.append("insufficient_assured_water")
            ev.limitations_en.append("Requires assured supplemental irrigation; rainfed/uncertain water increases crop failure risk.")
            ev.limitations_kn.append("ಮಳೆಯಾಶ್ರಿತ ಅಥವಾ ಅನಿಶ್ಚಿತ ನೀರಾವರಿಯಲ್ಲಿ ಈ ಅಧಿಕ ನೀರಿನ ಬೆಳೆಗೆ ಅಪಾಯ ಹೆಚ್ಚು.")
        elif crop.water_requirement_level == "Moderate":
            ev.water_score = 74.0
            badges["water"] = "moderate"
            if eff_moisture in ("low_retention", "likely_low_retention"):
                ev.water_score = 54.0
                ev.limitations_en.append("Fast-drying soil + rainfed status requires mulching or protective irrigation during flowering.")
                ev.limitations_kn.append("ಬೇಗ ಒಣಗುವ ಮಣ್ಣಿನಲ್ಲಿ ಹೂಬಿಡುವ ಹಂತದಲ್ಲಿ ತೇವಾಂಶ ರಕ್ಷಣೆ ಅಗತ್ಯ.")
        else:
            ev.water_score = 95.0
            badges["water"] = "aligned"
            ev.reasons_en.append("Low-water crop well matched for rainfed moisture conservation.")
            ev.reasons_kn.append("ಮಳೆಯಾಶ್ರಿತ ತೇವಾಂಶದಲ್ಲಿ ಸುರಕ್ಷಿತವಾಗಿ ಬೆಳೆಯುವ ಕಡಿಮೆ ನೀರಿನ ಬೆಳೆ.")
    elif water_tier in ("moderate", "rainfed_humid"):
        if crop.water_requirement_level == "High" and water_tier == "moderate":
            ev.water_score = 58.0
            badges["water"] = "caution"
            ev.limitations_en.append("Requires seasonal irrigation support; partial/certain-month water may not cover maturity.")
            ev.limitations_kn.append("ಕೆಲವು ತಿಂಗಳು ಮಾತ್ರ ನೀರು ಲಭ್ಯವಿದ್ದಲ್ಲಿ ಸಂಪೂರ್ಣ ಬೆಳೆ ಅವಧಿಗೆ ನೀರು ಸಾಲದಿರಬಹುದು.")
        else:
            ev.water_score = 92.0
            badges["water"] = "aligned"
            ev.reasons_en.append("Available water regime supports healthy growth across key stages.")
            ev.reasons_kn.append("ಲಭ್ಯವಿರುವ ನೀರಾವರಿ ಮತ್ತು ಮಳೆ ಪ್ರಮಾಣ ಬೆಳೆಯ ಹಂತಗಳಿಗೆ ಪೂರಕವಾಗಿದೆ.")
    else:  # assured
        ev.water_score = 96.0 if crop.water_requirement_level in ("Moderate", "High") else 86.0
        badges["water"] = "aligned"
        ev.reasons_en.append("Year-round/assured irrigation availability removes moisture bottleneck.")
        ev.reasons_kn.append("ಋತುವಿನ ಪೂರ್ತಿ ನೀರಾವರಿ ಲಭ್ಯತೆ ಇರುವುದರಿಂದ ತೇವಾಂಶದ ಕೊರತೆ ಇರುವುದಿಲ್ಲ.")

    if ctx.water_reliability == "uncertain":
        ev.missing_info_en.append("Irrigation reliability marked 'Uncertain' — verify borewell/canal release schedule before planting.")
        ev.missing_info_kn.append("ನೀರಾವರಿ ಸ್ಥಿರತೆ 'ಖಚಿತವಿಲ್ಲ' ಎಂದು ನಮೂದಿಸಲಾಗಿದೆ — ಬಿತ್ತನೆಗೆ ಮುನ್ನ ನೀರಿನ ಲಭ್ಯತೆ ಖಚಿತಪಡಿಸಿ.")

    # =========================================================================
    # STAGE 5: Climate & Weather Risk Suitability
    # =========================================================================
    long_climate = ctx.weather_intel["long_term_climate"]
    advisory = ctx.weather_intel["farming_advisory"]
    zone_temp = float(long_climate["season_normal_temp_c"])
    zone_annual_rain = float(long_climate.get("normal_annual_rainfall_mm") or 700.0)

    climate_pts = 80.0
    if req.temp_min_c <= zone_temp <= req.temp_max_c:
        climate_pts += 12.0
    else:
        climate_pts -= 28.0
        ev.limitations_en.append(
            f"Normal {ctx.season} temperature ({zone_temp:.1f} C) sits outside optimal {req.temp_min_c:.0f}-{req.temp_max_c:.0f} C range."
        )
        ev.limitations_kn.append(
            f"ವಲಯದ ಸಾಮಾನ್ಯ ತಾಪಮಾನ ({zone_temp:.1f}°C) ಸೂಕ್ತ ವ್ಯಾಪ್ತಿಗಿಂತ ({req.temp_min_c:.0f}-{req.temp_max_c:.0f}°C) ಭಿನ್ನವಾಗಿದೆ."
        )

    if zone_annual_rain < req.rainfall_min_mm and ctx.water_source == "rainfed":
        climate_pts -= 20.0
        ev.limitations_en.append(
            f"Zone normal rainfall ({zone_annual_rain:.0f} mm/yr) is tight for rainfed cultivation without supplemental water."
        )
        ev.limitations_kn.append(
            f"ವಲಯದ ವಾರ್ಷಿಕ ಮಳೆ ({zone_annual_rain:.0f} ಮಿ.ಮೀ) ಪೂರಕ ನೀರಾವರಿ ಇಲ್ಲದೆ ಸಾಲದಿರಬಹುದು."
        )
    elif zone_annual_rain > req.rainfall_max_mm * 1.15:
        climate_pts -= 18.0
        ev.limitations_en.append(
            f"High rainfall zone ({zone_annual_rain:.0f} mm/yr) elevates fungal/pod-rot risk for this crop."
        )
        ev.limitations_kn.append(
            f"ಅಧಿಕ ಮಳೆ ವಲಯದಲ್ಲಿ ({zone_annual_rain:.0f} ಮಿ.ಮೀ) ಬೂಷ್ಟು ಮತ್ತು ಕಾಯಿ ಕೊಳೆ ರೋಗದ ಅಪಾಯ ಹೆಚ್ಚು."
        )

    # Crop-stage specific weather risk note
    threshold_info = req.weather_risk_thresholds or {}
    if advisory.get("dry_spell_risk_level") == "high" and req.drought_tolerance == "low":
        climate_pts -= 16.0
        ev.limitations_en.append("Dry-spell risk flagged for this season + low drought tolerance requires protective irrigation readiness.")
        ev.limitations_kn.append("ಒಣ ಹವಾಮಾನದ ಅಪಾಯ ಹೆಚ್ಚಿದ್ದು ಈ ಬೆಳೆಗೆ ಸಂರಕ್ಷಣಾ ನೀರಾವರಿ ಸಿದ್ಧತೆ ಅಗತ್ಯ.")
    if threshold_info.get("risk_note_en"):
        ev.limitations_en.append(f"Weather stage check: {threshold_info['risk_note_en']}")
        ev.limitations_kn.append(f"ಹವಾಮಾನ ಹಂತದ ಎಚ್ಚರಿಕೆ: {threshold_info.get('risk_note_kn', threshold_info['risk_note_en'])}")

    if not advisory.get("live_weather_available"):
        ev.missing_info_en.append("Live current weather / 7-day forecast was unavailable; climate check relies on long-term zone normals.")
        ev.missing_info_kn.append("ಪ್ರಸ್ತುತ ನೇರ ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ ಲಭ್ಯವಿಲ್ಲದ ಕಾರಣ ದೀರ್ಘಕಾಲೀನ ಸರಾಸರಿ ಬಳಸಲಾಗಿದೆ.")

    ev.climate_score = round(max(10.0, min(100.0, climate_pts)), 2)

    # =========================================================================
    # STAGE 6 & 7: Farming Priority, Duration Preference & Rotation History
    # =========================================================================
    priority_pts = 72.0

    # Duration match
    if ctx.duration_preference == "short":
        if crop.duration_category == "short":
            priority_pts += 22.0
            badges["duration"] = "short_match"
            ev.reasons_en.append(f"Short growing duration ({crop.growing_duration_days_min}-{crop.growing_duration_days_max} days) satisfies your fast-harvest preference.")
            ev.reasons_kn.append(f"ಕಡಿಮೆ ಬೆಳೆ ಅವಧಿ ({crop.growing_duration_days_min}-{crop.growing_duration_days_max} ದಿನಗಳು) ನಿಮ್ಮ ಆದ್ಯತೆಗೆ ಹೊಂದುತ್ತದೆ.")
        elif crop.duration_category == "long":
            priority_pts -= 26.0
            badges["duration"] = "longer_than_requested"
            ev.limitations_en.append(f"Requires {crop.growing_duration_days_min}+ days, longer than your short-duration preference.")
            ev.limitations_kn.append(f"ಇದು {crop.growing_duration_days_min}+ ದಿನಗಳ ದೀರ್ಘಾವಧಿ ಬೆಳೆಯಾಗಿದೆ.")
        else:
            priority_pts -= 6.0
            badges["duration"] = "medium"
    elif ctx.duration_preference == "long":
        if crop.duration_category == "long":
            priority_pts += 16.0
            badges["duration"] = "long_match"
        else:
            badges["duration"] = crop.duration_category
    else:
        badges["duration"] = crop.duration_category

    # Farming priority alignment
    if ctx.farming_priority == "low_water":
        if crop.water_requirement_level == "Low":
            priority_pts += 20.0
            ev.reasons_en.append("Selected specifically to match your low-water cultivation priority.")
            ev.reasons_kn.append("ಕಡಿಮೆ ನೀರಿನ ಬೆಳೆ ಆದ್ಯತೆಗೆ ಸಂಪೂರ್ಣವಾಗಿ ಹೊಂದುತ್ತದೆ.")
        elif crop.water_requirement_level == "High":
            priority_pts -= 28.0
    elif ctx.farming_priority == "short_duration":
        if crop.duration_category == "short":
            priority_pts += 22.0
        elif crop.duration_category == "medium" and crop.growing_duration_days_max <= 115:
            priority_pts += 10.0
        elif crop.duration_category == "long":
            priority_pts -= 25.0
    elif ctx.farming_priority == "household_food":
        if crop.household_food_crop:
            priority_pts += 16.0
            ev.reasons_en.append("Provides household staple food / pulse / oilseed value.")
            ev.reasons_kn.append("ಕುಟುಂಬದ ಆಹಾರ ಬಳಕೆಗೆ ಉಪಯುಕ್ತವಾದ ಬೆಳೆ.")
        else:
            priority_pts -= 14.0
    elif ctx.farming_priority == "commercial":
        if crop.commercial_crop:
            priority_pts += 16.0
        else:
            priority_pts -= 8.0

    # History adjustments (optional inputs)
    if ctx.previous_crop:
        prev = ctx.previous_crop.strip().lower()
        same_crop = prev in crop.crop_key or prev in crop.name_en.lower()
        prev_cereal = any(w in prev for w in ("rice", "paddy", "maize", "jowar", "ragi", "sugarcane"))
        if same_crop:
            priority_pts -= 18.0
            ev.conflict_flags.append("monocropping_caution")
            ev.limitations_en.append(
                f"Growing {crop.name_en} immediately after '{ctx.previous_crop}' risks repeating soil-borne pests/nutrients depletion; consider crop rotation."
            )
            ev.limitations_kn.append(
                f"ಹಿಂದಿನ ಬೆಳೆ '{ctx.previous_crop}' ನಂತರ ಅದೇ ಬೆಳೆ ಹಾಕುವುದರಿಂದ ಕೀಟ ಮತ್ತು ಪೋಷಕಾಂಶ ಕೊರತೆ ಹೆಚ್ಚಬಹುದು; ಬೆಳೆ ಪರಿವರ್ತನೆ ಒಳ್ಳೆಯದು."
            )
        elif prev_cereal and crop.category in ("Pulse", "Oilseed"):
            priority_pts += 12.0
            ev.reasons_en.append(
                f"Good crop rotation break after '{ctx.previous_crop}' — helps rebuild root health and soil nitrogen cycle."
            )
            ev.reasons_kn.append(
                f"ಹಿಂದಿನ '{ctx.previous_crop}' ಬೆಳೆಯ ನಂತರ ದ್ವಿದಳ/ಎಣ್ಣೆಕಾಳು ಬೆಳೆ ಪರಿವರ್ತನೆಗೆ ಅತ್ಯುತ್ತಮವಾಗಿದೆ."
            )

    if ctx.drought_history == "yes":
        if req.drought_tolerance == "high":
            priority_pts += 10.0
            ev.reasons_en.append("Selected with strong drought recovery considering prior drought history on the field.")
            ev.reasons_kn.append("ಹಿಂದೆ ಬರ ಅನುಭವಿಸಿದ್ದ ಜಮೀನಿಗೆ ಬರ ಸಹಿಷ್ಣು ಗುಣ ಅನುಕೂಲಕರವಾಗಿದೆ.")
        elif req.drought_tolerance == "low":
            priority_pts -= 18.0
            ev.limitations_en.append("Field has prior drought history; this crop is sensitive to dry spells.")
            ev.limitations_kn.append("ಜಮೀನಿನಲ್ಲಿ ಹಿಂದೆ ಬರ ಅನುಭವವಿರುವುದರಿಂದ ಈ ಬೆಳೆಗೆ ಎಚ್ಚರಿಕೆ ಅಗತ್ಯ.")

    if ctx.flood_history == "yes":
        if req.waterlogging_tolerance == "low":
            priority_pts -= 16.0
            ev.conflict_flags.append("prior_flood_caution")
            ev.limitations_en.append("Field has flooding history; avoid sowing without effective perimeter drainage.")
            ev.limitations_kn.append("ಹಿಂದೆ ಪ್ರವಾಹ/ನೀರು ನಿಲ್ಲುವ ಅನುಭವ ಇರುವುದರಿಂದ ಬಸಿಕಾಲುವೆ ವ್ಯವಸ್ಥೆ ಇಲ್ಲದೆ ಬಿತ್ತನೆ ಬೇಡ.")

    if ctx.pest_disease_history:
        ev.limitations_en.append(
            f"Prior recurring issue noted ('{ctx.pest_disease_history}'): follow UAS/RSK seed treatment and IPM before sowing."
        )
        ev.limitations_kn.append(
            f"ಹಿಂದಿನ ಕೀಟ/ರೋಗ ಸಮಸ್ಯೆ ('{ctx.pest_disease_history}') ಹಿನ್ನೆಲೆಯಲ್ಲಿ ಬಿತ್ತನೆಗೆ ಮುನ್ನ ಬೀಜೋಪಚಾರ ಮಾಡಿ."
        )

    ev.priority_score = round(max(10.0, min(100.0, priority_pts)), 2)
    ev.compatibility_badges = badges
    return ev
