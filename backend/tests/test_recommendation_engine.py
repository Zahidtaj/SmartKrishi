import pytest
import asyncio
from backend.app.services.location_service import location_service
from backend.app.services.weather_service import weather_service
from backend.app.services.rule_engine import rule_engine
from backend.app.services.scoring_service import scoring_service
from backend.app.services.explanation_service import explanation_service
from backend.app.services.comparison_service import comparison_service

@pytest.fixture
def mock_weather():
    return {
        "location": "Chitradurga",
        "latitude": 14.2251,
        "longitude": 76.3980,
        "current_temperature_c": 28.5,
        "relative_humidity_pct": 60.0,
        "wind_speed_kmh": 12.0,
        "recent_precipitation_mm": 0.0,
        "condition": "Partly Cloudy",
        "source": "Open-Meteo High-Resolution Forecast Model",
        "retrieval_timestamp": "2026-11-16 12:00:00 UTC",
        "is_live_data": True,
        "forecast_7_day": [],
        "consecutive_dry_days_forecast": 4,
        "heavy_rainfall_alert": False,
        "historical_normal_rainfall_mm": 574.0
    }

# Scenario 1: Red soil, sandy texture, limited irrigation
def test_scenario_1_red_sandy_limited_irrigation(mock_weather):
    loc = location_service.resolve_location("Tumakuru")
    soil = {"soil_colour": "Red", "soil_texture": "Sandy", "drainage": "Water drains quickly", "soil_depth": "Medium"}
    water = {"irrigation_source": "Borewell", "availability_duration": "Limited water availability"}
    land = {"slope_type": "Flat land"}
    
    rec, filtered, quality = scoring_service.evaluate_candidates(
        location=loc, soil_obs=soil, water_avail=water, land_profile=land,
        season="Kharif", weather=mock_weather
    )
    assert len(rec) > 0
    top_crop_ids = [c["crop"]["id"] for c in rec[:4]]
    # Groundnut, Ragi, Sesamum, Horse Gram love red sandy/loamy soil
    assert any(c in top_crop_ids for c in ["groundnut", "ragi", "sesamum", "horse_gram"])

# Scenario 2: Dark soil, clayey texture, waterlogging
def test_scenario_2_dark_clay_waterlogged(mock_weather):
    loc = location_service.resolve_location("Raichur")
    soil = {
        "soil_colour": "Dark black",
        "soil_texture": "Clayey",
        "drainage": "Water remains for one or more days",
        "waterlogging_observed": True,
        "soil_depth": "Deep"
    }
    water = {"irrigation_source": "Canal irrigation", "availability_duration": "Throughout season"}
    land = {"slope_type": "Low-lying land"}
    
    rec, filtered, quality = scoring_service.evaluate_candidates(
        location=loc, soil_obs=soil, water_avail=water, land_profile=land,
        season="Kharif", weather=mock_weather
    )
    # Groundnut, red gram, and chickpea must be filtered out due to lethal waterlogging
    filtered_ids = [f["crop_id"] for f in filtered]
    assert "groundnut" in filtered_ids
    assert "red_gram" in filtered_ids

# Scenario 3: Loamy soil, moderate water availability
def test_scenario_3_loamy_moderate_water(mock_weather):
    loc = location_service.resolve_location("Mandya")
    soil = {"soil_colour": "Reddish brown", "soil_texture": "Loamy", "drainage": "Water drains moderately", "soil_depth": "Medium"}
    water = {"irrigation_source": "Canal irrigation", "availability_duration": "Throughout season"}
    land = {"slope_type": "Flat land"}
    
    rec, filtered, quality = scoring_service.evaluate_candidates(
        location=loc, soil_obs=soil, water_avail=water, land_profile=land,
        season="Kharif", weather=mock_weather
    )
    assert len(rec) > 0
    # Balanced loamy soil supports Ragi, Paddy, Maize, Sugarcane
    top_ids = [c["crop"]["id"] for c in rec[:5]]
    assert "ragi" in top_ids or "paddy" in top_ids or "maize" in top_ids

