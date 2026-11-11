# Recommendation Engine Design

SmartKrishi implements a transparent **hybrid recommendation engine** in `backend/rules/agronomic_rules.py`, `backend/rules/scoring.py`, and `backend/services/recommendation_service.py`.

## Processing Stages

### Stage 1: Input & Location Validation
- Incoming payloads are validated via Pydantic v2 (`ph` in 0-14, non-negative NPK, land area > 0, valid climate bounds).
- State, District, and Taluk must match a documented `Location` record (`422` otherwise).
- Biological non-arable extremes (e.g., `ph < 3.5` or `ph > 10.0`, temperature `< 2°C` or `> 48°C`) immediately return `mode_used = "insufficient_data"` with `recommendations = []` rather than forcing an unsafe crop.

### Stage 2: Hard Agronomic Constraint Gates
Each active crop is evaluated against hard regional, seasonal, and water constraints before composite ranking:
- **Regional Restriction Gate:** Crops marked `restricted` for Karnataka (e.g., temperate `apple`, Gangetic alluvial `jute`) are excluded regardless of ML class probability.
- **Season Gate:** Crops whose `suitable_seasons` exclude the farmer's chosen season (unless compatible perennial crops during Kharif/Rabi) are excluded.
- **Water Deficit Gate:** High-water crops (e.g., Sugarcane, Banana, and Paddy outside heavy-rainfall Coastal/Malnad belts) are excluded under `Rainfed` or `Limited irrigation` inputs.

### Stage 3: Configurable 6-Dimension Suitability Scoring
Non-excluded crops are scored across six configurable dimensions (`DEFAULT_WEIGHTS` in `backend/rules/scoring.py`):
- Location compatibility (`20%`)
- Soil texture & pH compatibility (`20%`)
- Water availability compatibility (`20%`)
- Seasonal alignment (`15%`)
- Climatic proximity (`15%`)
- Nutrient NPK proximity (`10%`)

### Stage 4: Bounded ML Blending & Reduced-Information Mode
- When full soil chemistry and climate values are provided (`hybrid_full`), Random Forest probabilities (`ml/predictor.py`) contribute a bounded `20%` weight (`ML_BLEND_FACTOR = 0.20`) ONLY for the 22 crops present in the training dataset.
- Documented Karnataka staples outside the public 22-crop CSV (`ragi`, `jowar`, `groundnut`, `sugarcane`) are scored fairly across the rule dimensions without penalty and explicitly tagged as rule-evaluated.
- When soil chemistry or climate values are missing (`reduced_information`), ML blending is bypassed, missing metrics receive neutral `0.5` proximity scores, confidence is downgraded to `reduced`, and explicit missing-field warnings are attached.
- If zero crops score >= `45.0`, SmartKrishi returns an honest `insufficient_data` notice instead of forcing a weak match.
