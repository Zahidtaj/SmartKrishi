# System Architecture

SmartKrishi separates presentation, API validation, observation-based decision logic, weather intelligence, optional ML lab analysis, and relational persistence into distinct layers.

```text
[React + TypeScript + Vite UI] (EN / KN i18n, Dark/Light Circular Theme)
         │  REST / JSON over Vite Dev Proxy (/api) or Single-Origin FastAPI
         ▼
[FastAPI Application (backend/main.py)]
   ├── Pydantic v2 Validation & Standardized JSON Error Handlers
   ├── Security Module (PBKDF2-HMAC-SHA256 + HMAC Bearer Tokens)
   ├── Services & 7-Stage Rule Engine
   │     ├── recommendation_service.py
   │     ├── agronomic_rules.py + scoring.py
   │     ├── soil_observation_service.py  (Primary field observation synthesis)
   │     ├── weather_service.py           (Climate normals vs live/forecast separation)
   │     ├── comparison_service.py
   │     └── soil_health_service.py       (Optional SHC pH/NPK reference)
   ├── Regional Knowledge Tables (backend/regional_data.py -> KA-Z1..KA-Z10)
   ├── Optional/Secondary ML Module (ml/predictor.py -> Joblib Pipeline)
   └── SQLAlchemy 2.x ORM (backend/models.py)
         │
         ▼
[SQLite Database (backend/data/smartkrishi.db)]  <── PostgreSQL-ready ORM schema
```

## Key Architectural Decisions

- **Observation-First Primary Flow:** The recommendation engine (`agronomic_rules.py` + `recommendation_service.py`) runs without mandatory lab N, P, K, or pH inputs and never infers soil chemical fertility from soil color alone.
- **Climate vs Weather Separation:** `weather_service.py` separates `long_term_climate` (from Karnataka agro-climatic zone metadata) from `current_weather` and `short_term_forecast`, returning `unavailable` cleanly when live weather is disabled (`SMARTKRISHI_ENABLE_LIVE_WEATHER=false`) or unreachable.
- **API-First Separation:** All business logic, agronomic profiles, and validation live inside Python FastAPI services rather than hardcoded frontend logic.
- **Fail-Safe Startup & Error Handling:** Global FastAPI exception handlers catch `RequestValidationError`, `HTTPException`, `SQLAlchemyError`, and unexpected errors without leaking stack traces or secrets.
- **PostgreSQL Migration Readiness:** Standard SQLAlchemy `Mapped` column types, explicit foreign keys, check constraints, and indexes avoid SQLite-only syntax inside ORM definitions.