# Scenario 4: Shallow soil with rocky land
def test_scenario_4_shallow_soil_rocky_land(mock_weather):
    loc = location_service.resolve_location("Chitradurga")
    soil = {"soil_colour": "Mixed", "soil_texture": "Mixed", "drainage": "Water drains quickly", "soil_depth": "Shallow"}
    water = {"irrigation_source": "Rainfed farming", "availability_duration": "Limited water availability"}
    land = {"slope_type": "Rocky land"}
    
    rec, filtered, quality = scoring_service.evaluate_candidates(
        location=loc, soil_obs=soil, water_avail=water, land_profile=land,
        season="Kharif", weather=mock_weather
    )
    filtered_ids = [f["crop_id"] for f in filtered]
    # Deep rooting Sugarcane or Cotton must be filtered or excluded
    assert "sugarcane" in filtered_ids or "cotton" in filtered_ids
    # Hardy shallow soil crops like Horse Gram / Ragi must be candidate
    rec_ids = [c["crop"]["id"] for c in rec]
    assert "horse_gram" in rec_ids or "ragi" in rec_ids

# Scenario 5: Flat land with seasonal rainfall
def test_scenario_5_flat_land_seasonal_rainfall(mock_weather):
    loc = location_service.resolve_location("Dharwad")
    soil = {"soil_colour": "Dark black", "soil_texture": "Loamy", "drainage": "Water drains moderately", "soil_depth": "Medium"}
    water = {"irrigation_source": "Rainfed farming", "availability_duration": "Throughout season"}
    land = {"slope_type": "Flat land"}
    
    rec, filtered, quality = scoring_service.evaluate_candidates(
        location=loc, soil_obs=soil, water_avail=water, land_profile=land,
        season="Kharif", weather=mock_weather
    )
    assert len(rec) > 0
    top_ids = [c["crop"]["id"] for c in rec[:5]]
    assert any(c in top_ids for c in ["soybean", "cotton", "maize", "jowar"])

# Scenario 6: Hilly land with high rainfall
def test_scenario_6_hilly_land_high_rainfall():
    loc = location_service.resolve_location("Kodagu")
    soil = {"soil_colour": "Red", "soil_texture": "Loamy", "drainage": "Water drains quickly", "soil_depth": "Deep"}
    water = {"irrigation_source": "Rainfed farming", "availability_duration": "Throughout season"}
    land = {"slope_type": "Steep or hilly land"}
    weather = {
        "location": "Kodagu", "current_temperature_c": 22.0, "is_live_data": True,
        "historical_normal_rainfall_mm": 2725.0
    }
    rec, filtered, quality = scoring_service.evaluate_candidates(
        location=loc, soil_obs=soil, water_avail=water, land_profile=land,
        season="Kharif", weather=weather
    )
    filtered_ids = [f["crop_id"] for f in filtered]
    # Paddy cannot be grown on steep hills unless terraced; Sugarcane excluded
    assert "sugarcane" in filtered_ids

# Scenario 7: Rainfed cultivation with expected dry spell
def test_scenario_7_rainfed_dry_spell(mock_weather):
    mock_weather["consecutive_dry_days_forecast"] = 6
    loc = location_service.resolve_location("Vijayapura")
    soil = {"soil_colour": "Dark black", "soil_texture": "Clayey", "drainage": "Water drains moderately", "soil_depth": "Medium"}
    water = {"irrigation_source": "Rainfed farming", "availability_duration": "Limited water availability"}
    land = {"slope_type": "Flat land"}
    
    rec, filtered, quality = scoring_service.evaluate_candidates(
        location=loc, soil_obs=soil, water_avail=water, land_profile=land,
        season="Kharif", weather=mock_weather
    )
    top_crops = [c["crop"]["id"] for c in rec[:5]]
    # Drought-hardy dryland staples (Jowar, Sunflower, Red Gram) should rank higher than water thirsty crops
    assert any(c in top_crops for c in ["jowar", "sunflower", "red_gram"])

# Scenario 8: Limited irrigation during growing season
def test_scenario_8_limited_irrigation_short_duration(mock_weather):
    loc = location_service.resolve_location("Gadag")
    soil = {"soil_colour": "Brown", "soil_texture": "Loamy", "drainage": "Water drains moderately", "soil_depth": "Medium"}
    water = {"irrigation_source": "Borewell", "availability_duration": "Water available during certain months"}
    land = {"slope_type": "Flat land"}
    
    rec, filtered, quality = scoring_service.evaluate_candidates(
        location=loc, soil_obs=soil, water_avail=water, land_profile=land,
        season="Kharif", weather=mock_weather
    )
    # Short-duration pulses (Green gram ~70 days, Black gram ~80 days, Sunflower ~90 days) should score well
    rec_ids = [c["crop"]["id"] for c in rec[:5]]
    assert any(c in rec_ids for c in ["green_gram", "black_gram", "sunflower"])

