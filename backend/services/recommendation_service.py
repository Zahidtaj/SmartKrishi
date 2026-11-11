"""Hybrid Recommendation Service orchestrating ML prediction, agronomic rules, and DB persistence."""

from typing import Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from backend.models import (
    Crop,
    FarmProfile,
    Farmer,
    Location,
    Recommendation,
    RecommendationResult,
    SoilRecord,
)
from backend.rules.agronomic_rules import evaluate_crop_against_rules
from backend.schemas import (
    DimensionScoresSchema,
    RecommendationRequest,
    RecommendationResponse,
    RecommendedCropResultSchema,
)
from ml.predictor import CropMLPredictor, ModelLoadError

SCORING_NOTICE_EN = (
    "Suitability scores are illustrative prototype indices combining documented agronomic compatibility "
    "and (where complete soil/climate parameters are supplied) Random Forest class probabilities. "
    "They are not scientifically validated yield guarantees."
)
SCORING_NOTICE_KN = (
    "ಸೂಚ್ಯಂಕ ಅಂಕಗಳು ಕೃಷಿ ನಿಯಮಗಳು ಮತ್ತು (ಪೂರ್ಣ ಮಣ್ಣು-ಹವಾಮಾನ ದತ್ತಾಂಶ ನೀಡಿದಾಗ) ಯಂತ್ರ ಕಲಿಕೆ ಮಾದರಿಯನ್ನು ಸಂಯೋಜಿಸುವ "
    "ಮಾದರಿ ಮಾರ್ಗಸೂಚಿಗಳಾಗಿವೆ; ಇವು ವೈಜ್ಞಾನಿಕ ಇಳುವರಿ ಖಾತರಿಯಲ್ಲ."
)
DISCLAIMER_EN = (
    "Decision-support guidance only. Confirm crop selection, variety, fertilizer dose, and pest management "
    "with your nearest Raitha Samparka Kendra (RSK) or Krishi Vigyan Kendra (KVK) before sowing."
)
DISCLAIMER_KN = (
    "ಇದು ಕೇವಲ ಕೃಷಿ ನಿರ್ಧಾರ-ಸಹಾಯಕ ಮಾಹಿತಿ ಮಾತ್ರ. ಬಿತ್ತನೆಗೆ ಮುನ್ನ ನಿಮ್ಮ ಹತ್ತಿರದ ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರ (RSK) ಅಥವಾ "
    "ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರ (KVK) ತಜ್ಞರ ಸಲಹೆ ಪಡೆಯಿರಿ."
)


def _check_biological_viability(payload: RecommendationRequest) -> str | None:
    """Detect extreme non-arable inputs where no field crop can be responsibly recommended."""
    if payload.ph is not None and (payload.ph < 3.5 or payload.ph > 10.0):
        return (
            f"Soil pH {payload.ph:.1f} is severely outside the arable agricultural range (3.5-10.0). "
            "Laboratory re-testing and specialist soil reclamation advice are required before crop selection."
        )
    if payload.temperature is not None and (payload.temperature < 2.0 or payload.temperature > 48.0):
        return (
            f"Ambient temperature {payload.temperature:.1f}°C lies outside standard Karnataka open-field crop limits. "
            "Verify temperature units (°C) and seasonal timing."
        )
    return None


