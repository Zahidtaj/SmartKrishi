# REST API Documentation & Endpoints Specification
## SmartKrishi Backend Web Services Specification

### 1. API Architecture Overview
- **Base URL**: `http://localhost:8000/api`
- **Framework**: FastAPI (Asynchronous Python 3.13)
- **Interactive Documentation**:
  - Swagger UI: `http://localhost:8000/docs`
  - ReDoc: `http://localhost:8000/redoc`
- **Response Format**: `application/json`

---

### 2. Endpoints Directory

#### A. Health and System Status
- **`GET /api/health`**
  - **Description**: Verifies database connectivity, counts loaded districts and crops, and returns uptime status.
  - **Response 200**:
    ```json
    {
      "status": "healthy",
      "system": "SmartKrishi Decision Support System",
      "version": "1.0.0",
      "target_state": "Karnataka",
      "districts_loaded": 31,
      "crops_loaded": 16,
      "timestamp": "2026-11-16T12:00:00Z"
    }
    ```

#### B. Location Intelligence
- **`GET /api/locations/states`**: Returns administrative state list (`Karnataka`).
- **`GET /api/locations/districts`**: Returns all 31 Karnataka districts with coordinates, agro-climatic zone IDs, normal rainfall, and taluk lists.
- **`GET /api/locations/taluks?district={name}`**: Returns taluks for a given district.
- **`GET /api/locations/zones`**: Returns the 10 official Agro-Climatic Zones of Karnataka.
- **`GET /api/locations/resolve?district={name}&taluk={name}`**: Maps location to its agro-climatic zone without guessing. Also supports reverse GPS via `?lat={float}&lon={float}`.

#### C. Soil Observation Reference
- **`GET /api/soil/characteristics`**: Returns the authoritative reference dictionary covering textures, ribbon lengths, colour indicators, drainage descriptions, and depth profiles.

#### D. Crops Catalog
- **`GET /api/crops`**: Returns all 16 verified Karnataka field crops with agronomic requirements and economic benchmarks.
- **`GET /api/crops/{crop_id}`**: Returns single crop detailed agronomic requirements and UAS package of practices.

#### E. Core Recommendation Engine
- **`POST /api/recommendations`**
  - **Description**: Evaluates farmer observations, runs agricultural rule engine, filters hard constraints, calculates multi-dimensional suitability scores, and returns ranked crops with structured explanations.
  - **Request Body**:
    ```json
    {
      "state": "Karnataka",
      "district": "Chitradurga",
      "taluk": "Challakere",
      "soil_observation": {
        "soil_colour": "Red",
        "soil_texture": "Sandy",
        "drainage": "Water drains quickly",
        "moisture_retention": "Soil dries quickly",
        "soil_depth": "Medium",
        "presence_of_stones": false,
        "waterlogging_observed": false
      },
      "water_availability": {
        "irrigation_source": "Rainfed farming",
        "availability_duration": "Limited water availability",
        "has_drip_facility": false
      },
      "land_profile": {
        "slope_type": "Flat land",
        "approximate_area_acres": 2.0
      },
      "planned_season": "Kharif",
      "planned_sowing_month": "July",
      "farming_history": {
        "previous_crop": "Green gram",
        "was_successful": true
      }
    }
    ```
  - **Response 200**:
    ```json
    {
      "recommendation_id": 1,
      "location": { "district": "Chitradurga", "zone_id": 4, "normal_rainfall_mm": 574.0 },
      "agro_climatic_zone": { "id": 4, "name": "Central Dry Zone", "code": "ZONE_4" },
      "weather_summary": { "source": "Open-Meteo High-Resolution Forecast Model", "temperature_c": 28.5 },
      "reliability_score_pct": 100.0,
      "data_completeness_pct": 100.0,
      "missing_fields": [],
      "recommendations": [
        {
          "crop_id": "groundnut",
          "crop_name": "Groundnut (Peanut)",
          "rank": 1,
          "suitability_score": 92.4,
          "suitability_tier": "Highly Suitable",
          "reasons_for_selection": [ ... ],
          "supporting_soil_observations": [ ... ],
          "potential_risks": [ ... ]
        }
      ],
      "filtered_crops": [ ... ],
      "agricultural_disclaimer": "..."
    }
    ```

#### F. Crop Comparison
- **`POST /api/crops/compare`**
  - **Request Body**: `{"crop_ids": ["ragi", "jowar", "groundnut"]}`
  - **Response 200**: Returns side-by-side comparative matrix of agronomic requirements, water needs, duration, and economic indicators.

#### G. Weather and Agromet Advisories
- **`GET /api/weather/{district_name}`**: Current weather and 7-day projection.
- **`GET /api/advisories/{district_name}`**: Active sowing alerts, dry spell warnings, and heavy rainfall precautions.

#### H. Knowledge and Data Provenance
- **`GET /api/knowledge`**: Educational agronomic articles.
- **`GET /api/sources`**: Data sources registry with verification dates and status.
- **`POST /api/feedback`**: Submit farmer ratings and outcome notes.
