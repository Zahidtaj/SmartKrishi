"""Observation-based and location-aware crop recommendation orchestration service."""

from typing import Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, selectinload

from backend.models import (
    Crop,
    Farmer,
    FarmProfile,
    Location,
    Recommendation,
    RecommendationResult,
    SoilRecord,
)
from backend.rules.agronomic_rules import EvaluationContext, evaluate_crop_observation_rules
from backend.rules.scoring import compute_observation_score
from backend.schemas import (
    DimensionScoresSchema,
    RecommendationRequest,
    RecommendationResponse,
    RecommendedCropResultSchema,
)
from backend.services.soil_observation_service import interpret_soil_observations
from backend.services.weather_service import get_weather_intelligence

SCORING_NOTICE_EN = (
    "Suitability ranking is an explainable rule-based prototype index derived from regional Karnataka zone rules, "
    "farmer physical observations, water availability, and available climate normals — NOT a prediction of yield, income, or laboratory fertility."
)
SCORING_NOTICE_KN = (
    "ಬೆಳೆ ಸೂಕ್ತತಾ ಶ್ರೇಯಾಂಕವು ಕರ್ನಾಟಕ ಕೃಷಿ-ಹವಾಮಾನ ವಲಯದ ನಿಯಮಗಳು, ರೈತರ ಭೌತಿಕ ವೀಕ್ಷಣೆ ಮತ್ತು ನೀರಾವರಿ ಮಾಹಿತಿಯನ್ನು ಆಧರಿಸಿದ "
    "ಪ್ರಾಥಮಿಕ ಮಾರ್ಗದರ್ಶಿಯಾಗಿದೆ — ಇದು ಖಚಿತ ಇಳುವರಿ ಅಥವಾ ಆದಾಯದ ಭರವಸೆಯಲ್ಲ."
)
DISCLAIMER_EN = (
    "SmartKrishi is an educational VTU Community Project decision-support prototype. Soil colour/texture observations do not replace laboratory Soil Health Card testing for fertilizer dosing. Consult local Raitha Samparka Kendra (RSK) or KVK agronomists before final crop investment."
)
DISCLAIMER_KN = (
    "SmartKrishi ಶೈಕ್ಷಣಿಕ VTU ಸಮುದಾಯ ಯೋಜನೆಯ ಮಾರ್ಗದರ್ಶಿ ಸಾಧನವಾಗಿದೆ. ರಸಗೊಬ್ಬರ ಪ್ರಮಾಣಕ್ಕಾಗಿ ಮಣ್ಣಿನ ಬಣ್ಣ/ವಿನ್ಯಾಸ ಪರೀಕ್ಷೆ ಪರ್ಯಾಯವಲ್ಲ; ಅಂತಿಮ ಕೃಷಿ ನಿರ್ಧಾರಕ್ಕೆ ಹತ್ತಿರದ ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರ (RSK) ಅಥವಾ ಕೆವಿಕೆ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ."
)


def _resolve_location(db: Session, state: str, district: str, taluk: str) -> Location:
    loc = (
        db.query(Location)
        .filter(
            Location.state.ilike(state.strip()),
            Location.district.ilike(district.strip()),
            Location.taluk.ilike(taluk.strip()),
        )
        .first()
    )
    if loc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Selected location '{taluk}, {district}, {state}' is not in the supported Karnataka dataset.",
        )
    return loc


