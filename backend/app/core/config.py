import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR.parent / "data"

class Settings(BaseSettings):
    PROJECT_NAME: str = "SmartKrishi"
    PROJECT_TITLE: str = "Observation-Based Smart Crop Recommendation & Agricultural Decision Support System"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/smartkrishi.db")
    
    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    
    # Path settings
    DATA_PATH: Path = DATA_DIR
    
    # Agricultural Suitability Scoring Weights (Sum = 1.00)
    # Stored separately from execution logic for transparent configurability
    SCORING_WEIGHTS: dict[str, float] = {
        "regional_suitability": 0.15,
        "soil_texture_compatibility": 0.20,
        "drainage_compatibility": 0.15,
        "water_availability_compatibility": 0.20,
        "rainfall_compatibility": 0.10,
        "temperature_compatibility": 0.10,
        "seasonal_compatibility": 0.10
    }
    
    # Uncertainty Deductions (Subtracted from overall score reliability percentage)
    UNCERTAINTY_PENALTIES: dict[str, int] = {
        "unknown_soil_texture": 15,
        "unknown_soil_colour": 5,
        "unknown_drainage": 10,
        "unknown_moisture_retention": 8,
        "unknown_soil_depth": 7,
        "missing_weather_live": 5
    }

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
