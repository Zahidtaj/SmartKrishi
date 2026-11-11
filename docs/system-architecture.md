# System Architecture

SmartKrishi separates presentation, API validation, hybrid decision logic, ML training/inference, and relational persistence into distinct layers.

```text
[React + TypeScript + Vite UI] (EN / KN i18n)
         │  REST / JSON over Vite Dev Proxy (/api)
         ▼
[FastAPI Application (backend/main.py)]
   ├── Pydantic v2 Validation & Standardized JSON Error Handlers
   ├── Security Module (PBKDF2-HMAC-SHA256 + HMAC Bearer Tokens)
   ├── Services & Rule Engine
   │     ├── recommendation_service.py
   │     ├── agronomic_rules.py + scoring.py
   │     ├── comparison_service.py
   │     └── soil_health_service.py
   ├── ML Inference Wrapper (ml/predictor.py -> Joblib Pipeline)
   └── SQLAlchemy 2.x ORM (backend/models.py)
         │
         ▼
[SQLite Database (backend/data/smartkrishi.db)]  <── PostgreSQL-ready ORM schema
```

## Key Architectural Decisions

- **API-First Separation:** All business logic, ML inference, and validation live inside Python FastAPI services rather than frontend client code.
- **Fail-Safe Startup & Error Handling:** Global FastAPI exception handlers catch `RequestValidationError`, `HTTPException`, `SQLAlchemyError`, and unexpected errors without leaking stack traces or secrets.
- **PostgreSQL Migration Readiness:** Standard SQLAlchemy `Mapped` column types, explicit foreign keys, check constraints, and indexes avoid SQLite-only syntax inside ORM definitions.
