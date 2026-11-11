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

Unlike opaque single-label ML demos, SmartKrishi uses a transparent hybrid engine: a Random Forest classifier trained on a documented public soil-climate dataset combined with configurable agronomic rules, hard constraint checks, transparent dimension scoring, and explicit limitation/insufficient-data warnings.

## Operating Context

- Desktop, laptop, tablet, and Android mobile web browsers used in English and Kannada (`en`, `kn`, extensible for `hi`).
- Inputs distinguish measured soil test data (Soil Health Card values with test date) from approximate estimates and allow reduced-information mode when lab data is missing.
- Local development prototype running FastAPI + SQLite locally; never claims real-time external weather APIs or scientifically validated profit guarantees when not connected.

## Capabilities and Constraints

- Structured multi-section recommendation form: Location (State, District, linked Taluk, Village, Agro-climatic Zone), Soil (Type, pH, N, P, K, test source & date), Farming Conditions (Season, Irrigation, Water availability, Area, Method, Previous crop), Climate (Temperature, Humidity, Rainfall with measurement provenance).
- Hybrid Recommendation Engine returning up to 3 ranked crops (or honest insufficient-data / conflict explanations) with dimension scores, reasons, limitations, duration, water needs, and cultivation guidance.
- Up-to-3 Crop Comparison with agronomic metrics, Recharts visualizations where informative, and explicitly documented economic assumptions (clearly separating verified agronomic reference data from prototype illustrative economic ranges).
- Soil Health Information module (pH & NPK reference ranges, testing method notes, Soil Health Card upload roadmap note).
- Categorized Agricultural Knowledge Centre with traceable sources (ICAR, UAS Bengaluru/Dharwad, Raitha Mitra / Karnataka Dept of Agriculture, Soil Health Card portal) — zero invented schemes or helpline numbers.
- Bilingual English and Kannada UI + explanations; Admin management module protected with real password hashing (`PBKDF2-HMAC-SHA256`) and signed local-dev tokens.

## Brand Commitments

- Name: SmartKrishi
- Visual direction specified by brief: dark-first interface, deep charcoal and forest-inspired dark surfaces, restrained natural green accents, warm neutral text, selective glassmorphism on navigation/overlays/selected panels, opaque reading surfaces, rectangular or subtly rounded buttons (no purple gradient pill buttons), and an original plant-growth SVG welcome animation (seed -> root -> stem -> leaves -> wordmark) with `prefers-reduced-motion` support.
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
