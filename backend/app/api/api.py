import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.models.models import (
    State, District, Taluk, AgroClimaticZone, Crop,
    Recommendation, RecommendationResult, SoilObservation,
    LandProfile, WaterAvailability, FarmingHistory,
    FarmerFeedback
)
from backend.app.schemas.schemas import (
    AgroClimaticZoneResponse, DistrictResponse, TalukResponse, StateResponse,
    RecommendationRequest, RecommendationResponse, RecommendedCropItem,
    CompareRequest, CompareResponse, WeatherResponse, AdvisoryResponse,
    KnowledgeArticleResponse, FeedbackRequest
)
from backend.app.services.location_service import location_service
from backend.app.services.weather_service import weather_service
from backend.app.services.rule_engine import rule_engine
from backend.app.services.scoring_service import scoring_service
from backend.app.services.explanation_service import explanation_service
from backend.app.services.comparison_service import comparison_service
from backend.app.services.advisory_service import advisory_service
from backend.app.services.knowledge_service import knowledge_service

router = APIRouter()

# --- Health Check ---
@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """System health check and diagnostic status."""
    try:
        dist_count = db.query(District).count()
        crop_count = db.query(Crop).count()
        return {
            "status": "healthy",
            "system": "SmartKrishi Decision Support System",
            "version": "1.0.0",
            "target_state": "Karnataka",
            "districts_loaded": dist_count,
            "crops_loaded": crop_count,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connectivity issue: {str(e)}")

# --- Locations ---
@router.get("/locations/states", response_model=List[StateResponse])
def get_states(db: Session = Depends(get_db)):
    states = db.query(State).all()
    res = []
    for s in states:
        res.append(StateResponse(
            id=s.id,
            code=s.code,
            name=s.name,
            kannada_name=s.kannada_name,
            districts=[d.name for d in s.districts]
        ))
    return res

@router.get("/locations/districts", response_model=List[DistrictResponse])
def get_districts(db: Session = Depends(get_db)):
    return location_service.get_all_districts(db)

@router.get("/locations/taluks", response_model=List[TalukResponse])
def get_taluks(district: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Taluk)
    if district:
        dist_obj = db.query(District).filter(District.name.ilike(district.strip())).first()
        if dist_obj:
            query = query.filter(Taluk.district_id == dist_obj.id)
        else:
            return []
    taluks = query.order_by(Taluk.name).all()
    return [
        TalukResponse(
            id=t.id,
            name=t.name,
            kannada_name=t.kannada_name,
            district_id=t.district_id,
            zone_id=t.zone_id
        )
        for t in taluks
    ]

@router.get("/locations/zones", response_model=List[AgroClimaticZoneResponse])
def get_zones(db: Session = Depends(get_db)):
    return location_service.get_all_zones(db)

@router.get("/locations/resolve")
def resolve_location(
    district: Optional[str] = None,
    taluk: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    db: Session = Depends(get_db)
):
    if lat is not None and lon is not None:
        gps_match = location_service.resolve_gps_coordinates(lat, lon, db)
        if gps_match:
            return gps_match
    if district:
        return location_service.resolve_location(district, taluk, db)
    raise HTTPException(status_code=400, detail="Provide either district name or latitude/longitude coordinates.")

# --- Soil Characteristics Guide ---
@router.get("/soil/characteristics")
def get_soil_characteristics():
    return knowledge_service.get_soil_reference()

# --- Crops ---
@router.get("/crops")
def get_crops():
    return rule_engine.get_all_crops()

@router.get("/crops/{crop_id}")
def get_crop_details(crop_id: str):
    crop = rule_engine.get_crop_by_id(crop_id)
    if not crop:
        raise HTTPException(status_code=404, detail=f"Crop with ID '{crop_id}' not found.")
    return crop

# --- Recommendations ---
@router.post("/recommendations", response_model=RecommendationResponse)
async def generate_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    # 1. Resolve Location & Agro-Climatic Zone
    loc = location_service.resolve_location(request.district, request.taluk, db)

    # 2. Retrieve Weather (Open-Meteo live API with IMD normal fallback)
    weather = await weather_service.get_weather_for_location(
        district_name=loc["district"],
        lat=loc["latitude"],
        lon=loc["longitude"],
        normal_rainfall_mm=loc["normal_rainfall_mm"]
    )

    # 3. Prepare Input Dicts
    soil_dict = request.soil_observation.model_dump()
    water_dict = request.water_availability.model_dump()
    land_dict = request.land_profile.model_dump()
    history_dict = request.farming_history.model_dump() if request.farming_history else None

    # 4. Run Rule Engine & Scoring
    recommended_candidates, filtered_crops, data_quality = scoring_service.evaluate_candidates(
        location=loc,
        soil_obs=soil_dict,
        water_avail=water_dict,
        land_profile=land_dict,
        season=request.planned_season,
        weather=weather,
        farming_history=history_dict
    )

    # 5. Persist Recommendation Session in DB
    rec_record = Recommendation(
        state=request.state,
        district=loc["district"],
        taluk=loc["taluk"],
        village=request.village,
        zone_id=loc["zone_id"],
        planned_season=request.planned_season,
        planned_sowing_month=request.planned_sowing_month,
        farming_objective=request.farming_objective,
        reliability_score_pct=data_quality["reliability_score_pct"],
        data_completeness_pct=data_quality["completeness_pct"],
        missing_fields=data_quality["missing_fields"]
    )
    db.add(rec_record)
    db.commit()
    db.refresh(rec_record)

    # Persist Observations
    soil_record = SoilObservation(
        recommendation_id=rec_record.id,
        soil_colour=soil_dict.get("soil_colour"),
        soil_texture=soil_dict.get("soil_texture"),
        drainage=soil_dict.get("drainage"),
        moisture_retention=soil_dict.get("moisture_retention"),
        soil_depth=soil_dict.get("soil_depth"),
        presence_of_stones=soil_dict.get("presence_of_stones", False),
        rocky_ground=soil_dict.get("rocky_ground", False),
        surface_erosion=soil_dict.get("surface_erosion", False),
        waterlogging_observed=soil_dict.get("waterlogging_observed", False),
        land_condition_notes=soil_dict.get("land_condition_notes")
    )
    db.add(soil_record)

    water_record = WaterAvailability(
        recommendation_id=rec_record.id,
        irrigation_source=water_dict.get("irrigation_source"),
        availability_duration=water_dict.get("availability_duration"),
        has_drip_facility=water_dict.get("has_drip_facility", False)
    )
    db.add(water_record)

    land_record = LandProfile(
        recommendation_id=rec_record.id,
        slope_type=land_dict.get("slope_type"),
        approximate_area_acres=land_dict.get("approximate_area_acres", 1.0)
    )
    db.add(land_record)
    db.commit()

    # 6. Format Detailed Recommendations with Explanations
    recommendation_items: List[RecommendedCropItem] = []
    for cand in recommended_candidates:
        crop = cand["crop"]
        expl = explanation_service.generate_explanation(
            candidate=cand,
            location=loc,
            soil_obs=soil_dict,
            water_avail=water_dict,
            season=request.planned_season,
            weather=weather,
            missing_fields=data_quality["missing_fields"]
        )

        # Persist Result Item
        res_item = RecommendationResult(
            recommendation_id=rec_record.id,
            crop_id=crop["id"],
            rank=cand["rank"],
            suitability_score=cand["suitability_score"],
            suitability_tier=cand["suitability_tier"],
            regional_score=cand["sub_scores"]["regional_score"],
            soil_score=cand["sub_scores"]["soil_score"],
            drainage_score=cand["sub_scores"]["drainage_score"],
            water_score=cand["sub_scores"]["water_score"],
            climate_score=cand["sub_scores"]["climate_score"],
            season_score=cand["sub_scores"]["season_score"],
            reasons_for_selection=expl["reasons_for_selection"],
            supporting_soil_observations=expl["supporting_soil_observations"],
            water_sufficiency_notes=expl["water_sufficiency_notes"],
            climate_suitability_notes=expl["climate_suitability_notes"],
            potential_risks=expl["potential_risks"],
            crucial_practices=expl["crucial_practices"],
            data_uncertainty_notes=expl["data_uncertainty_notes"]
        )
        db.add(res_item)

        recommendation_items.append(
            RecommendedCropItem(
                crop_id=crop["id"],
                crop_name=crop["crop_name"],
                kannada_name=crop.get("kannada_name"),
                scientific_name=crop.get("scientific_name"),
                category=crop.get("category", "Field Crop"),
                rank=cand["rank"],
                suitability_score=cand["suitability_score"],
                suitability_tier=cand["suitability_tier"],
                sub_scores=cand["sub_scores"],
                reasons_for_selection=expl["reasons_for_selection"],
                supporting_soil_observations=expl["supporting_soil_observations"],
                water_sufficiency_notes=expl["water_sufficiency_notes"],
                climate_suitability_notes=expl["climate_suitability_notes"],
                potential_risks=expl["potential_risks"],
                crucial_practices=expl["crucial_practices"],
                data_uncertainty_notes=expl["data_uncertainty_notes"],
                water_requirement_mm=crop.get("water_requirement_mm", {}),
                duration_days=crop.get("duration_days", {}),
                economics=crop.get("economics")
            )
        )
    db.commit()

    return RecommendationResponse(
        recommendation_id=rec_record.id,
        location=loc,
        agro_climatic_zone={
            "id": loc["zone_id"],
            "name": loc["zone_name"],
            "code": loc["zone_code"],
            "kannada_name": loc.get("zone_kannada_name")
        },
        weather_summary={
            "source": weather["source"],
            "is_live_data": weather["is_live_data"],
            "temperature_c": weather["current_temperature_c"],
            "condition": weather["condition"],
            "retrieval_timestamp": weather["retrieval_timestamp"],
            "forecast_7_day": weather.get("forecast_7_day", [])
        },
        reliability_score_pct=data_quality["reliability_score_pct"],
        data_completeness_pct=data_quality["completeness_pct"],
        missing_fields=data_quality["missing_fields"],
        recommendations=recommendation_items,
        filtered_crops=filtered_crops,
        agricultural_disclaimer=(
            "SmartKrishi generates advisory recommendations based on observable soil traits, "
            "agro-climatic zone parameters, and official package of practices (UASB / UASD / ICAR). "
            "Local micro-climates, unexpected pest outbreaks, and extreme weather events should be considered "
            "in consultation with local Krishi Vigyan Kendras (KVK) or Raitha Samparka Kendras (RSK)."
        )
    )

@router.get("/recommendations/{rec_id}")
def get_recommendation_by_id(rec_id: int, db: Session = Depends(get_db)):
    rec = db.query(Recommendation).filter_by(id=rec_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation record not found.")
    
    results = db.query(RecommendationResult).filter_by(recommendation_id=rec_id).order_by(RecommendationResult.rank).all()
    return {
        "id": rec.id,
        "district": rec.district,
        "taluk": rec.taluk,
        "zone_id": rec.zone_id,
        "season": rec.planned_season,
        "created_at": rec.created_at,
        "reliability_score_pct": rec.reliability_score_pct,
        "data_completeness_pct": rec.data_completeness_pct,
        "results": [
            {
                "crop_id": r.crop_id,
                "rank": r.rank,
                "suitability_score": r.suitability_score,
                "suitability_tier": r.suitability_tier,
                "reasons": r.reasons_for_selection,
                "risks": r.potential_risks,
                "practices": r.crucial_practices
            }
            for r in results
        ]
    }

# --- Crop Comparison ---
@router.post("/crops/compare", response_model=CompareResponse)
def compare_crops(request: CompareRequest):
    return comparison_service.compare_crops(request.crop_ids)

# --- Weather ---
@router.get("/weather/{location_id}", response_model=WeatherResponse)
async def get_weather(location_id: str, db: Session = Depends(get_db)):
    dist = location_service.get_district_by_name(location_id, db)
    if not dist:
        # Default to Bengaluru if district not recognized
        dist = {
            "name": "Bengaluru",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "normal_rainfall_mm": 860
        }
    weather = await weather_service.get_weather_for_location(
        district_name=dist["name"],
        lat=dist["latitude"],
        lon=dist["longitude"],
        normal_rainfall_mm=dist.get("normal_rainfall_mm", 750)
    )
    return WeatherResponse(**weather)

# --- Advisories ---
@router.get("/advisories/{location_id}", response_model=List[AdvisoryResponse])
async def get_advisories(location_id: str, db: Session = Depends(get_db)):
    loc = location_service.resolve_location(location_id, db=db)
    weather = await weather_service.get_weather_for_location(
        district_name=loc["district"],
        lat=loc["latitude"],
        lon=loc["longitude"],
        normal_rainfall_mm=loc["normal_rainfall_mm"]
    )
    return advisory_service.generate_advisories_for_location(
        district_name=loc["district"],
        zone_id=loc["zone_id"],
        weather=weather
    )

# --- Knowledge & Articles ---
@router.get("/knowledge", response_model=List[KnowledgeArticleResponse])
def get_articles(category: Optional[str] = None):
    return knowledge_service.get_all_articles(category)

@router.get("/knowledge/{article_id}", response_model=KnowledgeArticleResponse)
def get_article(article_id: int):
    art = knowledge_service.get_article_by_id(article_id)
    if not art:
        raise HTTPException(status_code=404, detail="Article not found.")
    return art

@router.get("/sources")
def get_data_sources():
    return knowledge_service.get_all_data_sources()

# --- Feedback ---
@router.post("/feedback")
def submit_feedback(fb: FeedbackRequest, db: Session = Depends(get_db)):
    feedback_record = FarmerFeedback(
        recommendation_id=fb.recommendation_id,
        district=fb.district,
        crop_selected=fb.crop_selected,
        rating=fb.rating,
        was_helpful=fb.was_helpful,
        feedback_notes=fb.feedback_notes
    )
    db.add(feedback_record)
    db.commit()
    return {"status": "success", "message": "Dhanyavadagalu! Thank you for your valuable feedback."}
