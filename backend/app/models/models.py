import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text, ForeignKey, JSON, DateTime
)
from sqlalchemy.orm import relationship
from backend.app.db.database import Base

class State(Base):
    __tablename__ = "states"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    kannada_name = Column(String(100))
    districts = relationship("District", back_populates="state", cascade="all, delete-orphan")

class AgroClimaticZone(Base):
    __tablename__ = "agro_climatic_zones"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(150), nullable=False)
    kannada_name = Column(String(150))
    headquarters = Column(String(100))
    districts_covered = Column(JSON)  # list of district names
    taluks_covered = Column(JSON)      # list of taluk names
    climate_description = Column(Text)
    annual_rainfall_min_mm = Column(Float)
    annual_rainfall_max_mm = Column(Float)
    normal_rainfall_mm = Column(Float)
    major_soils = Column(JSON)        # list of soil types
    primary_crops = Column(JSON)      # list of main crops
    critical_risks = Column(JSON)     # list of risks
    verification_status = Column(String(50), default="verified")
    source_reference = Column(Text)
    districts = relationship("District", back_populates="zone")

class District(Base):
    __tablename__ = "districts"
    id = Column(Integer, primary_key=True, index=True)
    state_id = Column(Integer, ForeignKey("states.id"), default=1)
    zone_id = Column(Integer, ForeignKey("agro_climatic_zones.id"), nullable=False)
    secondary_zone_id = Column(Integer, nullable=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    kannada_name = Column(String(100))
    headquarters = Column(String(100))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    normal_rainfall_mm = Column(Float)
    dominant_soils = Column(JSON)
    drainage_profile = Column(String(255))
    drought_vulnerability = Column(String(50))
    
    state = relationship("State", back_populates="districts")
    zone = relationship("AgroClimaticZone", back_populates="districts")
    taluks = relationship("Taluk", back_populates="district", cascade="all, delete-orphan")

class Taluk(Base):
    __tablename__ = "taluks"
    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)
    name = Column(String(100), index=True, nullable=False)
    kannada_name = Column(String(100))
    zone_id = Column(Integer, ForeignKey("agro_climatic_zones.id"), nullable=True)
    district = relationship("District", back_populates="taluks")
    villages = relationship("Village", back_populates="taluk", cascade="all, delete-orphan")

class Village(Base):
    __tablename__ = "villages"
    id = Column(Integer, primary_key=True, index=True)
    taluk_id = Column(Integer, ForeignKey("taluks.id"), nullable=False)
    name = Column(String(100), nullable=False)
    pincode = Column(String(10), nullable=True)
    taluk = relationship("Taluk", back_populates="villages")

class SoilObservation(Base):
    __tablename__ = "soil_observations"
    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), nullable=True)
    soil_colour = Column(String(50))        # Red, Dark black, Brown, etc.
    soil_texture = Column(String(50))       # Sandy, Clayey, Loamy, Silty, Mixed, Unknown
    drainage = Column(String(100))          # Water drains quickly, moderately, remains for several hours, days
    moisture_retention = Column(String(100))# Dries quickly, short period, several days
    soil_depth = Column(String(50))         # Shallow, Medium, Deep, Unknown
    presence_of_stones = Column(Boolean, default=False)
    rocky_ground = Column(Boolean, default=False)
    surface_erosion = Column(Boolean, default=False)
    waterlogging_observed = Column(Boolean, default=False)
    land_condition_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class LandProfile(Base):
    __tablename__ = "land_profiles"
    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), nullable=True)
    slope_type = Column(String(50))         # Flat land, Slightly sloping, Steep/hilly, Low-lying, Rocky
    approximate_area_acres = Column(Float, default=1.0)
    water_accumulation_risk = Column(String(50), default="Low")
    erosion_risk = Column(String(50), default="Low")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class WaterAvailability(Base):
    __tablename__ = "water_availabilities"
    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), nullable=True)
    irrigation_source = Column(String(100)) # Rainfed farming, Borewell, Canal, etc.
    availability_duration = Column(String(100)) # Throughout season, certain months, limited, uncertain
    has_drip_facility = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class FarmingHistory(Base):
    __tablename__ = "farming_histories"
    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), nullable=True)
    previous_crop = Column(String(100), nullable=True)
    previous_season = Column(String(50), nullable=True)
    was_successful = Column(Boolean, default=True)
    approximate_yield = Column(String(100), nullable=True)
    drought_affected = Column(Boolean, default=False)
    flood_affected = Column(Boolean, default=False)
    recurring_pest_problem = Column(String(200), nullable=True)
    water_shortage_encountered = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Crop(Base):
    __tablename__ = "crops"
    id = Column(String(50), primary_key=True, index=True)  # e.g. "ragi", "jowar"
    name = Column(String(100), nullable=False)
    kannada_name = Column(String(100))
    scientific_name = Column(String(100))
    category = Column(String(50))
    suitable_zones = Column(JSON)     # list of zone IDs [4, 5, 6, 7]
    suitable_districts = Column(JSON) # list of district names
    
    # Relationships
    requirements = relationship("CropRequirement", back_populates="crop", uselist=False, cascade="all, delete-orphan")
    economic_data = relationship("CropEconomicData", back_populates="crop", uselist=False, cascade="all, delete-orphan")
    regional_suitability = relationship("RegionalCropSuitability", back_populates="crop", cascade="all, delete-orphan")

