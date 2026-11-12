# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

React, TypeScript, Vite, Tailwind CSS, Lucide Icons, and Recharts (Frontend); Python 3.13, FastAPI, Pydantic, SQLAlchemy, and SQLite with PostgreSQL-compatible models (Backend & Database); Pandas, NumPy, and Scikit-learn Random Forest classification combined with an explicit agronomic rule engine (ML & Decision Support). Specified by the project Master Development Instruction.

## Users

- Primary users: Farmers and agricultural decision-makers in Karnataka, India (with architecture extensible to other Indian states) seeking crop selection guidance matched to soil, region, season, climate, and water availability.
- Secondary users: Agricultural extension educators, VTU community project reviewers, and local administrators managing verified crop rules, knowledge articles, and user feedback.

## Product Purpose

SmartKrishi is an agricultural decision-support platform that helps farmers answer practical pre-cultivation questions: which crops suit their land, geographical taluk/district, soil profile, growing season, and water availability; how candidate crops compare across agronomic requirements and clearly labelled economic assumptions; and what soil-health and agronomic practices apply before sowing.

## Positioning

Unlike opaque single-label ML demos or lab-only soil calculators, SmartKrishi leads with an **observation-based and location-aware agricultural decision-support engine** (`backend/rules/agronomic_rules.py` + `backend/services/soil_observation_service.py` + `backend/services/weather_service.py`) grounded in verified Karnataka NARP Agro-Climatic Zone profiles (`KA-Z1`..`KA-Z10`), paired with transparent constraint checks, honest uncertainty reporting, and institutional references.

## Operating Context

- Desktop, laptop, tablet, and Android mobile web browsers in English and Kannada (`en`, `kn`), supporting both Dark Mode (deep emerald/forest) and Light Mode with a smooth circular View Transitions reveal.
- Farmers answer plain-language visual, physical feel, drainage, topography, water source, optional history, and seasonal planning questions across an 8-step guided flow — never required to enter laboratory N, P, K, or pH measurements (`"Not sure"` and `"Unknown"` supported explicitly).
- Local and containerized prototype running FastAPI + SQLite; strictly separates long-term climate normals from optional live weather feeds and reports live weather as `unavailable` when disabled or unreachable rather than fabricating data.

## Capabilities and Constraints

- Guided **8-step observation-based advisory wizard**:
  1. Location (State, District, linked Taluk, optional Village, auto-mapped NARP Agro-Climatic Zone)
  2. Soil Appearance (8 verified educational SVG soil swatches + disclaimer that color does not establish fertility or pH)
  3. Soil Texture (Sandy, Clayey, Loamy, Silty, Mixed, Not sure + expandable visual & ribbon feel guide)
  4. Water Drainage & Moisture Retention (post-rain infiltration & dry-period retention observations)
  5. Land Characteristics (slope/topography, approximate depth, visible stones, waterlogging, erosion)
  6. Water Availability (source & seasonal reliability)
  7. Farming History (clearly optional previous crop, past drought/flood, recurring pests, land area)
  8. Season & Planning (season, intended sowing month, duration preference, main farming priority)
- Transparent 7-stage Recommendation Engine returning up to 3 ranked crops with **Why this crop was recommended**, **Conditions to consider before cultivation**, **Information that is still missing**, `input_provenance`, Physical Soil & Land Synthesis, and a dedicated **Weather and Farming Advisory** card.
- Up-to-3 Crop Comparison with agronomic metrics, Recharts visualizations, and explicitly documented illustrative economic assumptions.
- **Soil Observation & Soil Health module** (`/soil-health`): physical field-observation interpreter (`POST /api/soil/observe`) upfront, plus a clearly optional, collapsible Soil Health Card laboratory pH/NPK reference calculator (`POST /api/soil/analyze`).
- Categorized Agricultural Knowledge Centre with traceable institutional sources (`UAS Bengaluru`, `UAS Dharwad`, `ICAR`, `Karnataka Dept of Agriculture`, `Soil Health Card`) — zero invented schemes or helpline numbers.
- Bilingual English and Kannada UI + explanations; Admin management module protected with `PBKDF2-HMAC-SHA256` password hashing and signed local-dev bearer tokens.

## Brand Commitments

- Name: SmartKrishi
- Visual direction: Refined deep-emerald/forest analytics surfaces (`Dark Mode` default + `Light Mode` toggle with circular reveal), restrained botanical green accents, warm neutral inks, rectangular/soft-card surfaces with smooth animated transitions, and an original botanical SVG welcome intro (`WelcomeAnimation.tsx`, auto-completing without a "Skip intro" button and respecting `prefers-reduced-motion`).
- Custom sprout/plant-inspired SVG & ICO favicon (`favicon.svg`, `favicon.ico`, PNG).
- Zero fake testimonials, zero fake counters, zero AI-slop stock images, zero emoji interface icons (Lucide only).

## Evidence on Hand

- Public crop recommendation dataset (`datasets/raw/crop_recommendation.csv`, 2,200 records across 22 crop classes with N, P, K, temperature, humidity, pH, rainfall).
- Documented dataset provenance and limitations in `datasets/metadata/crop_recommendation_provenance.json`.
- Structured Karnataka district/taluk/agro-climatic zone reference data and documented crop agronomic profiles in `backend/seed.py`.
- Absence explicitly noted: no live weather API connection, no live Mandi market feed, and prototype economic figures are explicitly marked as illustrative reference estimates requiring local expert verification.

## Product Principles

1. Honesty over false precision: never override critical water, pH, or seasonal constraints with ML confidence; refuse or warn when data is insufficient.
2. Explainability first: every recommendation and economic row shows why it matched, its limitations, its assumptions, and its source.
3. Bilingual accessibility: natural English and accurate Kannada across navigation, forms, validations, and recommendation reasoning.
4. Separation of concerns: keep ML pipelines, agronomic rules, database models, API endpoints, and frontend UI cleanly decoupled.

## Accessibility & Inclusion

- WCAG AA contrast (>=4.5:1 body text, >=3:1 large text & UI controls) on dark surfaces.
- Full keyboard navigation, visible focus rings, `aria-describedby` inline validation errors, and `prefers-reduced-motion` bypass for the welcome animation and transitions.
- Mobile-responsive structural layout tested down to 375px / 390px for Android mobile users.