def generate_recommendation(
    db: Session,
    payload: RecommendationRequest,
    predictor: CropMLPredictor,
) -> RecommendationResponse:
    """Validate location, run ML + rule engine, persist records, and return up to 3 ranked crops."""
    # Verify location exists in structured Karnataka reference (prevent unsupported locations)
    location = (
        db.query(Location)
        .filter(
            Location.state.ilike(payload.state.strip()),
            Location.district.ilike(payload.district.strip()),
            Location.taluk.ilike(payload.taluk.strip()),
        )
        .first()
    )
    if location is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=(
                f"Unsupported or unrecognized location: {payload.state} / {payload.district} / {payload.taluk}. "
                "Please select a supported State, District, and Taluk."
            ),
        )

    missing_fields: list[str] = []
    warnings: list[str] = []

    if not payload.soil_data_available or payload.soil_measurement_source == "unavailable":
        missing_fields.extend(["ph", "nitrogen", "phosphorus", "potassium"])
        warnings.append(
            "Reduced-information mode: soil chemistry values were marked unavailable; recommendations rely on "
            "soil type, regional agro-climatic rules, season, and water availability."
        )
    else:
        for fname in ("ph", "nitrogen", "phosphorus", "potassium"):
            if getattr(payload, fname) is None:
                missing_fields.append(fname)
        if missing_fields:
            warnings.append(
                f"Partial soil data: missing {', '.join(missing_fields)}. Confidence is reduced until lab soil test values are supplied."
            )
        elif payload.soil_measurement_source == "estimate":
            warnings.append(
                "Soil pH/NPK were entered as approximate estimates rather than a formal lab Soil Health Card."
            )

    climate_missing: list[str] = []
    for cname in ("temperature", "humidity", "rainfall"):
        if getattr(payload, cname) is None:
            climate_missing.append(cname)
            missing_fields.append(cname)

    if climate_missing:
        warnings.append(
            f"Missing climate fields ({', '.join(climate_missing)}). Using taluk reference rainfall "
            f"({location.normal_annual_rainfall_mm} mm/yr) where applicable instead of live weather."
        )
    elif payload.climate_source == "estimate":
        warnings.append(
            "Climate parameters are user-entered estimates; SmartKrishi is not connected to a live weather feed."
        )

    reduced_info = bool(missing_fields) or not payload.soil_data_available

    # Check if ML model is required & healthy
    ml_probs: dict[str, float] = {}
    metrics = predictor.get_metrics()
    model_version = f"rf_v1_acc_{metrics['test_accuracy']:.3f}" if metrics else "rf_v1"

    try:
        predictor.ensure_loaded()
    except ModelLoadError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Recommendation ML engine unavailable: {exc}",
        ) from exc

    if not reduced_info and payload.ph is not None and payload.nitrogen is not None and payload.phosphorus is not None and payload.potassium is not None and payload.temperature is not None and payload.humidity is not None and payload.rainfall is not None:
        predictions = predictor.predict_probabilities(
            nitrogen=payload.nitrogen,
            phosphorus=payload.phosphorus,
            potassium=payload.potassium,
            temperature=payload.temperature,
            humidity=payload.humidity,
            ph=payload.ph,
            rainfall=payload.rainfall,
        )
        ml_probs = {p.crop_key: p.probability for p in predictions}

    # Persist anonymized farmer session + soil + farm profile
    farmer = Farmer(session_label="web-session", preferred_language=payload.language)
    db.add(farmer)
    db.flush()

    soil_record = SoilRecord(
        farmer_id=farmer.id,
        location_id=location.id,
        soil_type=payload.soil_type,
        ph=payload.ph,
        nitrogen=payload.nitrogen,
        phosphorus=payload.phosphorus,
        potassium=payload.potassium,
        measurement_source="unavailable" if not payload.soil_data_available else payload.soil_measurement_source,
        soil_test_date=payload.soil_test_date,
    )
    db.add(soil_record)

    farm_profile = FarmProfile(
        farmer_id=farmer.id,
        location_id=location.id,
        village=payload.village,
        season=payload.season,
        irrigation_type=payload.irrigation_type,
        water_availability=payload.water_availability,
        land_area_acres=payload.land_area_acres,
        farming_method=payload.farming_method,
        previous_crop=payload.previous_crop,
        temperature_c=payload.temperature,
        humidity_pct=payload.humidity,
        rainfall_mm=payload.rainfall,
        climate_source=payload.climate_source,
    )
    db.add(farm_profile)
    db.flush()

    # Extreme non-arable check -> do not force recommendation
    viability_issue = _check_biological_viability(payload)
    if viability_issue is not None:
        rec = Recommendation(
            farmer_id=farmer.id,
            location_id=location.id,
            soil_record_id=soil_record.id,
            farm_profile_id=farm_profile.id,
            mode_used="insufficient_data",
            confidence_level="insufficient",
            input_snapshot=payload.model_dump(mode="json"),
            warnings=warnings,
            insufficient_data_reason=viability_issue,
            model_version=model_version,
        )
        db.add(rec)
        db.commit()
        db.refresh(rec)
        return _build_response(rec, location, payload, [], missing_fields)

    crops = (
        db.query(Crop)
        .options(joinedload(Crop.requirement), joinedload(Crop.regional_rules))
        .filter(Crop.is_active.is_(True))
        .all()
    )

    inputs_dict = payload.model_dump()
    candidates = []
    excluded_notes = []

    for crop in crops:
        evaluated = evaluate_crop_against_rules(
            crop=crop,
            location=location,
            rules=crop.regional_rules,
            inputs=inputs_dict,
            ml_probability=ml_probs.get(crop.crop_key),
            reduced_info=reduced_info,
        )
        if evaluated.hard_excluded:
            excluded_notes.append((crop.name_en, evaluated.exclusion_reason_en))
        else:
            candidates.append(evaluated)

    # Filter out clearly unviable low scores (< 45)
    viable = [c for c in candidates if c.illustrative_score >= 45.0]
    viable.sort(
        key=lambda c: (
            len(c.conflict_flags) == 0,
            c.illustrative_score,
            c.ml_probability or 0.0,
        ),
        reverse=True,
    )
    top_crops = viable[:3]

    if not top_crops:
        reason = (
            "No crop cleared the minimum agronomic compatibility threshold for the entered combination of "
            f"season ({payload.season}), water availability ({payload.water_availability}), soil type ({payload.soil_type}), "
            "and soil/climatic measurements. Please review constraints or consult local agricultural experts."
        )
        rec = Recommendation(
            farmer_id=farmer.id,
            location_id=location.id,
            soil_record_id=soil_record.id,
            farm_profile_id=farm_profile.id,
            mode_used="insufficient_data",
            confidence_level="insufficient",
            input_snapshot=payload.model_dump(mode="json"),
            warnings=warnings,
            insufficient_data_reason=reason,
            model_version=model_version,
        )
        db.add(rec)
        db.commit()
        db.refresh(rec)
        return _build_response(rec, location, payload, [], missing_fields)

    mode_used = "reduced_information" if reduced_info else "hybrid_full"
    confidence_level = "reduced" if reduced_info else ("moderate" if all(not c.conflict_flags for c in top_crops) else "reduced")

    rec = Recommendation(
        farmer_id=farmer.id,
        location_id=location.id,
        soil_record_id=soil_record.id,
        farm_profile_id=farm_profile.id,
        mode_used=mode_used,
        confidence_level=confidence_level,
        input_snapshot=payload.model_dump(mode="json"),
        warnings=warnings,
        insufficient_data_reason=None,
        model_version=model_version,
    )
    db.add(rec)
    db.flush()

    result_schemas: list[RecommendedCropResultSchema] = []
    for idx, cand in enumerate(top_crops, start=1):
        res_row = RecommendationResult(
            recommendation_id=rec.id,
            crop_id=cand.crop.id,
            rank=idx,
            suitability_category=cand.suitability_category,
            illustrative_score=cand.illustrative_score,
            ml_probability=cand.ml_probability,
            dimension_scores=cand.dimension_scores,
            reasons_en=cand.reasons_en,
            reasons_kn=cand.reasons_kn,
            limitations_en=cand.limitations_en,
            limitations_kn=cand.limitations_kn,
            conflict_flags=cand.conflict_flags,
        )
        db.add(res_row)
        result_schemas.append(_candidate_to_schema(idx, cand))

    db.commit()
    db.refresh(rec)
    return _build_response(rec, location, payload, result_schemas, missing_fields)


