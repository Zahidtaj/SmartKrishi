"""Location hierarchy API routes (States -> Districts -> Taluks & Agro-Climatic Zones)."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Location
from backend.schemas import DistrictItem, DistrictListResponse, StateListResponse, TalukItem, TalukListResponse

router = APIRouter(prefix="/api/locations", tags=["Locations"])


@router.get("/states", response_model=StateListResponse)
def list_states(db: Session = Depends(get_db)) -> StateListResponse:
    rows = db.query(Location.state).distinct().order_by(Location.state.asc()).all()
    return StateListResponse(states=[r[0] for r in rows])


@router.get("/districts", response_model=DistrictListResponse)
def list_districts(
    state: str = Query(default="Karnataka", min_length=2),
    db: Session = Depends(get_db),
) -> DistrictListResponse:
    rows = (
        db.query(
            Location.district,
            func.min(Location.agro_climatic_zone),
            func.min(Location.zone_code),
            func.count(Location.id),
        )
        .filter(Location.state.ilike(state.strip()))
        .group_by(Location.district)
        .order_by(Location.district.asc())
        .all()
    )
    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No supported districts found for state '{state}'.",
        )
    return DistrictListResponse(
        state=state.strip(),
        districts=[
            DistrictItem(
                district=r[0],
                agro_climatic_zone=r[1],
                zone_code=r[2],
                taluk_count=int(r[3]),
            )
            for r in rows
        ],
    )


@router.get("/taluks", response_model=TalukListResponse)
def list_taluks(
    state: str = Query(default="Karnataka", min_length=2),
    district: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
) -> TalukListResponse:
    rows = (
        db.query(Location)
        .filter(Location.state.ilike(state.strip()), Location.district.ilike(district.strip()))
        .order_by(Location.taluk.asc())
        .all()
    )
    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No taluks found for {district} in {state}.",
        )
    return TalukListResponse(
        state=rows[0].state,
        district=rows[0].district,
        taluks=[
            TalukItem(
                id=r.id,
                taluk=r.taluk,
                agro_climatic_zone=r.agro_climatic_zone,
                zone_code=r.zone_code,
                normal_annual_rainfall_mm=r.normal_annual_rainfall_mm,
                typical_rainfall_pattern=r.typical_rainfall_pattern,
                dominant_soil_types=r.dominant_soil_types or [],
                common_soil_textures=r.common_soil_textures or [],
                major_crops=r.major_crops or [],
                recommended_seasons_summary=r.recommended_seasons_summary or {},
                growing_period_info=r.growing_period_info,
                regional_references=r.regional_references or [],
                data_source=r.data_source,
                verification_status=r.verification_status,
                last_updated=r.last_updated,
            )
            for r in rows
        ],
    )
