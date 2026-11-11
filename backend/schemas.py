"""Pydantic schemas for SmartKrishi REST API requests, responses, and standardized errors."""

from datetime import date, datetime
from typing import Any, Literal
from pydantic import BaseModel, Field, field_validator


class ErrorResponse(BaseModel):
    error: str
    detail: str
    code: str
    field_errors: dict[str, str] | None = None


class HealthResponse(BaseModel):
    status: str
    service: str
    database_connected: bool
    ml_model_loaded: bool
    ml_model_version: str | None = None
    record_counts: dict[str, int]


class StateListResponse(BaseModel):
    states: list[str]


class DistrictItem(BaseModel):
    district: str
    agro_climatic_zone: str
    zone_code: str
    taluk_count: int


class DistrictListResponse(BaseModel):
    state: str
    districts: list[DistrictItem]


class TalukItem(BaseModel):
    id: int
    taluk: str
    agro_climatic_zone: str
    zone_code: str
    normal_annual_rainfall_mm: float | None
    dominant_soil_types: list[str]
    data_source: str


class TalukListResponse(BaseModel):
    state: str
    district: str
    taluks: list[TalukItem]


class CropRequirementSchema(BaseModel):
    suitable_soil_types: list[str]
    ph_min: float
    ph_max: float
    ph_optimal_min: float
    ph_optimal_max: float
    nitrogen_min: float
    nitrogen_max: float
    phosphorus_min: float
    phosphorus_max: float
    potassium_min: float
    potassium_max: float
    temp_min_c: float
    temp_max_c: float
    humidity_min_pct: float
    humidity_max_pct: float
    rainfall_min_mm: float
    rainfall_max_mm: float
    suitable_seasons: list[str]
    supported_water_levels: list[str]


class CropEconomicSchema(BaseModel):
    region_scope: str
    season: str
    seed_cost_inr_per_acre: float | None
    cultivation_cost_min_inr_per_acre: float | None
    cultivation_cost_max_inr_per_acre: float | None
    expected_yield_qtl_min: float | None
    expected_yield_qtl_max: float | None
    indicative_price_inr_per_qtl: float | None
    assumptions_en: str
    assumptions_kn: str
    data_status: str
    source: str


class CropSummarySchema(BaseModel):
    id: int
    crop_key: str
    name_en: str
    name_kn: str
    scientific_name: str
    category: str
    image_asset: str
    growing_duration_days_min: int
    growing_duration_days_max: int
    water_requirement_level: str
    water_requirement_mm_min: int
    water_requirement_mm_max: int
    seed_rate_kg_per_acre: str
    record_status: str
    in_ml_dataset: bool
    suitable_seasons: list[str]
    suitable_soil_types: list[str]


class CropDetailSchema(CropSummarySchema):
    cultivation_guidance_en: str
    cultivation_guidance_kn: str
    information_source: str
    requirement: CropRequirementSchema
    economic_data: list[CropEconomicSchema]