def get_recommendation_by_id(db: Session, recommendation_id: int) -> RecommendationResponse:
    rec = (
        db.query(Recommendation)
        .options(
            joinedload(Recommendation.results).joinedload(RecommendationResult.crop).joinedload(Crop.requirement),
        )
        .filter(Recommendation.id == recommendation_id)
        .first()
    )
    if rec is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation record not found.")

    location = db.query(Location).filter(Location.id == rec.location_id).first() if rec.location_id else None
    snapshot = rec.input_snapshot or {}
    payload = RecommendationRequest(**snapshot)
    missing_fields = [f for f in ("ph", "nitrogen", "phosphorus", "potassium", "temperature", "humidity", "rainfall") if snapshot.get(f) is None]

    results = []
    for r in rec.results:
        req = r.crop.requirement
        results.append(
            RecommendedCropResultSchema(
                rank=r.rank,
                crop_id=r.crop.id,
                crop_key=r.crop.crop_key,
                name_en=r.crop.name_en,
                name_kn=r.crop.name_kn,
                scientific_name=r.crop.scientific_name,
                category=r.crop.category,
                image_asset=r.crop.image_asset,
                suitability_category=r.suitability_category,
                illustrative_score=r.illustrative_score,
                ml_probability=r.ml_probability,
                dimension_scores=DimensionScoresSchema(**r.dimension_scores),
                reasons_en=r.reasons_en,
                reasons_kn=r.reasons_kn,
                limitations_en=r.limitations_en,
                limitations_kn=r.limitations_kn,
                conflict_flags=r.conflict_flags,
                water_requirement_level=r.crop.water_requirement_level,
                water_requirement_mm_min=r.crop.water_requirement_mm_min,
                water_requirement_mm_max=r.crop.water_requirement_mm_max,
                suitable_seasons=req.suitable_seasons if req else [],
                growing_duration_days_min=r.crop.growing_duration_days_min,
                growing_duration_days_max=r.crop.growing_duration_days_max,
                cultivation_guidance_en=r.crop.cultivation_guidance_en,
                cultivation_guidance_kn=r.crop.cultivation_guidance_kn,
                information_source=r.crop.information_source,
                record_status=r.crop.record_status,
            )
        )

    return _build_response(rec, location, payload, results, missing_fields)


