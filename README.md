# SmartKrishi — Smart Crop Recommendation and Agricultural Decision Support System

SmartKrishi is a VTU Community Project web application designed to help farmers and agricultural decision-makers evaluate suitable crops using **farmer-friendly field observations and Karnataka location intelligence** — without requiring mandatory laboratory N, P, K, or pH measurements.

Farmers complete an **8-step guided wizard** (Location, Soil Appearance with educational soil swatches, Soil Texture + feel guide, Water Drainage & Moisture Retention, Land Characteristics, Water Availability, Optional Farming History, and Season & Planning). SmartKrishi pairs verified Karnataka NARP Agro-Climatic Zone profiles (`KA-Z1`–`KA-Z10`) with a transparent 7-stage agronomic rule engine, a physical Soil Observation Interpretation module, a Weather & Climate Intelligence module (strictly separating long-term climate normals from optional live weather feeds), bilingual English and Kannada explanations, Light/Dark mode with a circular reveal transition, crop comparison with illustrative economic assumptions, and an attribution-backed Agricultural Knowledge Centre.

## Technology Stack

- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS (Dark & Light modes), Lucide React icons, Recharts
- **Backend API:** Python 3.13, FastAPI, Pydantic v2, Uvicorn
- **Decision Engine & Optional ML:** Transparent 7-stage agronomic rule engine + Scikit-learn `RandomForestClassifier` (secondary/research baseline for optional lab workflows)
- **Database:** SQLite (local prototype) via SQLAlchemy 2.x (PostgreSQL-compatible relational schema)
- **Testing:** Pytest + FastAPI TestClient (backend & rules), Vitest + React Testing Library (frontend)

## Folder Structure

```text
SmartKrishi/
├── backend/
│   ├── config.py                  # Env settings, CORS, DB, & optional live weather toggle
│   ├── database.py                # SQLAlchemy engine & session management
│   ├── main.py                    # FastAPI app, SPA serving & global error handlers
│   ├── models.py                  # Relational ORM schema (12 core entities + AdminUser)
│   ├── regional_data.py           # Karnataka KA-Z1..KA-Z10 agronomic profiles & crop traits
│   ├── schemas.py                 # Pydantic v2 observation, weather, & advisory schemas
│   ├── security.py                # PBKDF2-HMAC-SHA256 password hashing & HMAC bearer tokens
│   ├── seed.py                    # Idempotent database initialization & seeding
│   ├── seed_locations.py          # Karnataka Districts, Taluks & 10 NARP Agro-Climatic Zones
│   ├── seed_crops.py              # Agronomic profiles, rules, & illustrative economic baselines
│   ├── seed_knowledge.py          # Bilingual Knowledge Centre articles with institutional sources
│   ├── rules/
│   │   ├── agronomic_rules.py     # 7-stage observation-based filtering, conflict caps & explanations
│   │   └── scoring.py             # Configurable dimension scoring weights & suitability labels
│   ├── services/
│   │   ├── recommendation_service.py
│   │   ├── soil_observation_service.py  # Physical soil observation synthesis (never guesses NPK/pH)
│   │   ├── weather_service.py           # Climate normals vs live weather/forecast module
│   │   ├── comparison_service.py
│   │   └── soil_health_service.py       # Optional lab Soil Health Card pH/NPK reference
│   ├── routers/                   # Modular REST API routers (locations, crops, recommendations, weather, knowledge, admin)
│   └── tests/                     # Pytest backend, scenario & ML test suites
├── datasets/
│   ├── raw/crop_recommendation.csv
│   ├── processed/dataset_validation_report.json
│   └── metadata/crop_recommendation_provenance.json
├── ml/                            # Standalone/secondary ML training & evaluation pipeline
├── frontend/
│   ├── public/                    # Custom SVG/ICO/PNG favicons, 26 crop SVGs & 8 soil swatches
│   └── src/
│       ├── api/                   # Typed REST client
│       ├── context/               # LanguageContext (en/kn) & ThemeContext (dark/light circular reveal)
│       ├── components/            # WelcomeAnimation, Navbar, Footer, CropDetailModal
│       ├── i18n/                  # English (en) & Kannada (kn) dictionaries
│       └── pages/                 # Home, Recommend (8-step), Results, Compare, SoilHealth, Knowledge, Admin, Legal
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

## Public Cloud Deployment (Access from Any Computer or Phone)

Because SmartKrishi runs a Python FastAPI + Scikit-learn backend alongside the React UI, it includes a unified single-container deployment setup ([Dockerfile](Dockerfile), [render.yaml](render.yaml), [railway.json](railway.json)) where FastAPI serves both `/api/*` and the built `frontend/dist` bundle over HTTPS:

1. **Render (Free Web Service):** Create a new Blueprint or Web Service on Render connected to `https://github.com/Zahidtaj/SmartKrishi` (`render.yaml` auto-configures the Docker build, `/api/health` check, and generated secrets).
2. **Railway:** Connect `https://github.com/Zahidtaj/SmartKrishi` in Railway (`railway.json` + `Dockerfile` configure build, port binding, and `/api/health` checks) and set `SMARTKRISHI_ADMIN_PASSWORD` and `SMARTKRISHI_TOKEN_SECRET`.

## API Endpoints Overview

- `GET /api/health` — Database and system readiness status
- `GET /api/locations/states` — Supported states
- `GET /api/locations/districts?state=Karnataka` — Districts mapped to agro-climatic zones
- `GET /api/locations/taluks?state=Karnataka&district=...` — Taluks with zone metadata, rainfall normals, soil groups, major crops, and institutional verification dates
- `GET /api/weather/advisory?state=Karnataka&district=...&taluk=...` — Modular weather & climate intelligence (long-term zone normals separated from live weather & seasonal outlook)
- `GET /api/crops` & `GET /api/crops/{crop_id}` — Crop catalog and full agronomic requirements
- `POST /api/recommendations` & `GET /api/recommendations/{id}` — Observation-based crop advisory generation & report retrieval
- `POST /api/crops/compare` — Side-by-side comparison of up to 3 crops with illustrative economic assumptions
- `POST /api/soil/observe` — Physical soil & field observation interpreter (color, texture, drainage, retention, depth, erosion)
- `POST /api/soil/analyze` — Optional Soil Health Card pH & NPK reference interpreter
- `GET /api/knowledge` & `GET /api/knowledge/{article_id}` — Categorized bilingual agricultural knowledge library
- `POST /api/feedback` — Non-personal user feedback submission
- `POST /api/admin/login`, `GET /api/admin/overview`, `PATCH /api/admin/crops/{id}`, `POST /api/admin/rules`, `POST /api/admin/knowledge`, `PATCH /api/admin/feedback/{id}` — Protected local-dev administration endpoints

## Dataset Provenance & Limitations

See [docs/dataset-sources.md](docs/dataset-sources.md) and [docs/known-limitations.md](docs/known-limitations.md) for full details on dataset origins, why raw ML accuracy must not be mistaken for real-world field validation, absence of live weather/APMC market feeds, and the illustrative status of economic benchmarks.