class CropRequirement(Base):
    __tablename__ = "crop_requirements"
    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(String(50), ForeignKey("crops.id"), unique=True, nullable=False)
    
    # Soil texture & colour
    preferred_textures = Column(JSON)
    acceptable_textures = Column(JSON)
    unsuitable_textures = Column(JSON)
    preferred_colors = Column(JSON)
    acceptable_colors = Column(JSON)
    unsuitable_colors = Column(JSON)
    
    # Drainage & moisture
    drainage_preferred = Column(JSON)
    drainage_unsuitable = Column(JSON)
    moisture_preferred = Column(JSON)
    min_soil_depth = Column(String(50))
    
    # Water & climate
    water_req_min_mm = Column(Float)
    water_req_opt_min_mm = Column(Float)
    water_req_opt_max_mm = Column(Float)
    water_req_max_mm = Column(Float)
    suitable_water_sources = Column(JSON)
    water_scarcity_tolerance = Column(String(50))
    
    temp_min_c = Column(Float)
    temp_opt_min_c = Column(Float)
    temp_opt_max_c = Column(Float)
    temp_max_c = Column(Float)
    
    rain_min_mm = Column(Float)
    rain_opt_min_mm = Column(Float)
    rain_opt_max_mm = Column(Float)
    rain_max_mm = Column(Float)
    
    # Season & duration
    suitable_seasons = Column(JSON)
    sowing_windows = Column(JSON)
    duration_min_days = Column(Integer)
    duration_max_days = Column(Integer)
    duration_category = Column(String(50))
    
    # Land & rotation
    preferred_slopes = Column(JSON)
    unsuitable_slopes = Column(JSON)
    favored_predecessors = Column(JSON)
    discouraged_predecessors = Column(JSON)
    critical_risks = Column(JSON)
    cultivation_practices = Column(Text)
    verification_status = Column(String(50), default="verified")
    source_reference = Column(Text)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    
    crop = relationship("Crop", back_populates="requirements")

class RegionalCropSuitability(Base):
    __tablename__ = "regional_crop_suitabilities"
    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(String(50), ForeignKey("crops.id"), nullable=False)
    zone_id = Column(Integer, ForeignKey("agro_climatic_zones.id"), nullable=False)
    suitability_tier = Column(String(50)) # Highly Recommended, Moderately Suitable, Contingent, Not Recommended
    historical_yield_notes = Column(Text, nullable=True)
    special_regional_advisory = Column(Text, nullable=True)
    crop = relationship("Crop", back_populates="regional_suitability")

class CropEconomicData(Base):
    __tablename__ = "crop_economic_data"
    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(String(50), ForeignKey("crops.id"), unique=True, nullable=False)
    seed_cost_per_acre_inr = Column(Float)
    input_cost_per_acre_inr = Column(Float)
    labor_cost_per_acre_inr = Column(Float)
    total_cost_per_acre_inr = Column(Float)
    avg_yield_quintals_per_acre_min = Column(Float)
    avg_yield_quintals_per_acre_max = Column(Float)
    benchmark_msp_inr_per_quintal = Column(Float)
    data_year = Column(String(20), default="2024-25")
    source_reference = Column(Text)
    crop = relationship("Crop", back_populates="economic_data")

