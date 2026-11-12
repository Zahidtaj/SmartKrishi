"""Comprehensive observation-based recommendation tests covering all 9 required agronomic scenarios."""


def _base_payload(**overrides):
    data = {
        "state": "Karnataka",
        "district": "Tumakuru",
        "taluk": "Tumakuru",
        "soil_color": "red",
        "soil_texture": "loamy",
        "drainage_after_rain": "moderately",
        "moisture_retention": "short_period",
        "soil_depth": "medium",
        "visible_stones": "none_few",
        "waterlogging_issue": "none",
        "erosion_issue": "none",
        "land_topography": "flat",
        "water_source": "borewell",
        "water_reliability": "certain_months",
        "season": "Kharif",
        "intended_sowing_month": "June",
        "duration_preference": "flexible",
        "farming_priority": "land_suitability",
        "language": "en",
    }
    data.update(overrides)
    return data


def test_scenario_1_red_soil_limited_irrigation(client):
    """Red soil + limited irrigation should recommend drought-hardy dryland crops, NOT Rice/Sugarcane."""
    resp = client.post(
        "/api/recommendations",
        json=_base_payload(
            district="Kolar",
            taluk="Kolar",
            soil_color="red",
            soil_texture="loamy",
            water_source="borewell",
            water_reliability="limited",
            farming_priority="low_water",
        ),
    )
    assert resp.status_code == 201
    data = resp.json()
    top_keys = [r["crop_key"] for r in data["recommendations"]]
    assert top_keys
    assert "rice" not in top_keys
    assert "sugarcane" not in top_keys
    assert any(k in top_keys for k in ("ragi", "groundnut", "pigeonpeas", "jowar", "mungbean", "blackgram"))
    assert "NO" not in data["soil_interpretation"]["color_disclaimer_en"] or "pH" in data["soil_interpretation"]["color_disclaimer_en"]


