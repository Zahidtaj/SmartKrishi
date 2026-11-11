# SmartKrishi — Smart Crop Recommendation and Agricultural Decision Support System

SmartKrishi is a VTU Community Project web application designed to help farmers and agricultural decision-makers evaluate suitable crops based on soil characteristics, Karnataka geographical taluk/district location, growing season, climatic estimates, and water availability.

Instead of returning an opaque crop label from a machine learning classifier alone, SmartKrishi pairs a Scikit-learn Random Forest model with an explicit agronomic rule engine, hard regional/water/seasonal constraints, transparent scoring dimensions, bilingual English and Kannada explanations, crop comparison with documented economic assumptions, soil health interpretation, and an attribution-backed Agricultural Knowledge Centre.

## Technology Stack

- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Lucide React icons, Recharts
- **Backend API:** Python 3.13, FastAPI, Pydantic v2, Uvicorn
- **Machine Learning:** Pandas, NumPy, Scikit-learn (`RandomForestClassifier`), Joblib
- **Database:** SQLite (local prototype) via SQLAlchemy 2.x (PostgreSQL-compatible relational schema)
- **Testing:** Pytest + FastAPI TestClient (backend & ML), Vitest + React Testing Library (frontend)

## Folder Structure

```text
SmartKrishi/
├── backend/
│   ├── config.py                  # Env settings & CORS/DB configuration
│   ├── database.py                # SQLAlchemy engine & session management
│   ├── main.py                    # FastAPI app, middleware & global error handlers
│   ├── models.py                  # 13 SQLAlchemy relational models (12 core entities + AdminUser)
│   ├── schemas.py                 # Pydantic request/response schemas
│   ├── security.py                # PBKDF2-HMAC-SHA256 password hashing & HMAC bearer tokens
│   ├── seed.py                    # Idempotent database initialization & seeding
│   ├── seed_locations.py          # Karnataka Districts, Taluks & 10 NARP Agro-Climatic Zones
│   ├── seed_crops.py              # Agronomic profiles, rules, & illustrative economic baselines
│   ├── seed_knowledge.py          # Bilingual Knowledge Centre articles with institutional sources
│   ├── rules/
│   │   ├── agronomic_rules.py     # Regional, soil, pH, NPK, season, water & climate rule engine
│   │   └── scoring.py             # Configurable dimension scoring weights & suitability labels
│   ├── services/
│   │   ├── recommendation_service.py
│   │   ├── comparison_service.py
│   │   └── soil_health_service.py
│   ├── routers/                   # Modular REST API routers
│   └── tests/                     # Pytest backend & ML test suites
├── datasets/
│   ├── raw/crop_recommendation.csv
│   ├── processed/dataset_validation_report.json
│   └── metadata/crop_recommendation_provenance.json
├── ml/
│   ├── config.py
│   ├── data_loader.py
│   ├── data_validator.py
│   ├── preprocessor.py            # Stratified train/test split before scaler/encoder fit
│   ├── train.py
│   ├── evaluate.py                # Accuracy, Precision, Recall, F1, CV & Confusion Matrix
│   ├── serializer.py
│   ├── predictor.py
│   └── artifacts/
├── frontend/
│   ├── public/                    # Custom SVG/ICO/PNG favicons & 26 botanical crop SVGs
│   └── src/
│       ├── api/                   # Typed REST client
│       ├── components/            # WelcomeAnimation, Navbar, Footer, CropDetailModal
│       ├── i18n/                  # English (en) & Kannada (kn) dictionaries
│       └── pages/                 # Home, Recommend, Results, Compare, SoilHealth, Knowledge, Admin, Legal
├── docs/                          # Detailed technical & architectural documentation
├── PRODUCT.md
├── DESIGN.md
├── .env.example
└── pytest.ini
```

## Installation & Setup

### Prerequisites
- Python 3.11+ (verified on Python 3.13.14)
- Node.js 18+ and npm (verified on Node v22.20.0, npm 10.9.3)