def _candidate_to_schema(rank: int, cand) -> RecommendedCropResultSchema:
    req = cand.crop.requirement
    return RecommendedCropResultSchema(
        rank=rank,
        crop_id=cand.crop.id,
        crop_key=cand.crop.crop_key,
        name_en=cand.crop.name_en,
        name_kn=cand.crop.name_kn,
        scientific_name=cand.crop.scientific_name,
        category=cand.crop.category,
        image_asset=cand.crop.image_asset,
        suitability_category=cand.suitability_category,
        illustrative_score=cand.illustrative_score,
        ml_probability=cand.ml_probability,
        dimension_scores=DimensionScoresSchema(**cand.dimension_scores),
        reasons_en=cand.reasons_en,
        reasons_kn=cand.reasons_kn,
        limitations_en=cand.limitations_en,
        limitations_kn=cand.limitations_kn,
        conflict_flags=cand.conflict_flags,
        water_requirement_level=cand.crop.water_requirement_level,
        water_requirement_mm_min=cand.crop.water_requirement_mm_min,
        water_requirement_mm_max=cand.crop.water_requirement_mm_max,
        suitable_seasons=req.suitable_seasons if req else [],
        growing_duration_days_min=cand.crop.growing_duration_days_min,
        growing_duration_days_max=cand.crop.growing_duration_days_max,
        cultivation_guidance_en=cand.crop.cultivation_guidance_en,
        cultivation_guidance_kn=cand.crop.cultivation_guidance_kn,
        information_source=cand.crop.information_source,
        record_status=cand.crop.record_status,
    )


def _build_response(
    rec: Recommendation,
    location: Location | None,
    payload: RecommendationRequest,
    results: list[RecommendedCropResultSchema],
    missing_fields: list[str],
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
        insufficient_data_reason=rec.insufficient_data_reason,
        missing_fields=sorted(set(missing_fields)),
        location_context={
            "state": location.state if location else payload.state,
            "district": location.district if location else payload.district,
            "taluk": location.taluk if location else payload.taluk,
            "village": payload.village,
            "agro_climatic_zone": location.agro_climatic_zone if location else payload.agro_climatic_zone,
            "zone_code": location.zone_code if location else None,
            "normal_annual_rainfall_mm": location.normal_annual_rainfall_mm if location else None,
            "dominant_soil_types": location.dominant_soil_types if location else [],
        },
        input_summary={
            "soil_type": payload.soil_type,
            "soil_measurement_source": payload.soil_measurement_source,
            "soil_data_available": payload.soil_data_available,
            "ph": payload.ph,
            "nitrogen": payload.nitrogen,
            "phosphorus": payload.phosphorus,
            "potassium": payload.potassium,
            "season": payload.season,
            "irrigation_type": payload.irrigation_type,
            "water_availability": payload.water_availability,
            "land_area_acres": payload.land_area_acres,
            "farming_method": payload.farming_method,
            "previous_crop": payload.previous_crop,
            "temperature": payload.temperature,
            "humidity": payload.humidity,
            "rainfall": payload.rainfall,
            "climate_source": payload.climate_source,
        },
        recommendations=results,
    )