def generate_recommendation(
    db: Session,
    payload: RecommendationRequest,
    force_live_weather_unavailable: bool = False,
) -> RecommendationResponse:
    """Validate location & observations, interpret soil & weather, score crops, persist and return response."""
    location = _resolve_location(db, payload.state, payload.district, payload.taluk)

    # 1. Interpret farmer physical soil & land observations (never assumes NPK/pH from color)
    soil_obs = interpret_soil_observations(
        soil_color=payload.soil_color,
        soil_texture=payload.soil_texture,
        drainage_after_rain=payload.drainage_after_rain,
        moisture_retention=payload.moisture_retention,
        soil_depth=payload.soil_depth,
        visible_stones=payload.visible_stones,
        waterlogging_issue=payload.waterlogging_issue,
        erosion_issue=payload.erosion_issue,
        land_topography=payload.land_topography,
    )

    # 2. Weather & Climate Intelligence Module
    weather_intel = get_weather_intelligence(
        location=location,
        season=payload.season,
        soil_observation=soil_obs,
        water_source=payload.water_source,
        water_reliability=payload.water_reliability,
        intended_sowing_month=payload.intended_sowing_month,
        force_live_unavailable=force_live_weather_unavailable or payload.simulate_weather_unavailable,
    )

    # 3. Collect overall system warnings and missing information
    warnings: list[str] = []
    missing_information: list[str] = list(soil_obs["unknown_fields"])

    if soil_obs["effective_drainage"] == "waterlogging_prone":
        warnings.append(
            "Waterlogging / multi-day standing water reported: upland crops face high root-rot risk unless surface drainage is built."
        )
    if soil_obs["observation_confidence"] == "low":
        warnings.append(
            "Multiple soil observations were marked 'Not sure / Unknown'. Rankings rely primarily on Karnataka agro-climatic zone, season, and water availability."
        )
    if not weather_intel["farming_advisory"]["live_weather_available"]:
        warnings.append(
            "Live weather & short-term forecast feed is currently unavailable; advisory uses verified long-term zone normals without fabricating live data."
        )
        missing_information.append("live_weather_forecast")
    if payload.water_reliability == "uncertain":
        missing_information.append("water_reliability")
    if not payload.intended_sowing_month:
        missing_information.append("intended_sowing_month")

    # Confidence calculation
    confidence_level = soil_obs["observation_confidence"]
    if payload.water_reliability == "uncertain" and confidence_level == "high":
        confidence_level = "moderate"
    if not weather_intel["farming_advisory"]["live_weather_available"] and confidence_level == "high":
        confidence_level = "moderate"

    # 4. Evaluate all active crops using transparent observation rule engine
    crops = (
        db.query(Crop)
        .options(selectinload(Crop.requirement), selectinload(Crop.regional_rules))
        .filter(Crop.is_active.is_(True))
        .all()
    )

    ctx = EvaluationContext(
        location=location,
        season=payload.season,
        soil_color=payload.soil_color,
        soil_texture=payload.soil_texture,
        drainage_after_rain=payload.drainage_after_rain,
        moisture_retention=payload.moisture_retention,
        soil_depth=payload.soil_depth,
        visible_stones=payload.visible_stones,
        waterlogging_issue=payload.waterlogging_issue,
        erosion_issue=payload.erosion_issue,
        land_topography=payload.land_topography,
        water_source=payload.water_source,
        water_reliability=payload.water_reliability,
        intended_sowing_month=payload.intended_sowing_month,
        duration_preference=payload.duration_preference,
        farming_priority=payload.farming_priority,
        previous_crop=payload.previous_crop,
        previous_crop_success=payload.previous_crop_success,
        drought_history=payload.drought_history,
        flood_history=payload.flood_history,
        pest_disease_history=payload.pest_disease_history,
        soil_observation=soil_obs,
        weather_intel=weather_intel,
    )

    scored_candidates: list[tuple[float, str, dict[str, float], Any]] = []
    for crop in crops:
        if crop.requirement is None:
            continue
        ev = evaluate_crop_observation_rules(
            crop=crop,
            req=crop.requirement,
            rules=crop.regional_rules,
            ctx=ctx,
        )
        score, category, dims = compute_observation_score(ev)
        if not ev.hard_rejected:
            scored_candidates.append((score, category, dims, ev))

    scored_candidates.sort(key=lambda item: (-item[0], item[3].crop.crop_key))
    top_candidates = [c for c in scored_candidates if c[0] >= 35.0][:3]
    if not top_candidates and scored_candidates:
        top_candidates = scored_candidates[:3]

    insufficient_data_reason = None
    if not top_candidates:
        confidence_level = "low"
        insufficient_data_reason = (
            f"No crop cleanly passed regional {payload.season} constraints in {location.taluk}. "
            "Consult local KVK / Raitha Samparka Kendra for micro-plot guidance."
        )
    elif soil_obs["observation_confidence"] == "low":
        insufficient_data_reason = (
            "Soil feel, drainage, and moisture retention were largely unknown; top options reflect verified Karnataka zone, season, and water fit."
        )

    # 5. Track strict provenance categorization
    farmer_observed = [
        f"soil_color={payload.soil_color}",
        f"soil_texture={payload.soil_texture}",
        f"drainage_after_rain={payload.drainage_after_rain}",
        f"moisture_retention={payload.moisture_retention}",
        f"soil_depth={payload.soil_depth}",
        f"visible_stones={payload.visible_stones}",
        f"waterlogging_issue={payload.waterlogging_issue}",
        f"erosion_issue={payload.erosion_issue}",
        f"land_topography={payload.land_topography}",
        f"water_source={payload.water_source}",
        f"water_reliability={payload.water_reliability}",
        f"season={payload.season}",
        f"duration_preference={payload.duration_preference}",
        f"farming_priority={payload.farming_priority}",
    ]
    if payload.previous_crop:
        farmer_observed.append(f"previous_crop={payload.previous_crop}")
    if payload.land_area_acres:
        farmer_observed.append(f"land_area_acres={payload.land_area_acres}")

    input_provenance = {
        "farmer_observed": {
            "label": "Farmer Physical & Operational Observations",
            "fields": farmer_observed,
        },
        "institution_sourced": {
            "label": "Verified Regional & Agronomic Institutional Data",
            "sources": location.regional_references,
            "location_verification_status": location.verification_status,
            "location_last_updated": str(location.last_updated),
        },
        "weather_provider_sourced": {
            "label": "Weather Provider Status",
            "current_weather_status": weather_intel["current_weather"]["status"],
            "short_term_forecast_status": weather_intel["short_term_forecast"]["status"],
            "provider": weather_intel["current_weather"]["provider"],
        },
        "demonstration_data": {
            "label": "Prototype Demonstration Indicators",
            "note": "Suitability index (0-100) and illustrative per-acre cost/price bands are prototype demonstration tools, not guaranteed yields or APMC quotes.",
        },
    }

    # 6. Persist normalized relational records
    farmer = Farmer(session_label="web-farmer-session", preferred_language=payload.language)
    db.add(farmer)
    db.flush()

    soil_rec = SoilRecord(
        farmer_id=farmer.id,
        location_id=location.id,
        soil_color=payload.soil_color,
        soil_texture=payload.soil_texture,
        drainage_after_rain=payload.drainage_after_rain,
        moisture_retention=payload.moisture_retention,
        soil_depth=payload.soil_depth,
        visible_stones=payload.visible_stones,
        waterlogging_issue=payload.waterlogging_issue,
        erosion_issue=payload.erosion_issue,
        observation_confidence=soil_obs["observation_confidence"],
        measurement_source="farmer_observation",
    )
    db.add(soil_rec)

    long_climate = weather_intel["long_term_climate"]
    curr_w = weather_intel["current_weather"]
    farm_profile = FarmProfile(
        farmer_id=farmer.id,
        location_id=location.id,
        village=payload.village,
        land_topography=payload.land_topography,
        water_source=payload.water_source,
        water_reliability=payload.water_reliability,
        previous_crop=payload.previous_crop,
        previous_crop_success=payload.previous_crop_success,
        drought_history=payload.drought_history,
        flood_history=payload.flood_history,
        pest_disease_history=payload.pest_disease_history,
        land_area_acres=payload.land_area_acres,
        season=payload.season,
        intended_sowing_month=payload.intended_sowing_month,
        duration_preference=payload.duration_preference,
        farming_priority=payload.farming_priority,
        temperature_c=curr_w.get("temperature_c") or long_climate.get("season_normal_temp_c"),
        humidity_pct=curr_w.get("humidity_pct") or long_climate.get("season_normal_humidity_pct"),
        rainfall_mm=long_climate.get("normal_annual_rainfall_mm"),
        climate_source="live_plus_zone_normal" if weather_intel["farming_advisory"]["live_weather_available"] else "zone_long_term_normal",
    )
    db.add(farm_profile)
    db.flush()

    input_snapshot = payload.model_dump(mode="json")
    rec = Recommendation(
        farmer_id=farmer.id,
        location_id=location.id,
        soil_record_id=soil_rec.id,
        farm_profile_id=farm_profile.id,
        mode_used="observation_rule_based",
        confidence_level=confidence_level,
        soil_interpretation=soil_obs,
        weather_advisory=weather_intel,
        input_provenance=input_provenance,
        input_snapshot=input_snapshot,
        warnings=warnings,
        missing_information=missing_information,
        insufficient_data_reason=insufficient_data_reason,
        model_version="observation-rules-v2.0",
    )
    db.add(rec)
    db.flush()

    result_schemas: list[RecommendedCropResultSchema] = []
    for idx, (score, category, dims, ev) in enumerate(top_candidates, start=1):
        crop = ev.crop
        reasons_en = ev.reasons_en[:5] or [f"Matches regional {payload.season} agricultural reference in {location.agro_climatic_zone}."]
        reasons_kn = ev.reasons_kn[:5] or [f"{location.agro_climatic_zone} ವಲಯದ {payload.season} ಹಂಗಾಮಿಗೆ ಹೊಂದಿಕೊಳ್ಳುತ್ತದೆ."]
        limitations_en = ev.limitations_en[:5] or ["Confirm local seed variety and sowing date with nearest RSK before planting."]
        limitations_kn = ev.limitations_kn[:5] or ["ಬಿತ್ತನೆಗೆ ಮುನ್ನ ಹತ್ತಿರದ ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರದಲ್ಲಿ ಸೂಕ್ತ ತಳಿ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ."]

        rec_res = RecommendationResult(
            recommendation_id=rec.id,
            crop_id=crop.id,
            rank=idx,
            suitability_category=category,
            illustrative_score=score,
            ml_probability=None,
            dimension_scores=dims,
            reasons_en=reasons_en,
            reasons_kn=reasons_kn,
            limitations_en=limitations_en,
            limitations_kn=limitations_kn,
            missing_info_en=ev.missing_info_en[:4],
            missing_info_kn=ev.missing_info_kn[:4],
            compatibility_badges=ev.compatibility_badges,
            conflict_flags=ev.conflict_flags,
        )
        db.add(rec_res)
        result_schemas.append(
            RecommendedCropResultSchema(
                rank=idx,
                crop_id=crop.id,
                crop_key=crop.crop_key,
                name_en=crop.name_en,
                name_kn=crop.name_kn,
                scientific_name=crop.scientific_name,
                category=crop.category,
                image_asset=crop.image_asset,
                suitability_category=category,
                illustrative_score=score,
                dimension_scores=DimensionScoresSchema(**dims),
                reasons_en=reasons_en,
                reasons_kn=reasons_kn,
                limitations_en=limitations_en,
                limitations_kn=limitations_kn,
                missing_info_en=ev.missing_info_en[:4],
                missing_info_kn=ev.missing_info_kn[:4],
                compatibility_badges=ev.compatibility_badges,
                conflict_flags=ev.conflict_flags,
                water_requirement_level=crop.water_requirement_level,
                water_requirement_mm_min=crop.water_requirement_mm_min,
                water_requirement_mm_max=crop.water_requirement_mm_max,
                suitable_seasons=crop.requirement.suitable_seasons,
                growing_duration_days_min=crop.growing_duration_days_min,
                growing_duration_days_max=crop.growing_duration_days_max,
                cultivation_guidance_en=crop.cultivation_guidance_en,
                cultivation_guidance_kn=crop.cultivation_guidance_kn,
                information_source=crop.information_source,
                record_status=crop.record_status,
            )
        )

    db.commit()
    db.refresh(rec)

    return _build_response(
        rec=rec,
        location=location,
        results=result_schemas,
    )


