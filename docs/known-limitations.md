# Known Limitations and Roadmap

1. **No Live Weather API Integration:** Climatic inputs (temperature, humidity, rainfall) are manually entered estimates/measurements or taluk annual rainfall normals. Live forecast integration (e.g., IMD Agromet / Open-Meteo) is future work.
2. **No Live APMC Market Prices:** Economic comparisons rely on clearly tagged `prototype_demonstration` baselines per acre under documented assumptions and do not reflect daily APMC mandi prices.
3. **Soil Health Card Document Parsing:** Manual soil parameter entry is implemented; automated OCR/PDF parsing of government Soil Health Cards is planned for a future release.
4. **Geographic Coverage:** Initial release thoroughly covers Karnataka (131 taluks across districts and all 10 NARP agro-climatic zones); additional Indian states require curated district/taluk/zone seed tables.
5. **Nutrient Unit Differences:** The public ML dataset encodes N/P/K on a `0-140 / 5-145 / 5-205` comparative scale rather than standardized Soil Health Card laboratory extraction methods (Alkaline KMnO₄-N, Olsen-P, NH₄OAc-K). SmartKrishi explains this difference in the Soil Health module and withholds automated chemical fertilizer prescriptions.
6. **Local Development Admin Auth:** Administrator login uses PBKDF2-HMAC-SHA256 hashing and signed bearer tokens intended for local development prototype review; production deployment requires HTTPS, rotated secrets, and hardened session management.
7. **Illustrative Scoring:** Composite suitability percentages have not yet undergone multi-season field validation with agricultural university agronomists.