class RecommendationRequest(BaseModel):
    state: str = Field(..., min_length=2, max_length=80)
    district: str = Field(..., min_length=2, max_length=80)
    taluk: str = Field(..., min_length=2, max_length=80)
    village: str | None = Field(default=None, max_length=100)
    agro_climatic_zone: str | None = Field(default=None, max_length=120)

    soil_type: Literal["Red", "Black", "Alluvial", "Laterite", "Sandy", "Loamy", "Clay"]
    soil_data_available: bool = True
    soil_measurement_source: Literal["soil_test", "estimate", "unavailable"] = "estimate"
    soil_test_date: date | None = None
    ph: float | None = Field(default=None, ge=0.0, le=14.0)
    nitrogen: float | None = Field(default=None, ge=0.0, le=500.0)
    phosphorus: float | None = Field(default=None, ge=0.0, le=500.0)
    potassium: float | None = Field(default=None, ge=0.0, le=600.0)

    season: Literal["Kharif", "Rabi", "Zaid", "Perennial"]
    irrigation_type: Literal["Rainfed", "Borewell", "Canal", "Drip", "Sprinkler", "Tank / Open Well"]
    water_availability: Literal["Rainfed", "Limited irrigation", "Moderate irrigation", "Assured irrigation"]
    land_area_acres: float = Field(..., gt=0.0, le=1000.0)
    farming_method: Literal["Conventional", "Organic / Natural", "Integrated (INM/IPM)", "Mixed / Multi-crop"]
    previous_crop: str | None = Field(default=None, max_length=80)

    temperature: float | None = Field(default=None, ge=-5.0, le=60.0)
    humidity: float | None = Field(default=None, ge=0.0, le=100.0)
    rainfall: float | None = Field(default=None, ge=0.0, le=5000.0)
    climate_source: Literal["measured", "estimate", "reference"] = "estimate"
    language: Literal["en", "kn"] = "en"

    @field_validator("village", "previous_crop", "agro_climatic_zone", mode="before")
    @classmethod
    def _strip_empty_strings(cls, v: Any) -> Any:
        if isinstance(v, str):
            cleaned = v.strip()
            return cleaned if cleaned else None
        return v


class DimensionScoresSchema(BaseModel):
    location: float
    soil: float
    water: float
    seasonal: float
    climatic: float
    nutrient: float


class RecommendedCropResultSchema(BaseModel):
    rank: int
    crop_id: int
    crop_key: str
    name_en: str
    name_kn: str
    scientific_name: str
    category: str
    image_asset: str
    suitability_category: str
    illustrative_score: float
    ml_probability: float | None
    dimension_scores: DimensionScoresSchema
    reasons_en: list[str]
    reasons_kn: list[str]
    limitations_en: list[str]
    limitations_kn: list[str]
    conflict_flags: list[str]
    water_requirement_level: str
    water_requirement_mm_min: int
    water_requirement_mm_max: int
    suitable_seasons: list[str]
    growing_duration_days_min: int
    growing_duration_days_max: int
    cultivation_guidance_en: str
    cultivation_guidance_kn: str
    information_source: str
    record_status: str


class RecommendationResponse(BaseModel):
    recommendation_id: int
    created_at: datetime
    mode_used: str
    confidence_level: str
    scoring_notice_en: str
    scoring_notice_kn: str
    disclaimer_en: str
    disclaimer_kn: str
    warnings: list[str]
    insufficient_data_reason: str | None
    missing_fields: list[str]
    location_context: dict[str, Any]
    input_summary: dict[str, Any]
    recommendations: list[RecommendedCropResultSchema]


class CompareCropsRequest(BaseModel):
    crop_ids: list[int] = Field(..., min_length=1, max_length=3)
    land_area_acres: float = Field(default=1.0, gt=0.0, le=1000.0)


class ComparedCropItem(BaseModel):
    crop_id: int
    crop_key: str
    name_en: str
    name_kn: str
    category: str
    image_asset: str
    suitable_soil_types: list[str]
    ph_range: str
    water_requirement_level: str
    water_requirement_mm_range: str
    suitable_seasons: list[str]
    growing_duration_days_range: str
    temperature_range_c: str
    humidity_range_pct: str
    rainfall_range_mm: str
    seed_rate_kg_per_acre: str
    economic_data_status: str
    economic_available: bool
    seed_cost_inr_total: float | None
    cultivation_cost_min_total: float | None
    cultivation_cost_max_total: float | None
    expected_yield_qtl_min_total: float | None
    expected_yield_qtl_max_total: float | None
    indicative_price_inr_per_qtl: float | None
    gross_revenue_min_total: float | None
    gross_revenue_max_total: float | None
    net_return_min_total: float | None
    net_return_max_total: float | None
    assumptions_en: str | None
    assumptions_kn: str | None
    economic_source: str | None
    information_source: str


class CompareCropsResponse(BaseModel):
    land_area_acres: float
    disclaimer_en: str
    disclaimer_kn: str
    crops: list[ComparedCropItem]


