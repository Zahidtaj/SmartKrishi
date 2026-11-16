from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# --- Location Schemas ---
class AgroClimaticZoneResponse(BaseModel):
    id: int
    code: str
    name: str
    kannada_name: Optional[str] = None
    headquarters: Optional[str] = None
    climate_description: Optional[str] = None
    annual_rainfall_min_mm: Optional[float] = None
    annual_rainfall_max_mm: Optional[float] = None
    normal_rainfall_mm: Optional[float] = None
    major_soils: Optional[List[str]] = []
    primary_crops: Optional[List[str]] = []
    critical_risks: Optional[List[str]] = []
    verification_status: str

class DistrictResponse(BaseModel):
    id: int
    name: str
    kannada_name: Optional[str] = None
    zone_id: int
    secondary_zone_id: Optional[int] = None
    headquarters: Optional[str] = None
    latitude: float
    longitude: float
    normal_rainfall_mm: Optional[float] = None
    dominant_soils: Optional[List[str]] = []
    drainage_profile: Optional[str] = None
    drought_vulnerability: Optional[str] = None
    taluks: Optional[List[str]] = []

class TalukResponse(BaseModel):
    id: int
    name: str
    kannada_name: Optional[str] = None
    district_id: int
    zone_id: Optional[int] = None

class StateResponse(BaseModel):
    id: int
    code: str
    name: str
    kannada_name: Optional[str] = None
    districts: List[str] = []

# --- Soil Observation Schemas ---
class SoilObservationInput(BaseModel):
    soil_colour: str = Field(default="Unknown", description="Red, Dark black, Brown, Yellowish, Grey, Light sandy, Mixed, Unknown")
    soil_texture: str = Field(default="Unknown", description="Sandy, Clayey, Loamy, Silty, Mixed, Unknown")
    drainage: str = Field(default="Unknown", description="Water drains quickly, moderately, remains for several hours, days, Unknown")
    moisture_retention: str = Field(default="Unknown", description="Soil dries quickly, short period, several days, Unknown")
    soil_depth: str = Field(default="Unknown", description="Shallow (<25cm), Medium (25-75cm), Deep (>75cm), Unknown")
    presence_of_stones: bool = False
    rocky_ground: bool = False
    surface_erosion: bool = False
    waterlogging_observed: bool = False
    land_condition_notes: Optional[str] = None

class LandProfileInput(BaseModel):
    slope_type: str = Field(default="Flat land", description="Flat land, Slightly sloping land, Steep or hilly land, Low-lying land, Rocky land")
    approximate_area_acres: float = Field(default=1.0, ge=0.1)

class WaterAvailabilityInput(BaseModel):
    irrigation_source: str = Field(default="Rainfed farming", description="Rainfed farming, Borewell, Open well, Canal irrigation, Farm pond, Reservoir, Drip irrigation, Multiple irrigation sources, Other")
    availability_duration: str = Field(default="Throughout season", description="Throughout season, Water available during certain months, Limited water availability, Uncertain availability")
    has_drip_facility: bool = False

class FarmingHistoryInput(BaseModel):
    previous_crop: Optional[str] = None
    previous_season: Optional[str] = None
    was_successful: bool = True
    approximate_yield: Optional[str] = None
    drought_affected: bool = False
    flood_affected: bool = False
    recurring_pest_problem: Optional[str] = None
    water_shortage_encountered: bool = False

# --- Recommendation Schemas ---
class RecommendationRequest(BaseModel):
    state: str = "Karnataka"
    district: str
    taluk: str
    village: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    soil_observation: SoilObservationInput = Field(default_factory=SoilObservationInput)
    water_availability: WaterAvailabilityInput = Field(default_factory=WaterAvailabilityInput)
    land_profile: LandProfileInput = Field(default_factory=LandProfileInput)
    farming_history: Optional[FarmingHistoryInput] = None
    planned_season: str = Field(default="Kharif", description="Kharif, Rabi, Summer")
    planned_sowing_month: Optional[str] = None
    duration_preference: Optional[str] = "Any"
    farming_objective: Optional[str] = "High Yield & Stability"

class FilteredCropInfo(BaseModel):
    crop_id: str
    crop_name: str
    reason_for_exclusion: str
    constraint_type: str  # Hard Constraint / Agronomic Incompatibility

class RecommendedCropItem(BaseModel):
    crop_id: str
    crop_name: str
    kannada_name: Optional[str] = None
    scientific_name: Optional[str] = None
    category: str
    rank: int
    suitability_score: float
    suitability_tier: str
    sub_scores: Dict[str, float]
    reasons_for_selection: List[str]
    supporting_soil_observations: List[str]
    water_sufficiency_notes: str
    climate_suitability_notes: str
    potential_risks: List[str]
    crucial_practices: str
    data_uncertainty_notes: Optional[str] = None
    water_requirement_mm: Dict[str, Any]
    duration_days: Dict[str, Any]
    economics: Optional[Dict[str, Any]] = None

class RecommendationResponse(BaseModel):
    recommendation_id: int
    location: Dict[str, Any]
    agro_climatic_zone: Dict[str, Any]
    weather_summary: Dict[str, Any]
    reliability_score_pct: float
    data_completeness_pct: float
    missing_fields: List[str]
    recommendations: List[RecommendedCropItem]
    filtered_crops: List[FilteredCropInfo]
    agricultural_disclaimer: str

# --- Crop Comparison Schemas ---
class CompareRequest(BaseModel):
    crop_ids: List[str] = Field(..., min_items=2, max_items=3)

class CropComparisonItem(BaseModel):
    crop_id: str
    crop_name: str
    kannada_name: Optional[str]
    scientific_name: Optional[str]
    category: str
    suitable_zones: List[int]
    preferred_soil_textures: List[str]
    drainage_preference: str
    water_requirement_mm: Dict[str, Any]
    water_scarcity_tolerance: str
    temperature_range_c: str
    rainfall_range_mm: str
    duration_days: Dict[str, Any]
    suitable_seasons: List[str]
    key_risks: List[str]
    cultivation_practices: str
    economics: Optional[Dict[str, Any]] = None

class CompareResponse(BaseModel):
    crops: List[CropComparisonItem]
    comparison_summary: str
    comparison_timestamp: str

# --- Weather & Advisory Schemas ---
class WeatherResponse(BaseModel):
    location: str
    latitude: float
    longitude: float
    current_temperature_c: float
    relative_humidity_pct: float
    wind_speed_kmh: float
    recent_precipitation_mm: float
    condition: str
    source: str
    retrieval_timestamp: str
    is_live_data: bool
    forecast_7_day: List[Dict[str, Any]] = []

class AdvisoryResponse(BaseModel):
    id: int
    title: str
    kannada_title: Optional[str]
    advisory_type: str
    severity: str
    message: str
    kannada_message: Optional[str]
    source: str
    valid_from: Optional[str]
    valid_until: Optional[str]

# --- Knowledge & Feedback ---
class KnowledgeArticleResponse(BaseModel):
    id: int
    title: str
    kannada_title: Optional[str]
    category: str
    summary: str
    content: str
    source: str
    publication_date: Optional[str]
    geographic_applicability: str

class FeedbackRequest(BaseModel):
    recommendation_id: Optional[int] = None
    district: Optional[str] = None
    crop_selected: Optional[str] = None
    rating: int = Field(..., ge=1, le=5)
    was_helpful: bool = True
    feedback_notes: Optional[str] = None
