"""Weather and regional climate advisory endpoint."""

from typing import Any, Literal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Location
from backend.services.soil_observation_service import interpret_soil_observations
from backend.services.weather_service import get_weather_intelligence

router = APIRouter(prefix="/api/weather", tags=["Weather & Climate"])


@router.get("/advisory")
def get_regional_weather_advisory(
    state: str = Query(default="Karnataka"),
    district: str = Query(...),
    taluk: str = Query(...),
    season: Literal["Kharif", "Rabi", "Zaid", "Perennial"] = Query(default="Kharif"),
    water_source: str = Query(default="rainfed"),
    water_reliability: str = Query(default="uncertain"),
    soil_texture: str = Query(default="not_sure"),
    drainage_after_rain: str = Query(default="not_sure"),
    simulate_unavailable: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    location = (
        db.query(Location)
        .filter(
            Location.state.ilike(state.strip()),
            Location.district.ilike(district.strip()),
            Location.taluk.ilike(taluk.strip()),
        )
        .first()
    )
    if location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location '{taluk}, {district}, {state}' not found.",
        )

    soil_obs = interpret_soil_observations(
        soil_texture=soil_texture,
        drainage_after_rain=drainage_after_rain,
    )
    return get_weather_intelligence(
        location=location,
        season=season,
        soil_observation=soil_obs,
        water_source=water_source,
        water_reliability=water_reliability,
        force_live_unavailable=simulate_unavailable,
    )
