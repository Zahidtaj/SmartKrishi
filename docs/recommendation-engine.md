# Observation-Based & Location-Aware Recommendation Engine

SmartKrishi uses a transparent, deterministic 7-stage agronomic rule engine built around **farmer field observations** and **verified Karnataka agro-climatic zone data**, without requiring laboratory NPK or pH measurements.

## 1. Input Philosophy

- Mandatory laboratory soil tests (Nitrogen, Phosphorus, Potassium, pH) are removed from the primary workflow.
- Farmers step through 8 focused screens: Location, Soil Appearance, Soil Texture (hand feel), Water Drainage & Moisture Retention, Land Characteristics, Water Availability, Optional Farming History, and Season & Planning.
- Every uncertain field supports explicit `"Not sure"` / `"Unknown"` choices rather than forcing synthetic values.

## 2. Seven Evaluation Stages

1. **Regional & Agro-Climatic Compatibility (`location`)**: Resolves State, District, and Taluk to Karnataka NARP Zones (`KA-Z1` through `KA-Z10`). Out-of-zone crops (e.g., temperate apple, Indo-Gangetic jute) are strictly restricted.
2. **Seasonal & Sowing Window Compatibility (`seasonal`)**: Matches planned season (`Kharif`, `Rabi`, `Zaid`, `Perennial`) and compares intended sowing month against documented regional sowing calendars.
3. **Soil Observation & Land Compatibility (`soil_land`)**: Synthesizes soil texture (`sandy`, `clayey`, `loamy`, `silty`, `mixed`, `not_sure`), rain drainage (`very_quickly`, `moderately`, `remains_hours`, `remains_days`, `not_sure`), waterlogging tendency, soil depth, visible stones, erosion, and land topography (`flat`, `slightly_sloping`, `steep_hilly`, `low_lying`, `rocky_stony`). Soil colour is never treated as proof of NPK/pH fertility.
4. **Water & Moisture Compatibility (`water`)**: Combines irrigation source (`rainfed`, `borewell`, `open_well`, `canal`, `pond_reservoir`, `drip_irrigation`, `multiple_sources`) with seasonal reliability and dry-period soil moisture retention.
5. **Weather & Climate Risk Compatibility (`climate`)**: Uses long-term Karnataka zone temperature/rainfall normals plus live observations when connected; flags waterlogging and dry-spell risks at sensitive crop stages.
6. **Farming Priority & Duration Alignment (`priority_history`)**: Aligns recommendations with `low_water`, `short_duration`, `land_suitability`, `household_food`, or `commercial` priorities and requested crop duration.
7. **Crop Rotation & Field History (`priority_history`)**: Uses optional previous crop, drought/flood experience, and recurring pest notes to favor cereal-pulse rotations and warn on monocropping or flood vulnerability.

## 3. Output Transparency

Every recommendation card returns:
- **Why this crop was recommended**
- **Conditions to consider before cultivation**
- **Information that is still missing**
- **Weather and Farming Advisory** separating long-term zone normals from live observations (or marking live weather honestly as `unavailable`).
