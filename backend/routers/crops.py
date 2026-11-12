"""Crops catalog, crop detail, and multi-crop comparison endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from backend.database import get_db
from backend.models import Crop
from backend.schemas import (
    CompareCropsRequest,
    CompareCropsResponse,
    CropDetailSchema,
    CropEconomicSchema,
    CropRequirementSchema,
    CropSummarySchema,
)
from backend.services.comparison_service import compare_crops

router = APIRouter(prefix="/api/crops", tags=["Crops"])


@router.get("", response_model=list[CropSummarySchema])
def list_crops(
    category: str | None = Query(default=None),
    season: str | None = Query(default=None),
    water_level: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[CropSummarySchema]:
    query = db.query(Crop).options(joinedload(Crop.requirement)).filter(Crop.is_active.is_(True))
    if category:
        query = query.filter(Crop.category.ilike(category.strip()))
    if water_level:
        query = query.filter(Crop.water_requirement_level.ilike(water_level.strip()))

    crops = query.order_by(Crop.name_en.asc()).all()
    results: list[CropSummarySchema] = []
    for c in crops:
        req = c.requirement
        seasons = req.suitable_seasons if req else []
        if season and season.strip() not in seasons:
            continue
        results.append(
            CropSummarySchema(
                id=c.id,
                crop_key=c.crop_key,
                name_en=c.name_en,
                name_kn=c.name_kn,
                scientific_name=c.scientific_name,
                category=c.category,
                image_asset=c.image_asset,
                growing_duration_days_min=c.growing_duration_days_min,
                growing_duration_days_max=c.growing_duration_days_max,
                duration_category=c.duration_category,
                water_requirement_level=c.water_requirement_level,
                water_requirement_mm_min=c.water_requirement_mm_min,
                water_requirement_mm_max=c.water_requirement_mm_max,
                seed_rate_kg_per_acre=c.seed_rate_kg_per_acre,
                record_status=c.record_status,
                verification_status=c.verification_status,
                last_updated=c.last_updated,
                in_ml_dataset=c.in_ml_dataset,
                suitable_seasons=seasons,
                suitable_soil_types=req.suitable_soil_types if req else [],
                suitable_textures=req.suitable_textures if req else [],
            )
        )
    return results


@router.get("/{crop_id}", response_model=CropDetailSchema)
def get_crop_detail(crop_id: int, db: Session = Depends(get_db)) -> CropDetailSchema:
    crop = (
        db.query(Crop)
        .options(joinedload(Crop.requirement), joinedload(Crop.economic_data))
        .filter(Crop.id == crop_id, Crop.is_active.is_(True))
        .first()
    )
    if crop is None or crop.requirement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Crop with id {crop_id} not found.")

    req = crop.requirement
    return CropDetailSchema(
        id=crop.id,
        crop_key=crop.crop_key,
        name_en=crop.name_en,
        name_kn=crop.name_kn,
        scientific_name=crop.scientific_name,
        category=crop.category,
        image_asset=crop.image_asset,
        growing_duration_days_min=crop.growing_duration_days_min,
        growing_duration_days_max=crop.growing_duration_days_max,
        duration_category=crop.duration_category,
        water_requirement_level=crop.water_requirement_level,
        water_requirement_mm_min=crop.water_requirement_mm_min,
        water_requirement_mm_max=crop.water_requirement_mm_max,
        seed_rate_kg_per_acre=crop.seed_rate_kg_per_acre,
        record_status=crop.record_status,
        verification_status=crop.verification_status,
        last_updated=crop.last_updated,
        in_ml_dataset=crop.in_ml_dataset,
        suitable_seasons=req.suitable_seasons,
        suitable_soil_types=req.suitable_soil_types,
        suitable_textures=req.suitable_textures,
        cultivation_guidance_en=crop.cultivation_guidance_en,
        cultivation_guidance_kn=crop.cultivation_guidance_kn,
        information_source=crop.information_source,
        requirement=CropRequirementSchema(
            suitable_soil_types=req.suitable_soil_types,
            suitable_textures=req.suitable_textures,
            suitable_drainage=req.suitable_drainage,
            moisture_needs=req.moisture_needs,
            suitable_land_topography=req.suitable_land_topography,
            min_soil_depth=req.min_soil_depth,
            drought_tolerance=req.drought_tolerance,
            waterlogging_tolerance=req.waterlogging_tolerance,
            sowing_months=req.sowing_months,
            temp_min_c=req.temp_min_c,
            temp_max_c=req.temp_max_c,
            humidity_min_pct=req.humidity_min_pct,
            humidity_max_pct=req.humidity_max_pct,
            rainfall_min_mm=req.rainfall_min_mm,
            rainfall_max_mm=req.rainfall_max_mm,
            suitable_seasons=req.suitable_seasons,
            supported_water_levels=req.supported_water_levels,
        ),
        economic_data=[
            CropEconomicSchema(
                region_scope=e.region_scope,
                season=e.season,
                seed_cost_inr_per_acre=e.seed_cost_inr_per_acre,
                cultivation_cost_min_inr_per_acre=e.cultivation_cost_min_inr_per_acre,
                cultivation_cost_max_inr_per_acre=e.cultivation_cost_max_inr_per_acre,
                expected_yield_qtl_min=e.expected_yield_qtl_min,
                expected_yield_qtl_max=e.expected_yield_qtl_max,
                indicative_price_inr_per_qtl=e.indicative_price_inr_per_qtl,
                assumptions_en=e.assumptions_en,
                assumptions_kn=e.assumptions_kn,
                data_status=e.data_status,
                source=e.source,
            )
            for e in crop.economic_data
        ],
    )


@router.post("/compare", response_model=CompareCropsResponse)
def compare_selected_crops(payload: CompareCropsRequest, db: Session = Depends(get_db)) -> CompareCropsResponse:
    return compare_crops(db, payload)
