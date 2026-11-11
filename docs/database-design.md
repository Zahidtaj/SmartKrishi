# Database Design

SmartKrishi implements 13 relational tables in `backend/models.py` using SQLAlchemy 2.x (12 core domain entities plus `admin_users`):

1. `farmers` — Pseudonymous session preference (`session_label`, `preferred_language`). No phone numbers or personal IDs stored.
2. `locations` — Hierarchical State / District / Taluk records mapped to Karnataka's 10 NARP Agro-Climatic Zones (`zone_code`, `normal_annual_rainfall_mm`, `dominant_soil_types`), uniquely constrained on `(state, district, taluk)`.
3. `soil_records` — Soil type, optional `ph`, `nitrogen`, `phosphorus`, `potassium`, `measurement_source` (`soil_test` | `estimate` | `unavailable`), and optional `soil_test_date`.
4. `farm_profiles` — Village (optional), season, irrigation type, water availability, land area, farming method, previous crop, and climate estimates/source.
5. `crops` — Core crop master records (`crop_key` unique, bilingual EN/KN names & guidance, duration range, water demand mm, seed rate, `in_ml_dataset`, `record_status`, `information_source`).
6. `crop_requirements` — 1-to-1 agronomic envelope (`suitable_soil_types`, `ph_min`/`max`/`optimal`, NPK bounds, temperature/humidity/rainfall ranges, seasons, supported water levels).
7. `regional_crop_rules` — Configurable state/zone/season suitability rules (`recommended`, `conditional`, `restricted`).
8. `recommendations` — Logged recommendation execution header (`mode_used`, `confidence_level`, `input_snapshot`, `warnings`, `insufficient_data_reason`, `model_version`).
9. `recommendation_results` — Ranked top-3 crop outcomes linked via foreign key (`rank`, `illustrative_score`, `ml_probability`, `dimension_scores`, bilingual reasons/limitations, `conflict_flags`).
10. `crop_economic_data` — Illustrative cultivation cost, expected yield, indicative price, and explicit assumptions per acre (`data_status = prototype_demonstration`).
11. `knowledge_articles` — Categorized bilingual guides with `source_name` and `source_url`.
12. `feedback` — Non-personal user feedback with `CheckConstraint` (`rating` 1..5) and review status.
13. `admin_users` — Administrator account table storing salted `PBKDF2-HMAC-SHA256` password hashes (`310,000` iterations).
