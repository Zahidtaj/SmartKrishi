# Agricultural Data Sources Registry & Provenance
## SmartKrishi System &bull; Verification & Traceability Standard

### 1. Data Source Policy
To prevent algorithmic hallucination and preserve trust, SmartKrishi enforces strict data classification across all system modules:
- **Verified**: Published in authoritative agricultural university manuals, ICAR publications, or government gazettes.
- **External Live Data**: Real-time APIs from accredited meteorological agencies (Open-Meteo / WMO compliant).
- **Demonstration / Unverified**: Clearly tagged and separated; never presented as authoritative advice.

---

### 2. Primary Data Sources Registry

#### A. University of Agricultural Sciences, Bengaluru (UASB)
- **Publication**: *Package of Practices for Field Crops and Horticulture (Southern and Eastern Dry Zones)*.
- **URL**: `https://uasbangalore.edu.in`
- **Data Extracted**:
  - Ragi (GPU-28, ML-365, Indaf-7) sowing windows and spacing.
  - Groundnut (TMV-2, KCG-2) soil requirements (friable sandy loam, gypsum application).
  - Crop water requirements, irrigation frequency, drought coping intercrops (Ragi + Red gram 4:2 / 8:2).
- **Geographic Coverage**: Zones 4, 5, 6, 7 (Southern and Eastern Karnataka).
- **Status**: `Verified` (PoP 2023-24).

#### B. University of Agricultural Sciences, Dharwad (UASD)
- **Publication**: *Package of Practices for Dryland and Irrigated Crops (Northern Transition and Dry Zones)*.
- **URL**: `https://uasd.edu`
- **Data Extracted**:
  - Rabi Jowar (M 35-1 Maldandi) deep black soil moisture conservation practices.
  - Chickpea (Annigeri-1, JG-11) temperature thresholds and wilt management.
  - Cotton (Bt hybrids) and Soybean (JS-335, DSb-21) spacing and waterlogging vulnerabilities.
- **Geographic Coverage**: Zones 1, 2, 3, 8 (Northern Karnataka).
- **Status**: `Verified` (PoP 2022-24).

#### C. Karnataka State Department of Agriculture (KSDA) & Planning Commission
- **Publication**: *Agro-Climatic Atlas and District Profile of Karnataka*.
- **URL**: `https://raitamitra.karnataka.gov.in`
- **Data Extracted**:
  - Official delineation of 10 agro-climatic zones across 31 districts.
  - District normal rainfall, dominant soil associations, drought vulnerability index.
- **Geographic Coverage**: Statewide (Karnataka).
- **Status**: `Verified`.

#### D. India Meteorological Department (IMD)
- **Publication**: *District Climatological Rainfall and Temperature Normals (1981-2010 Epoch)*.
- **URL**: `https://mausam.imd.gov.in`
- **Data Extracted**:
  - 30-year district average monthly precipitation and mean maximum/minimum temperatures.
  - Agrometeorological advisory thresholds for dry spells and heavy rainfall alerts.
- **Status**: `Verified` (Historical Climatological Baseline).

#### E. Open-Meteo High-Resolution Numerical Weather Service
- **Service**: Global Numerical Weather Prediction (WMO / ECMWF / DWD Ingestion).
- **URL**: `https://open-meteo.com`
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0).
- **Parameters Queried**:
  - Hourly and current 2m temperature (°C).
  - Relative humidity (%).
  - 10m wind speed (km/h).
  - 7-day daily precipitation sum (mm) and rain probability (%).
- **Fallback Policy**: If the Open-Meteo API experiences latency or network disconnects, the system instantly switches to IMD 30-year climatological normals with an explicit telemetry flag.
- **Status**: `External Live Data`.

#### F. Commission for Agricultural Costs and Prices (CACP)
- **Publication**: *Price Policy for Kharif and Rabi Crops (2024-25 Season)*.
- **URL**: `https://cacp.dacnet.nic.in`
- **Data Extracted**:
  - Official Minimum Support Price (MSP) benchmarks for Paddy, Ragi, Jowar, Maize, Groundnut, Red Gram, Green Gram, Chickpea, Cotton, Soybean, Sunflower, Sesamum.
  - Fair and Remunerative Price (FRP) for Sugarcane.
  - Average cost of cultivation estimates ($A_2 + FL$).
- **Status**: `Verified` (Benchmark only, non-guaranteed).