class WeatherObservation(Base):
    __tablename__ = "weather_observations"
    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)
    observation_time = Column(DateTime, default=datetime.datetime.utcnow)
    temperature_c = Column(Float)
    relative_humidity_pct = Column(Float)
    precipitation_recent_mm = Column(Float)
    wind_speed_kmh = Column(Float)
    weather_condition = Column(String(100))
    source = Column(String(100))  # "Open-Meteo API", "IMD Normal", etc.

class WeatherForecast(Base):
    __tablename__ = "weather_forecasts"
    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)
    forecast_date = Column(DateTime, nullable=False)
    temp_min_c = Column(Float)
    temp_max_c = Column(Float)
    precipitation_expected_mm = Column(Float)
    precipitation_probability_pct = Column(Float)
    forecast_source = Column(String(100))
    retrieval_timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class AgriculturalAdvisory(Base):
    __tablename__ = "agricultural_advisories"
    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    zone_id = Column(Integer, ForeignKey("agro_climatic_zones.id"), nullable=True)
    crop_id = Column(String(50), ForeignKey("crops.id"), nullable=True)
    title = Column(String(255), nullable=False)
    kannada_title = Column(String(255))
    advisory_type = Column(String(50)) # Sowing Window, Heavy Rainfall Warning, Dry Spell Alert, General
    severity = Column(String(20), default="Info") # Info, Warning, Alert, Severe
    message = Column(Text, nullable=False)
    kannada_message = Column(Text)
    valid_from = Column(DateTime)
    valid_until = Column(DateTime)
    source = Column(String(100))
    published_date = Column(DateTime, default=datetime.datetime.utcnow)

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, index=True)
    state = Column(String(50), default="Karnataka")
    district = Column(String(100), nullable=False)
    taluk = Column(String(100), nullable=False)
    village = Column(String(100), nullable=True)
    zone_id = Column(Integer, ForeignKey("agro_climatic_zones.id"))
    planned_season = Column(String(50))
    planned_sowing_month = Column(String(50), nullable=True)
    farming_objective = Column(String(100), nullable=True)
    reliability_score_pct = Column(Float, default=100.0)
    data_completeness_pct = Column(Float, default=100.0)
    missing_fields = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    results = relationship("RecommendationResult", back_populates="recommendation", cascade="all, delete-orphan")

class RecommendationResult(Base):
    __tablename__ = "recommendation_results"
    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), nullable=False)
    crop_id = Column(String(50), ForeignKey("crops.id"), nullable=False)
    rank = Column(Integer, nullable=False)
    suitability_score = Column(Float, nullable=False)  # 0 to 100
    suitability_tier = Column(String(50))              # Highly Suitable, Moderately Suitable, Marginally Suitable
    
    # Sub-scores
    regional_score = Column(Float)
    soil_score = Column(Float)
    drainage_score = Column(Float)
    water_score = Column(Float)
    climate_score = Column(Float)
    season_score = Column(Float)
    
    # Detailed explanations & conditions
    reasons_for_selection = Column(JSON)
    supporting_soil_observations = Column(JSON)
    water_sufficiency_notes = Column(Text)
    climate_suitability_notes = Column(Text)
    potential_risks = Column(JSON)
    crucial_practices = Column(Text)
    data_uncertainty_notes = Column(Text)
    
    recommendation = relationship("Recommendation", back_populates="results")

class KnowledgeArticle(Base):
    __tablename__ = "knowledge_articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    kannada_title = Column(String(255))
    category = Column(String(100), index=True)
    summary = Column(Text)
    content = Column(Text, nullable=False)
    source = Column(String(255))
    verification_status = Column(String(50), default="verified")
    publication_date = Column(String(50))
    geographic_applicability = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DataSource(Base):
    __tablename__ = "data_sources"
    id = Column(String(50), primary_key=True)
    source_name = Column(String(255), nullable=False)
    source_url = Column(String(255))
    data_category = Column(String(255))
    geographic_coverage = Column(String(255))
    collection_date = Column(String(50))
    verification_date = Column(String(50))
    license_or_usage = Column(String(255))
    data_status = Column(String(50), default="verified")
    update_frequency = Column(String(100))

class FarmerFeedback(Base):
    __tablename__ = "farmer_feedback"
    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(Integer, nullable=True)
    district = Column(String(100), nullable=True)
    crop_selected = Column(String(100), nullable=True)
    rating = Column(Integer)  # 1 to 5
    was_helpful = Column(Boolean, default=True)
    feedback_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
