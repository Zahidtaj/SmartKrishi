"""Relational database models for SmartKrishi (SQLite & PostgreSQL compatible)."""

from datetime import date, datetime, timezone
from typing import Any
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Farmer(Base):
    __tablename__ = "farmers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_label: Mapped[str] = mapped_column(String(80), nullable=False, default="anonymous-session")
    preferred_language: Mapped[str] = mapped_column(String(8), nullable=False, default="en")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    soil_records: Mapped[list["SoilRecord"]] = relationship(back_populates="farmer")
    farm_profiles: Mapped[list["FarmProfile"]] = relationship(back_populates="farmer")
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="farmer")


class Location(Base):
    __tablename__ = "locations"
    __table_args__ = (
        UniqueConstraint("state", "district", "taluk", name="uq_location_state_district_taluk"),
        Index("ix_locations_state_district", "state", "district"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    state: Mapped[str] = mapped_column(String(80), nullable=False)
    district: Mapped[str] = mapped_column(String(80), nullable=False)
    taluk: Mapped[str] = mapped_column(String(80), nullable=False)
    agro_climatic_zone: Mapped[str] = mapped_column(String(120), nullable=False)
    zone_code: Mapped[str] = mapped_column(String(24), nullable=False)
    normal_annual_rainfall_mm: Mapped[float | None] = mapped_column(Float, nullable=True)
    typical_rainfall_pattern: Mapped[str] = mapped_column(String(240), nullable=False)
    dominant_soil_types: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    common_soil_textures: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    major_crops: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    recommended_seasons_summary: Mapped[dict[str, str]] = mapped_column(JSON, nullable=False, default=dict)
    growing_period_info: Mapped[str] = mapped_column(String(200), nullable=False)
    regional_references: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    data_source: Mapped[str] = mapped_column(String(220), nullable=False)
    verification_status: Mapped[str] = mapped_column(String(48), nullable=False, default="verified_reference")
    last_updated: Mapped[date] = mapped_column(Date, nullable=False, default=date(2026, 5, 1))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class SoilRecord(Base):
    __tablename__ = "soil_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    farmer_id: Mapped[int | None] = mapped_column(ForeignKey("farmers.id", ondelete="SET NULL"), nullable=True)
    location_id: Mapped[int | None] = mapped_column(ForeignKey("locations.id", ondelete="SET NULL"), nullable=True)

    # Primary observation-based farmer inputs
    soil_color: Mapped[str] = mapped_column(String(40), nullable=False, default="mixed_uncertain")
    soil_texture: Mapped[str] = mapped_column(String(40), nullable=False, default="not_sure")
    drainage_after_rain: Mapped[str] = mapped_column(String(40), nullable=False, default="not_sure")
    moisture_retention: Mapped[str] = mapped_column(String(40), nullable=False, default="not_sure")
    soil_depth: Mapped[str] = mapped_column(String(24), nullable=False, default="unknown")
    visible_stones: Mapped[str] = mapped_column(String(24), nullable=False, default="not_sure")
    waterlogging_issue: Mapped[str] = mapped_column(String(24), nullable=False, default="not_sure")
    erosion_issue: Mapped[str] = mapped_column(String(24), nullable=False, default="not_sure")
    observation_confidence: Mapped[str] = mapped_column(String(24), nullable=False, default="moderate")

    # Optional secondary / future laboratory fields (never mandatory)
    soil_type: Mapped[str | None] = mapped_column(String(40), nullable=True)
    ph: Mapped[float | None] = mapped_column(Float, nullable=True)
    nitrogen: Mapped[float | None] = mapped_column(Float, nullable=True)
    phosphorus: Mapped[float | None] = mapped_column(Float, nullable=True)
    potassium: Mapped[float | None] = mapped_column(Float, nullable=True)
    measurement_source: Mapped[str] = mapped_column(String(32), nullable=False, default="farmer_observation")
    soil_test_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    farmer: Mapped["Farmer | None"] = relationship(back_populates="soil_records")


class FarmProfile(Base):
    __tablename__ = "farm_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    farmer_id: Mapped[int | None] = mapped_column(ForeignKey("farmers.id", ondelete="SET NULL"), nullable=True)
    location_id: Mapped[int | None] = mapped_column(ForeignKey("locations.id", ondelete="SET NULL"), nullable=True)
    village: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Land & Water observations
    land_topography: Mapped[str] = mapped_column(String(40), nullable=False, default="flat")
    water_source: Mapped[str] = mapped_column(String(40), nullable=False, default="rainfed")
    water_reliability: Mapped[str] = mapped_column(String(40), nullable=False, default="uncertain")

    # Optional Farming History
    previous_crop: Mapped[str | None] = mapped_column(String(80), nullable=True)
    previous_crop_success: Mapped[str | None] = mapped_column(String(32), nullable=True)
    drought_history: Mapped[str | None] = mapped_column(String(24), nullable=True)
    flood_history: Mapped[str | None] = mapped_column(String(24), nullable=True)
    pest_disease_history: Mapped[str | None] = mapped_column(String(240), nullable=True)
    land_area_acres: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Season & Planning
    season: Mapped[str] = mapped_column(String(24), nullable=False)
    intended_sowing_month: Mapped[str | None] = mapped_column(String(24), nullable=True)
    duration_preference: Mapped[str] = mapped_column(String(24), nullable=False, default="flexible")
    farming_priority: Mapped[str] = mapped_column(String(40), nullable=False, default="land_suitability")

    # Weather / Climate snapshot metadata
    temperature_c: Mapped[float | None] = mapped_column(Float, nullable=True)
    humidity_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    rainfall_mm: Mapped[float | None] = mapped_column(Float, nullable=True)
    climate_source: Mapped[str] = mapped_column(String(40), nullable=False, default="zone_long_term_normal")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    farmer: Mapped["Farmer | None"] = relationship(back_populates="farm_profiles")


class Crop(Base):
    __tablename__ = "crops"
    __table_args__ = (
        Index("ix_crops_crop_key", "crop_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    crop_key: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    name_kn: Mapped[str] = mapped_column(String(120), nullable=False)
    scientific_name: Mapped[str] = mapped_column(String(120), nullable=False)
    category: Mapped[str] = mapped_column(String(40), nullable=False)
    image_asset: Mapped[str] = mapped_column(String(180), nullable=False)
    growing_duration_days_min: Mapped[int] = mapped_column(Integer, nullable=False)
    growing_duration_days_max: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_category: Mapped[str] = mapped_column(String(24), nullable=False, default="medium")
    water_requirement_level: Mapped[str] = mapped_column(String(32), nullable=False)
    water_requirement_mm_min: Mapped[int] = mapped_column(Integer, nullable=False)
    water_requirement_mm_max: Mapped[int] = mapped_column(Integer, nullable=False)
    seed_rate_kg_per_acre: Mapped[str] = mapped_column(String(60), nullable=False)
    household_food_crop: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    commercial_crop: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    cultivation_guidance_en: Mapped[str] = mapped_column(Text, nullable=False)
    cultivation_guidance_kn: Mapped[str] = mapped_column(Text, nullable=False)
    information_source: Mapped[str] = mapped_column(String(220), nullable=False)
    record_status: Mapped[str] = mapped_column(String(32), nullable=False, default="verified_reference")
    verification_status: Mapped[str] = mapped_column(String(48), nullable=False, default="verified_institutional_reference")
    last_updated: Mapped[date] = mapped_column(Date, nullable=False, default=date(2026, 5, 1))
    in_ml_dataset: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    requirement: Mapped["CropRequirement | None"] = relationship(
        back_populates="crop", cascade="all, delete-orphan", uselist=False
    )
    regional_rules: Mapped[list["RegionalCropRule"]] = relationship(
        back_populates="crop", cascade="all, delete-orphan"
    )
    economic_data: Mapped[list["CropEconomicData"]] = relationship(
        back_populates="crop", cascade="all, delete-orphan"
    )


class CropRequirement(Base):
    __tablename__ = "crop_requirements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    crop_id: Mapped[int] = mapped_column(ForeignKey("crops.id", ondelete="CASCADE"), unique=True, nullable=False)
    suitable_soil_types: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    suitable_textures: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    suitable_drainage: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    moisture_needs: Mapped[str] = mapped_column(String(24), nullable=False, default="moderate")
    suitable_land_topography: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    min_soil_depth: Mapped[str] = mapped_column(String(24), nullable=False, default="medium")
    drought_tolerance: Mapped[str] = mapped_column(String(24), nullable=False, default="moderate")
    waterlogging_tolerance: Mapped[str] = mapped_column(String(24), nullable=False, default="low")
    sowing_months: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    weather_risk_thresholds: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

    # Optional lab reference bands (for optional secondary Soil Health Card interpretation only)
    ph_min: Mapped[float] = mapped_column(Float, nullable=False)
    ph_max: Mapped[float] = mapped_column(Float, nullable=False)
    ph_optimal_min: Mapped[float] = mapped_column(Float, nullable=False)
    ph_optimal_max: Mapped[float] = mapped_column(Float, nullable=False)
    nitrogen_min: Mapped[float] = mapped_column(Float, nullable=False)
    nitrogen_max: Mapped[float] = mapped_column(Float, nullable=False)
    phosphorus_min: Mapped[float] = mapped_column(Float, nullable=False)
    phosphorus_max: Mapped[float] = mapped_column(Float, nullable=False)
    potassium_min: Mapped[float] = mapped_column(Float, nullable=False)
    potassium_max: Mapped[float] = mapped_column(Float, nullable=False)

    temp_min_c: Mapped[float] = mapped_column(Float, nullable=False)
    temp_max_c: Mapped[float] = mapped_column(Float, nullable=False)
    humidity_min_pct: Mapped[float] = mapped_column(Float, nullable=False)
    humidity_max_pct: Mapped[float] = mapped_column(Float, nullable=False)
    rainfall_min_mm: Mapped[float] = mapped_column(Float, nullable=False)
    rainfall_max_mm: Mapped[float] = mapped_column(Float, nullable=False)
    suitable_seasons: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    supported_water_levels: Mapped[list[str]] = mapped_column(JSON, nullable=False)

    crop: Mapped["Crop"] = relationship(back_populates="requirement")


class RegionalCropRule(Base):
    __tablename__ = "regional_crop_rules"
    __table_args__ = (
        Index("ix_regional_rules_lookup", "state", "district", "season"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    crop_id: Mapped[int] = mapped_column(ForeignKey("crops.id", ondelete="CASCADE"), nullable=False)
    state: Mapped[str] = mapped_column(String(80), nullable=False)
    district: Mapped[str | None] = mapped_column(String(80), nullable=True)
    agro_climatic_zone: Mapped[str | None] = mapped_column(String(120), nullable=True)
    season: Mapped[str] = mapped_column(String(24), nullable=False)
    suitability_level: Mapped[str] = mapped_column(String(24), nullable=False, default="recommended")
    priority_weight: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    rule_notes_en: Mapped[str] = mapped_column(Text, nullable=False)
    rule_notes_kn: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(180), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    crop: Mapped["Crop"] = relationship(back_populates="regional_rules")


class Recommendation(Base):
    __tablename__ = "recommendations"
    __table_args__ = (
        Index("ix_recommendations_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    farmer_id: Mapped[int | None] = mapped_column(ForeignKey("farmers.id", ondelete="SET NULL"), nullable=True)
    location_id: Mapped[int | None] = mapped_column(ForeignKey("locations.id", ondelete="SET NULL"), nullable=True)
    soil_record_id: Mapped[int | None] = mapped_column(ForeignKey("soil_records.id", ondelete="SET NULL"), nullable=True)
    farm_profile_id: Mapped[int | None] = mapped_column(ForeignKey("farm_profiles.id", ondelete="SET NULL"), nullable=True)
    mode_used: Mapped[str] = mapped_column(String(40), nullable=False, default="observation_rule_based")
    confidence_level: Mapped[str] = mapped_column(String(24), nullable=False)
    soil_interpretation: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    weather_advisory: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    input_provenance: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    input_snapshot: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    warnings: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    missing_information: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    insufficient_data_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    model_version: Mapped[str] = mapped_column(String(64), nullable=False, default="observation-rules-v2.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    farmer: Mapped["Farmer | None"] = relationship(back_populates="recommendations")
    results: Mapped[list["RecommendationResult"]] = relationship(
        back_populates="recommendation", cascade="all, delete-orphan", order_by="RecommendationResult.rank"
    )


class RecommendationResult(Base):
    __tablename__ = "recommendation_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recommendation_id: Mapped[int] = mapped_column(ForeignKey("recommendations.id", ondelete="CASCADE"), nullable=False)
    crop_id: Mapped[int] = mapped_column(ForeignKey("crops.id", ondelete="CASCADE"), nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    suitability_category: Mapped[str] = mapped_column(String(40), nullable=False)
    illustrative_score: Mapped[float] = mapped_column(Float, nullable=False)
    ml_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    dimension_scores: Mapped[dict[str, float]] = mapped_column(JSON, nullable=False)
    reasons_en: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    reasons_kn: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    limitations_en: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    limitations_kn: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    missing_info_en: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    missing_info_kn: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    compatibility_badges: Mapped[dict[str, str]] = mapped_column(JSON, nullable=False, default=dict)
    conflict_flags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    recommendation: Mapped["Recommendation"] = relationship(back_populates="results")
    crop: Mapped["Crop"] = relationship()


class CropEconomicData(Base):
    __tablename__ = "crop_economic_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    crop_id: Mapped[int] = mapped_column(ForeignKey("crops.id", ondelete="CASCADE"), nullable=False)
    region_scope: Mapped[str] = mapped_column(String(80), nullable=False, default="Karnataka (Illustrative Baseline)")
    season: Mapped[str] = mapped_column(String(24), nullable=False)
    seed_cost_inr_per_acre: Mapped[float | None] = mapped_column(Float, nullable=True)
    cultivation_cost_min_inr_per_acre: Mapped[float | None] = mapped_column(Float, nullable=True)
    cultivation_cost_max_inr_per_acre: Mapped[float | None] = mapped_column(Float, nullable=True)
    expected_yield_qtl_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    expected_yield_qtl_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    indicative_price_inr_per_qtl: Mapped[float | None] = mapped_column(Float, nullable=True)
    assumptions_en: Mapped[str] = mapped_column(Text, nullable=False)
    assumptions_kn: Mapped[str] = mapped_column(Text, nullable=False)
    data_status: Mapped[str] = mapped_column(String(32), nullable=False, default="prototype_demonstration")
    source: Mapped[str] = mapped_column(String(220), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    crop: Mapped["Crop"] = relationship(back_populates="economic_data")


class KnowledgeArticle(Base):
    __tablename__ = "knowledge_articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    title_en: Mapped[str] = mapped_column(String(180), nullable=False)
    title_kn: Mapped[str] = mapped_column(String(220), nullable=False)
    summary_en: Mapped[str] = mapped_column(Text, nullable=False)
    summary_kn: Mapped[str] = mapped_column(Text, nullable=False)
    content_en: Mapped[str] = mapped_column(Text, nullable=False)
    content_kn: Mapped[str] = mapped_column(Text, nullable=False)
    source_name: Mapped[str] = mapped_column(String(180), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(300), nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)


class Feedback(Base):
    __tablename__ = "feedback"
    __table_args__ = (
        CheckConstraint("rating IS NULL OR (rating >= 1 AND rating <= 5)", name="ck_feedback_rating_range"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recommendation_id: Mapped[int | None] = mapped_column(ForeignKey("recommendations.id", ondelete="SET NULL"), nullable=True)
    category: Mapped[str] = mapped_column(String(40), nullable=False, default="general")
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    district: Mapped[str | None] = mapped_column(String(80), nullable=True)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    review_status: Mapped[str] = mapped_column(String(24), nullable=False, default="pending")
    admin_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class AdminUser(Base):
    __tablename__ = "admin_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[str] = mapped_column(String(24), nullable=False, default="admin")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
