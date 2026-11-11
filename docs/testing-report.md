# Testing Report — SmartKrishi

This report summarizes all automated and live end-to-end checks executed on the SmartKrishi prototype.

## 1. Machine Learning Pipeline Validation & Evaluation (`python -m ml.train`)

- **Dataset:** `datasets/raw/crop_recommendation.csv` (2,200 rows, 22 balanced crop classes, 7 features).
- **Data Validation (`ml/data_validator.py`):** 0 missing/NULL cells, 0 out-of-range values, 0 exact duplicates (`2,200` valid rows).
- **Split Discipline (`ml/preprocessor.py`):** Stratified 80/20 split (`1,760` train / `440` held-out test, `random_state=42`) performed prior to `StandardScaler` and `LabelEncoder` fitting.
- **Measured Metrics (`ml/artifacts/model_metrics.json`):**
  - Held-out Test Accuracy: `0.9955` (`99.55%`)
  - Macro Precision: `0.9957`
  - Macro Recall: `0.9955`
  - Macro F1 Score: `0.9955`
  - 5-Fold Stratified CV Macro F1: `0.9920 +/- 0.0067`
  - Overfitting Gap (`train - test`): `0.0045`

## 2. Backend & API Automated Test Suite (`pytest`)

17 Pytest tests in `backend/tests/` verifying:
- `GET /api/health` database & ML artifact readiness check
- Cascading `GET /api/locations/states`, `districts`, `taluks` and `404` on unknown district
- Valid hybrid recommendation (`POST /api/recommendations`) & retrieval (`GET /api/recommendations/{id}`)
- Regional & water hard constraint enforcement (excluding temperate `apple`, Gangetic `jute`, and dryland rainfed `rice`)
- Rabi black-soil evaluation (Dharwad -> Chickpea / Jowar)
- Reduced-information mode when soil NPK/pH marked unavailable
- Input validation (`422` on invalid pH `18.5`, negative NPK, empty payload, unsupported state)
- Extreme non-arable pH (`2.0`) returning `insufficient_data` with `recommendations = []`
- Safe `503` error handling on missing ML artifacts and safe `500` handling on simulated `SQLAlchemyError` without leaking stack traces
- Crop catalog (`26` crops), `404` on unknown crop, multi-crop comparison (`POST /api/crops/compare`)
- Soil health interpretation (`POST /api/soil/analyze`), Knowledge Centre (`GET /api/knowledge`), Feedback (`POST /api/feedback`)
- Protected Admin login (`401` on unauthorized/bad credentials, `200` with PBKDF2-SHA256 verified token)

## 3. Frontend Typechecking, Tests, Build & Design Checks

- `npm run lint` (`tsc --noEmit`): 0 TypeScript errors
- `npm run test` (`vitest run`): 4/4 component & user-interaction tests passing (EN/KN switching, cascading dropdowns, inline pH validation, recommendation flow, comparison matrix, soil health, knowledge centre, privacy/terms routing, welcome animation skip & `prefers-reduced-motion` bypass)
- `npm run build` (`tsc -b && vite build`): Production bundle built cleanly
- `impeccable detect --json`: 0 errors, 0 warnings across HTML/CSS/TSX targets

## 4. Live Full-Stack Browser Verification

Verified live running FastAPI (`http://127.0.0.1:8000`) + Vite (`http://127.0.0.1:5173`):
- Confirmed `200 OK` / `201 Created` across live location, recommendation, comparison, soil analysis, and knowledge API requests
- Verified mobile viewport layout at `390x844` with zero horizontal overflow; refined stepper label wrapping (`RecommendPage.tsx`) after inspecting the mobile screenshot so "Farming Conditions" no longer truncates.