### 1. Environment Configuration
Copy `.env.example` to `.env` inside `SmartKrishi/` and update secrets if needed:
```powershell
Copy-Item .env.example .env
```
Key environment variables:
- `SMARTKRISHI_ENV`: `development`
- `SMARTKRISHI_DATABASE_URL`: SQLite path (`sqlite:///./backend/data/smartkrishi.db`) or PostgreSQL URL
- `SMARTKRISHI_CORS_ORIGINS`: comma-separated allowed frontend origins (default `http://localhost:5173,http://127.0.0.1:5173`)
- `SMARTKRISHI_ADMIN_USERNAME`: local dev admin username (default `admin`)
- `SMARTKRISHI_ADMIN_PASSWORD`: local dev admin password (change in `.env` before shared use)
- `SMARTKRISHI_TOKEN_SECRET`: signing secret for local bearer tokens

### 2. Python Virtual Environment & Backend Dependencies
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

### 3. ML Model Training & Evaluation
```powershell
.\.venv\Scripts\python.exe -m ml.train
```
This validates `datasets/raw/crop_recommendation.csv` (2,200 rows, 22 classes), performs an 80/20 stratified train/test split before fitting preprocessing, trains the `RandomForestClassifier`, evaluates held-out metrics + 5-fold cross-validation, and writes artifacts under `ml/artifacts/`.

### 4. Database Initialization & Seeding
```powershell
.\.venv\Scripts\python.exe -m backend.seed
```
Creates all relational tables in `backend/data/smartkrishi.db` and seeds Karnataka locations (131 taluks across districts/zones), 26 crop profiles, regional crop rules, knowledge articles, and the hashed local development admin account.

### 5. Frontend Dependencies
```powershell
cd frontend
npm install
```

## Running the Application Locally

Start the FastAPI backend (Terminal 1, from `SmartKrishi/`):
```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Start the Vite frontend dev server (Terminal 2, from `SmartKrishi/frontend/`):
```powershell
npm run dev
```

- **Local Frontend URL:** `http://localhost:5173`
- **Backend API & OpenAPI Docs:** `http://127.0.0.1:8000/docs`

## Running Tests

### Backend & ML Tests (Pytest)
```powershell
.\.venv\Scripts\python.exe -m pytest
```

### Frontend Typecheck, Component Tests & Build
```powershell
cd frontend
npm run lint
npm run test
npm run build
```

## API Endpoints Overview

- `GET /api/health` — Database and ML model status
- `GET /api/locations/states` — Supported states
- `GET /api/locations/districts?state=Karnataka` — Districts mapped to agro-climatic zones
- `GET /api/locations/taluks?state=Karnataka&district=...` — Taluks with zone & reference rainfall
- `GET /api/crops` & `GET /api/crops/{crop_id}` — Crop catalog and full agronomic requirements
- `POST /api/recommendations` & `GET /api/recommendations/{id}` — Hybrid crop recommendation generation & report retrieval
- `POST /api/crops/compare` — Side-by-side comparison of up to 3 crops with economic assumptions
- `POST /api/soil/analyze` — Agronomic pH & NPK soil health interpretation
- `GET /api/knowledge` & `GET /api/knowledge/{article_id}` — Categorized bilingual agricultural knowledge library
- `POST /api/feedback` — Non-personal user feedback submission
- `POST /api/admin/login`, `GET /api/admin/overview`, `PATCH /api/admin/crops/{id}`, `POST /api/admin/rules`, `POST /api/admin/knowledge`, `PATCH /api/admin/feedback/{id}` — Protected local-dev administration endpoints

## Dataset Provenance & Limitations

See [docs/dataset-sources.md](docs/dataset-sources.md) and [docs/known-limitations.md](docs/known-limitations.md) for full details on dataset origins, why raw ML accuracy must not be mistaken for real-world field validation, absence of live weather/APMC market feeds, and the illustrative status of economic benchmarks.