def test_scenario_2_black_clayey_soil_waterlogging(client):
    """Black clayey soil + frequent waterlogging should warn strongly and downgrade sensitive upland crops."""
    resp = client.post(
        "/api/recommendations",
        json=_base_payload(
            district="Kalaburagi",
            taluk="Kalaburagi",
            soil_color="dark_black",
            soil_texture="clayey",
            drainage_after_rain="remains_days",
            moisture_retention="several_days",
            soil_depth="deep",
            waterlogging_issue="frequent",
            land_topography="low_lying",
            water_source="canal",
            water_reliability="throughout_season",
            season="Kharif",
        ),
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["soil_interpretation"]["effective_drainage"] == "waterlogging_prone"
    assert any("waterlogging" in w.lower() for w in data["warnings"])
    assert data["weather_advisory"]["farming_advisory"]["heavy_rainfall_risk_level"] == "high"
    # Groundnut cannot thrive in multi-day waterlogged clay
    top_keys = [r["crop_key"] for r in data["recommendations"]]
    assert "groundnut" not in top_keys


def test_scenario_3_sandy_soil_low_water(client):
    """Sandy soil + scarce/rainfed water should favor low-water crops & avoid high-water crops."""
    resp = client.post(
        "/api/recommendations",
        json=_base_payload(
            district="Chitradurga",
            taluk="Challakere",
            soil_color="sandy_pale",
            soil_texture="sandy",
            drainage_after_rain="very_quickly",
            moisture_retention="dries_quickly",
            water_source="rainfed",
            water_reliability="limited",
            season="Kharif",
            farming_priority="low_water",
        ),
    )
    assert resp.status_code == 201
    data = resp.json()
    top_keys = [r["crop_key"] for r in data["recommendations"]]
    assert "rice" not in top_keys
    assert "sugarcane" not in top_keys
    assert any(k in top_keys for k in ("ragi", "groundnut", "mungbean", "mothbeans", "blackgram"))
    assert data["weather_advisory"]["farming_advisory"]["dry_spell_risk_level"] == "high"


def test_scenario_4_loamy_soil_moderate_irrigation(client):
    """Loamy soil + moderate irrigation should give balanced transitional crops with high/moderate confidence."""
    resp = client.post(
        "/api/recommendations",
        json=_base_payload(
            district="Hassan",
            taluk="Hassan",
            soil_color="reddish_brown",
            soil_texture="loamy",
            drainage_after_rain="moderately",
            moisture_retention="short_period",
            soil_depth="deep",
            water_source="borewell",
            water_reliability="certain_months",
            season="Kharif",
            intended_sowing_month="June",
            previous_crop="Ragi",
        ),
    )
    assert resp.status_code == 201
    data = resp.json()
    assert len(data["recommendations"]) == 3
    top_keys = [r["crop_key"] for r in data["recommendations"]]
    assert any(k in top_keys for k in ("maize", "ragi", "blackgram", "pigeonpeas", "cotton"))
    assert "provenance" not in data or "farmer_observed" in data["input_provenance"]


def test_scenario_5_hilly_land_high_rainfall(client):
    """Hilly land in Kodagu high rainfall zone should prioritize hill/plantation or valley-adapted options with slope notes."""
    resp = client.post(
        "/api/recommendations",
        json=_base_payload(
            district="Kodagu",
            taluk="Madikeri",
            soil_color="reddish_brown",
            soil_texture="loamy",
            drainage_after_rain="moderately",
            moisture_retention="several_days",
            soil_depth="deep",
            erosion_issue="mild",
            land_topography="steep_hilly",
            water_source="rainfed",
            water_reliability="certain_months",
            season="Perennial",
            intended_sowing_month="June",
        ),
    )
    assert resp.status_code == 201
    data = resp.json()
    top_keys = [r["crop_key"] for r in data["recommendations"]]
    assert any(k in top_keys for k in ("coffee", "orange", "coconut"))
    assert any("contour" in g.lower() for g in data["soil_interpretation"]["management_guidance_en"])


def test_scenario_6_flat_land_seasonal_rainfall(client):
    """Flat rainfed land in Rabi Northern Dry Zone should recommend Rabi crops (e.g. chickpea, jowar)."""
    resp = client.post(
        "/api/recommendations",
        json=_base_payload(
            district="Vijayapura",
            taluk="Vijayapura",
            soil_color="dark_black",
            soil_texture="clayey",
            drainage_after_rain="moderately",
            moisture_retention="several_days",
            soil_depth="deep",
            land_topography="flat",
            water_source="rainfed",
            water_reliability="limited",
            season="Rabi",
            intended_sowing_month="October",
            farming_priority="household_food",
        ),
    )
    assert resp.status_code == 201
    data = resp.json()
    top_keys = [r["crop_key"] for r in data["recommendations"]]
    assert any(k in top_keys for k in ("chickpea", "jowar", "maize"))


def test_scenario_7_missing_soil_info(client):
    """Missing/uncertain soil observations should still run responsibly and lower confidence."""
    resp = client.post(
        "/api/recommendations",
        json=_base_payload(
            district="Mandya",
            taluk="Mandya",
            soil_color="mixed_uncertain",
            soil_texture="not_sure",
            drainage_after_rain="not_sure",
            moisture_retention="not_sure",
            soil_depth="unknown",
            visible_stones="not_sure",
            waterlogging_issue="not_sure",
            erosion_issue="not_sure",
            water_source="rainfed",
            water_reliability="uncertain",
            intended_sowing_month=None,
        ),
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["confidence_level"] == "low"
    assert len(data["recommendations"]) >= 1
    assert "soil_texture" in data["missing_information"]
    assert "drainage_after_rain" in data["missing_information"]
    assert data["insufficient_data_reason"] is not None
    assert len(data["recommendations"][0]["missing_info_en"]) >= 1


def test_scenario_8_unknown_soil_color(client):
    """Unknown soil color alone should reduce caution note without guessing NPK or failing."""
    resp = client.post(
        "/api/recommendations",
        json=_base_payload(
            district="Dharwad",
            taluk="Dharwad",
            soil_color="mixed_uncertain",
            soil_texture="loamy",
            drainage_after_rain="moderately",
            moisture_retention="short_period",
            soil_depth="medium",
            water_source="rainfed",
            water_reliability="certain_months",
            season="Kharif",
        ),
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "soil_color" in data["soil_interpretation"]["unknown_fields"]
    assert "cannot measure pH" in data["soil_interpretation"]["color_disclaimer_en"]
    assert len(data["recommendations"]) == 3


def test_scenario_9_unavailable_live_weather_data(client):
    """Unavailable live weather must report unavailable honestly without fabricating weather metrics."""
    resp = client.post(
        "/api/recommendations",
        json=_base_payload(
            district="Bengaluru Rural",
            taluk="Devanahalli",
            simulate_weather_unavailable=True,
        ),
    )
    assert resp.status_code == 201
    data = resp.json()
    weather = data["weather_advisory"]
    assert weather["current_weather"]["status"] == "unavailable"
    assert weather["current_weather"]["temperature_c"] is None
    assert weather["short_term_forecast"]["status"] == "unavailable"
    assert weather["short_term_forecast"]["next_7_days_rain_total_mm"] is None
    assert weather["long_term_climate"]["status"] == "available"
    assert weather["farming_advisory"]["live_weather_available"] is False
    assert "live_weather_forecast" in data["missing_information"]

    # Also test GET retrieval of persisted recommendation
    get_resp = client.get(f"/api/recommendations/{data['recommendation_id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["weather_advisory"]["current_weather"]["status"] == "unavailable"


def test_validation_and_unknown_location_return_structured_errors(client):
    bad_location = client.post(
        "/api/recommendations",
        json=_base_payload(district="MarsDistrict", taluk="MarsTaluk"),
    )
    assert bad_location.status_code == 404
    assert bad_location.json()["code"] == "HTTP_404"

    bad_payload = client.post(
        "/api/recommendations",
        json=_base_payload(land_area_acres=-5),
    )
    assert bad_payload.status_code == 422
    assert bad_payload.json()["code"] == "VALIDATION_ERROR"
