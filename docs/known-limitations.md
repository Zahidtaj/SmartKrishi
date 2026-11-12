# Known Limitations & Honest Prototype Boundaries

1. **Observations Do Not Measure Nutrients or pH**: Soil colour (`red`, `dark_black`, etc.) and hand-feel texture only guide physical water retention, drainage, and structural suitability. Farmers needing fertilizer rates should obtain a laboratory Soil Health Card from their nearest Raitha Samparka Kendra (RSK) or KVK.
2. **Weather Provider Availability**: SmartKrishi keeps verified long-term Karnataka NARP zone normals strictly separate from live weather APIs. When external live weather is disabled or unreachable, live observations and 7-day forecasts display `unavailable` — values are never fabricated.
3. **Geographical Scope**: Regional location-to-zone verification currently covers 131 taluks across Karnataka's 10 NARP Agro-Climatic Zones. Expansion to other states requires adding verified district-taluk zone tables.
4. **Illustrative Economic Figures**: Crop comparison cost, yield, and price figures (`prototype_demonstration`) use documented 1-acre assumptions rather than live APMC mandi price feeds.
5. **Suitability Score**: The 0-100 suitability score is an explainable prototype ranking index, not a statistical yield probability or agronomic guarantee.