def get_recommendation_by_id(db: Session, recommendation_id: int) -> RecommendationResponse:
    rec = (
        db.query(Recommendation)
        .options(selectinload(Recommendation.results).selectinload(RecommendationResult.crop).selectinload(Crop.requirement))
        .filter(Recommendation.id == recommendation_id)
        .first()
    )
    if rec is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recommendation #{recommendation_id} was not found.",
        )

    location = db.query(Location).filter(Location.id == rec.location_id).first()
    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location record for recommendation missing.")

    result_schemas: list[RecommendedCropResultSchema] = []
    for res in rec.results:
        crop = res.crop
        result_schemas.append(
            RecommendedCropResultSchema(
                rank=res.rank,
                crop_id=crop.id,
                crop_key=crop.crop_key,
                name_en=crop.name_en,
                name_kn=crop.name_kn,
                scientific_name=crop.scientific_name,
                category=crop.category,
                image_asset=crop.image_asset,
                suitability_category=res.suitability_category,
                illustrative_score=res.illustrative_score,
                dimension_scores=DimensionScoresSchema(**res.dimension_scores),
                reasons_en=res.reasons_en,
                reasons_kn=res.reasons_kn,
                limitations_en=res.limitations_en,
                limitations_kn=res.limitations_kn,
                missing_info_en=res.missing_info_en or [],
                missing_info_kn=res.missing_info_kn or [],
                compatibility_badges=res.compatibility_badges or {},
                conflict_flags=res.conflict_flags or [],
                water_requirement_level=crop.water_requirement_level,
                water_requirement_mm_min=crop.water_requirement_mm_min,
                water_requirement_mm_max=crop.water_requirement_mm_max,
                suitable_seasons=crop.requirement.suitable_seasons if crop.requirement else [],
                growing_duration_days_min=crop.growing_duration_days_min,
                growing_duration_days_max=crop.growing_duration_days_max,
                cultivation_guidance_en=crop.cultivation_guidance_en,
                cultivation_guidance_kn=crop.cultivation_guidance_kn,
                information_source=crop.information_source,
                record_status=crop.record_status,
            )
        )

    return _build_response(rec=rec, location=location, results=result_schemas)