# Scenario 9: Unknown soil colour
def test_scenario_9_unknown_soil_colour(mock_weather):
    loc = location_service.resolve_location("Bengaluru Rural")
    soil = {"soil_colour": "Unknown", "soil_texture": "Loamy", "drainage": "Water drains moderately", "soil_depth": "Medium"}
    water = {"irrigation_source": "Borewell", "availability_duration": "Throughout season"}
    land = {"slope_type": "Flat land"}
    
    rec, filtered, quality = scoring_service.evaluate_candidates(
        location=loc, soil_obs=soil, water_avail=water, land_profile=land,
        season="Kharif", weather=mock_weather
    )
    assert len(rec) > 0
    # Reliability penalty applied
    assert quality["reliability_score_pct"] <= 95.0
    assert "Soil Colour" in quality["missing_fields"]

# Scenario 10: Unknown soil texture
def test_scenario_10_unknown_soil_texture(mock_weather):
    loc = location_service.resolve_location("Kolar")
    soil = {"soil_colour": "Red", "soil_texture": "Unknown", "drainage": "Unknown", "soil_depth": "Medium"}
    water = {"irrigation_source": "Rainfed farming", "availability_duration": "Throughout season"}
    land = {"slope_type": "Flat land"}
    
    rec, filtered, quality = scoring_service.evaluate_candidates(
        location=loc, soil_obs=soil, water_avail=water, land_profile=land,
        season="Kharif", weather=mock_weather
    )
    assert len(rec) > 0
    # Heavy reliability penalty applied
    assert quality["reliability_score_pct"] <= 75.0
    assert "Soil Texture" in quality["missing_fields"]

# Scenario 11: Missing weather information (offline baseline)
def test_scenario_11_missing_live_weather():
    offline_weather = weather_service._get_imd_climatological_baseline("Bagalkote", 16.18, 75.69, 562.0)
    assert offline_weather["is_live_data"] is False
    assert "IMD 30-Year Climatological" in offline_weather["source"]
    
    loc = location_service.resolve_location("Bagalkote")
    soil = {"soil_colour": "Dark black", "soil_texture": "Clayey", "drainage": "Water drains moderately", "soil_depth": "Deep"}
    water = {"irrigation_source": "Rainfed farming", "availability_duration": "Throughout season"}
    land = {"slope_type": "Flat land"}
    
    rec, filtered, quality = scoring_service.evaluate_candidates(
        location=loc, soil_obs=soil, water_avail=water, land_profile=land,
        season="Rabi", weather=offline_weather
    )
    assert len(rec) > 0
    assert any("Weather" in m for m in quality["missing_fields"])

# Scenario 12: Missing location information
def test_scenario_12_missing_location():
    # Resolving with unknown district gives honest unverified fallback
    loc = location_service.resolve_location("NonExistentDistrict")
    assert loc["is_verified"] is False
    assert loc["zone_id"] == 5

# Scenario 13: Conflicting agricultural inputs
def test_scenario_13_conflicting_inputs(mock_weather):
    # Paddy in rainfed Northern Dry zone with only 500 mm rain
    loc = location_service.resolve_location("Vijayapura")
    soil = {"soil_colour": "Dark black", "soil_texture": "Clayey", "drainage": "Water drains moderately", "soil_depth": "Deep"}
    water = {"irrigation_source": "Rainfed farming", "availability_duration": "Limited water availability"}
    land = {"slope_type": "Flat land"}
    
    rec, filtered, quality = scoring_service.evaluate_candidates(
        location=loc, soil_obs=soil, water_avail=water, land_profile=land,
        season="Kharif", weather=mock_weather
    )
    filtered_ids = [f["crop_id"] for f in filtered]
    # Hard constraint must catch conflicting paddy/sugarcane
    assert "paddy" in filtered_ids
    assert "sugarcane" in filtered_ids

# Scenario 14: Unsupported district
def test_scenario_14_unsupported_district():
    dist = location_service.get_district_by_name("Jaipur")
    assert dist is None

# Scenario 15: Crop comparison test
def test_scenario_15_crop_comparison():
    res = comparison_service.compare_crops(["ragi", "jowar", "groundnut"])
    assert len(res["crops"]) == 3
    assert res["crops"][0]["crop_id"] == "ragi"
    assert "economics" in res["crops"][0]
