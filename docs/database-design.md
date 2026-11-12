# Database Design (SQLite & PostgreSQL Compatible)

SmartKrishi uses SQLAlchemy ORM models (`backend/models.py`) designed cleanly for local SQLite prototyping and seamless migration to PostgreSQL via `SMARTKRISHI_DATABASE_URL`.

## Core Tables

- **`locations`**: 131 Karnataka taluks across 25 districts mapped to the 10 NARP Agro-Climatic Zones (`KA-Z1`..`KA-Z10`), storing `typical_rainfall_pattern`, `dominant_soil_types`, `common_soil_textures`, `major_crops`, `recommended_seasons_summary`, `growing_period_info`, `regional_references`, `data_source`, `verification_status`, and `last_updated`.
- **`soil_records`**: Stores physical farmer observations (`soil_color`, `soil_texture`, `drainage_after_rain`, `moisture_retention`, `soil_depth`, `visible_stones`, `waterlogging_issue`, `erosion_issue`, `observation_confidence`) plus optional nullable legacy/Soil Health Card fields.
- **`farm_profiles`**: Stores `land_topography`, `water_source`, `water_reliability`, optional history (`previous_crop`, `previous_crop_success`, `drought_history`, `flood_history`, `pest_disease_history`, `land_area_acres`), and planning choices (`season`, `intended_sowing_month`, `duration_preference`, `farming_priority`).
- **`crops` & `crop_requirements`**: 26 structured crop profiles carrying `suitable_textures`, `suitable_drainage`, `moisture_needs`, `suitable_land_topography`, `min_soil_depth`, `drought_tolerance`, `waterlogging_tolerance`, `sowing_months`, `weather_risk_thresholds`, `duration_category`, `verification_status`, and `last_updated`.
- **`regional_crop_rules`**: Zone-season suitability rules (`recommended`, `conditional`, `restricted`) with English and Kannada agronomic notes and institutional citations.
- **`recommendations` & `recommendation_results`**: Persists each advisory session along with `soil_interpretation`, `weather_advisory`, `input_provenance` (`farmer_observed`, `institution_sourced`, `weather_provider_sourced`, `demonstration_data`), `missing_information`, ranked crop results, explicit reasons, limitations, and missing-field explanations.
- **`crop_economic_data`, `knowledge_articles`, `feedback`, `admin_users`**: Illustrative 1-acre economic comparison baselines, bilingual agronomic guides, community feedback, and PBKDF2-SHA256 admin moderation.