class SoilAnalysisRequest(BaseModel):
    soil_type: Literal["Red", "Black", "Alluvial", "Laterite", "Sandy", "Loamy", "Clay"]
    ph: float | None = Field(default=None, ge=0.0, le=14.0)
    nitrogen: float | None = Field(default=None, ge=0.0, le=500.0)
    phosphorus: float | None = Field(default=None, ge=0.0, le=500.0)
    potassium: float | None = Field(default=None, ge=0.0, le=600.0)
    measurement_source: Literal["soil_test", "estimate", "unavailable"] = "soil_test"
    soil_test_date: date | None = None


class NutrientInterpretation(BaseModel):
    parameter: str
    value: float | None
    unit: str
    status: str
    interpretation_en: str
    interpretation_kn: str
    reference_range: str


class SoilAnalysisResponse(BaseModel):
    soil_type: str
    measurement_source: str
    overview_en: str
    overview_kn: str
    interpretations: list[NutrientInterpretation]
    guidance_en: list[str]
    guidance_kn: list[str]
    fertilizer_caution_en: str
    fertilizer_caution_kn: str


class KnowledgeArticleSummary(BaseModel):
    id: int
    slug: str
    category: str
    title_en: str
    title_kn: str
    summary_en: str
    summary_kn: str
    source_name: str
    source_url: str | None
    updated_at: datetime


class KnowledgeArticleDetail(KnowledgeArticleSummary):
    content_en: str
    content_kn: str


class FeedbackCreateRequest(BaseModel):
    recommendation_id: int | None = None
    category: Literal["recommendation_accuracy", "usability", "translation", "data_correction", "general"] = "general"
    rating: int | None = Field(default=None, ge=1, le=5)
    district: str | None = Field(default=None, max_length=80)
    comment: str = Field(..., min_length=5, max_length=2000)


class FeedbackResponse(BaseModel):
    id: int
    category: str
    rating: int | None
    district: str | None
    comment: str
    review_status: str
    created_at: datetime


class AdminLoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=1, max_length=128)


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    role: str
    local_dev_notice: str


class AdminCropUpdateRequest(BaseModel):
    name_en: str | None = Field(default=None, max_length=100)
    name_kn: str | None = Field(default=None, max_length=120)
    water_requirement_level: str | None = Field(default=None, max_length=32)
    cultivation_guidance_en: str | None = None
    cultivation_guidance_kn: str | None = None
    information_source: str | None = Field(default=None, max_length=220)
    is_active: bool | None = None


class AdminRuleCreateRequest(BaseModel):
    crop_id: int
    state: str = Field(..., max_length=80)
    district: str | None = Field(default=None, max_length=80)
    agro_climatic_zone: str | None = Field(default=None, max_length=120)
    season: Literal["Kharif", "Rabi", "Zaid", "Perennial"]
    suitability_level: Literal["recommended", "conditional", "restricted"]
    priority_weight: float = Field(default=1.0, ge=0.0, le=2.0)
    rule_notes_en: str = Field(..., min_length=5)
    rule_notes_kn: str = Field(..., min_length=5)
    source: str = Field(..., min_length=3, max_length=180)


class AdminArticleCreateRequest(BaseModel):
    slug: str = Field(..., min_length=3, max_length=100)
    category: str = Field(..., min_length=2, max_length=60)
    title_en: str = Field(..., min_length=3, max_length=180)
    title_kn: str = Field(..., min_length=3, max_length=220)
    summary_en: str = Field(..., min_length=10)
    summary_kn: str = Field(..., min_length=10)
    content_en: str = Field(..., min_length=20)
    content_kn: str = Field(..., min_length=20)
    source_name: str = Field(..., min_length=3, max_length=180)
    source_url: str | None = Field(default=None, max_length=300)


class AdminFeedbackUpdateRequest(BaseModel):
    review_status: Literal["pending", "reviewed"]
    admin_notes: str | None = Field(default=None, max_length=1000)