def _build_response(
    *,
    rec: Recommendation,
    location: Location,
    results: list[RecommendedCropResultSchema],
) -> RecommendationResponse:
    return RecommendationResponse(
        recommendation_id=rec.id,
        created_at=rec.created_at,
        mode_used=rec.mode_used,
        confidence_level=rec.confidence_level,
        scoring_notice_en=SCORING_NOTICE_EN,
        scoring_notice_kn=SCORING_NOTICE_KN,
        disclaimer_en=DISCLAIMER_EN,
        disclaimer_kn=DISCLAIMER_KN,
        warnings=rec.warnings or [],
        missing_information=rec.missing_information or [],
        insufficient_data_reason=rec.insufficient_data_reason,
        location_context={
            "state": location.state,
            "district": location.district,
            "taluk": location.taluk,
            "agro_climatic_zone": location.agro_climatic_zone,
            "zone_code": location.zone_code,
            "normal_annual_rainfall_mm": location.normal_annual_rainfall_mm,
            "typical_rainfall_pattern": location.typical_rainfall_pattern,
            "dominant_soil_types": location.dominant_soil_types,
            "common_soil_textures": location.common_soil_textures,
            "major_crops": location.major_crops,
            "recommended_seasons_summary": location.recommended_seasons_summary,
            "growing_period_info": location.growing_period_info,
            "regional_references": location.regional_references,
            "data_source": location.data_source,
            "verification_status": location.verification_status,
            "last_updated": str(location.last_updated),
        },
        soil_interpretation=rec.soil_interpretation or {},
        weather_advisory=rec.weather_advisory or {},
        input_provenance=rec.input_provenance or {},
        input_summary=rec.input_snapshot or {},
        recommendations=results,
    )
