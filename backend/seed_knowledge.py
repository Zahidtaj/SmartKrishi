"""Traceable bilingual Agricultural Knowledge Centre seed articles."""

KNOWLEDGE_SEED_DATA: list[dict] = [
    {
        "slug": "soil-ph-nutrient-availability-guide",
        "category": "soil",
        "title_en": "Understanding Soil pH and Nutrient Availability",
        "title_kn": "ಮಣ್ಣಿನ ಪಿಎಚ್ (pH) ಮತ್ತು ಪೋಷಕಾಂಶಗಳ ಲಭ್ಯತೆ",
        "summary_en": "Why soil acidity and alkalinity control how effectively crops absorb Nitrogen, Phosphorus, Potassium, and micronutrients.",
        "summary_kn": "ಮಣ್ಣಿನ ಆಮ್ಲೀಯತೆ ಮತ್ತು ಕ್ಷಾರೀಯತೆ ಬೆಳೆಗಳು ಸಾರಜನಕ, ರಂಜಕ ಹಾಗೂ ಪೊಟ್ಯಾಶ್ ಹೀರಿಕೊಳ್ಳುವುದನ್ನು ಹೇಗೆ ನಿಯಂತ್ರಿಸುತ್ತದೆ ಎಂಬುದರ ಮಾಹಿತಿ.",
        "content_en": (
            "Soil pH measures acidity or alkalinity on a 0-14 scale. Most field crops perform best between pH 6.0 and 7.5 because essential macro and micronutrients remain soluble in soil water.\n\n"
            "Acidic soils (pH < 5.5), common in Karnataka's Coastal and Malnad laterite zones, can lock up Phosphorus and cause aluminium toxicity; agricultural lime application is guided strictly by buffer-pH soil testing.\n\n"
            "Alkaline/sodic soils (pH > 8.2), seen in pockets of Northern Dry Zone black soils, reduce Zinc and Iron availability. Gypsum amendment combined with organic compost and drainage improvement is recommended only after a formal Soil Health Card lab report."
        ),
        "content_kn": (
            "ಮಣ್ಣಿನ ಪಿಎಚ್ (pH) 0 ರಿಂದ 14ರ ಮಾಪಕದಲ್ಲಿ ಮಣ್ಣಿನ ಆಮ್ಲೀಯತೆ ಅಥವಾ ಕ್ಷಾರೀಯತೆಯನ್ನು ಸೂಚಿಸುತ್ತದೆ. ಬಹುತೇಕ ಬೆಳೆಗಳಿಗೆ pH 6.0 ರಿಂದ 7.5 ಅತ್ಯುತ್ತಮವಾಗಿದ್ದು ಪೋಷಕಾಂಶಗಳು ಸುಲಭವಾಗಿ ಲಭ್ಯವಾಗುತ್ತವೆ.\n\n"
            "ಕರಾವಳಿ ಮತ್ತು ಮಲೆನಾಡಿನ ಲ್ಯಾಟರೈಟ್ ಮಣ್ಣುಗಳಲ್ಲಿ ಕಂಡುಬರುವ ಆಮ್ಲೀಯ ಮಣ್ಣಿನಲ್ಲಿ (pH < 5.5) ರಂಜಕ ಲಭ್ಯತೆ ಕಡಿಮೆಯಾಗುತ್ತದೆ. ಮಣ್ಣು ಪರೀಕ್ಷೆಯ ವರದಿ ಆಧರಿಸಿ ಸುಣ್ಣ ಬಳಸುವುದು ಸೂಕ್ತ.\n\n"
            "ಉತ್ತರ ಕರ್ನಾಟಕದ ಕೆಲವು ಕಪ್ಪು ಮಣ್ಣಿನ ಭಾಗಗಳಲ್ಲಿ ಕ್ಷಾರೀಯತೆ (pH > 8.2) ಹೆಚ್ಚಾದಾಗ ಸತು ಮತ್ತು ಕಬ್ಬಿಣದ ಕೊರತೆ ಕಾಣಿಸುತ್ತದೆ. ಪ್ರಯೋಗಾಲಯದ ಮಣ್ಣು ಆರೋಗ್ಯ ಚೀಟಿ ಆಧರಿಸಿ ಜಿಪ್ಸಂ ಮತ್ತು ಸಾವಯವ ಗೊಬ್ಬರ ಬಳಸಬೇಕು."
        ),
        "source_name": "Soil Health Card Portal (Dept. of Agriculture & Farmers Welfare, GoI)",
        "source_url": "https://soilhealth.dac.gov.in/",
    },
    {
        "slug": "karnataka-cropping-seasons-kharif-rabi-zaid",
        "category": "seasons",
        "title_en": "Cropping Seasons in Karnataka: Kharif, Rabi, and Zaid",
        "title_kn": "ಕರ್ನಾಟಕದ ಕೃಷಿ ಹಂಗಾಮುಗಳು: ಮುಂಗಾರು, ಹಿಂಗಾರು ಮತ್ತು ಬೇಸಿಗೆ",
        "summary_en": "An overview of Karnataka's three major sowing windows, monsoon dependencies, and typical crop choices across dry and transition zones.",
        "summary_kn": "ಕರ್ನಾಟಕದ ಮುಂಗಾರು (ಖರೀಫ್), ಹಿಂಗಾರು (ರಬಿ) ಮತ್ತು ಬೇಸಿಗೆ (ಜಾಯದ್) ಬಿತ್ತನೆ ಅವಧಿಗಳು ಹಾಗೂ ಮಳೆ ಆಧಾರಿತ ಬೆಳೆ ಆಯ್ಕೆಯ ಮಾರ್ಗದರ್ಶಿ.",
        "content_en": (
            "1. Kharif (Mungaru / June-October): Driven by the Southwest Monsoon. Rainfed red-soil regions sow Ragi, Groundnut, Maize, and Pulses (Tur, Greengram), while assured irrigated and coastal belts grow Paddy.\n\n"
            "2. Rabi (Hingaru / October-February): Relies on Northeast Monsoon and residual moisture in deep black soils of Northern Karnataka. Key crops include Rabi Jowar, Chickpea (Bengal Gram), Safflower, and irrigated Maize.\n\n"
            "3. Zaid / Summer (Besige / February-May): Requires assured borewell, canal, or tank irrigation. Short-duration crops such as Watermelon, Muskmelon, Summer Groundnut, and Vegetables fit this window."
        ),
        "content_kn": (
            "1. ಮುಂಗಾರು (ಖರೀಫ್ / ಜೂನ್-ಅಕ್ಟೋಬರ್): ನೈಋತ್ಯ ಮುಂಗಾರು ಮಳೆಯನ್ನು ಅವಲಂಬಿಸಿದೆ. ಕೆಂಪು ಮಣ್ಣಿನ ಪ್ರದೇಶಗಳಲ್ಲಿ ರಾಗಿ, ಶೇಂಗಾ, ಮೆಕ್ಕೆಜೋಳ, ತೊಗರಿ ಹಾಗೂ ಕರಾವಳಿ/ನೀರಾವರಿ ಪ್ರದೇಶಗಳಲ್ಲಿ ಭತ್ತ ಬೆಳೆಯಲಾಗುತ್ತದೆ.\n\n"
            "2. ಹಿಂಗಾರು (ರಬಿ / ಅಕ್ಟೋಬರ್-ಫೆಬ್ರವರಿ): ಈಶಾನ್ಯ ಮಳೆ ಮತ್ತು ಉತ್ತರ ಕರ್ನಾಟಕದ ಆಳವಾದ ಕಪ್ಪು ಮಣ್ಣಿನ ತೇವಾಂಶವನ್ನು ಅವಲಂಬಿಸಿದೆ. ಹಿಂಗಾರು ಜೋಳ, ಕಡಲೆ, ಕುಸುಬೆ ಪ್ರಮುಖ ಬೆಳೆಗಳು.\n\n"
            "3. ಬೇಸಿಗೆ (ಜಾಯದ್ / ಫೆಬ್ರವರಿ-ಮೇ): ಕೊಳವೆ ಬಾವಿ ಅಥವಾ ಕಾಲುವೆ ನೀರಾವರಿ ಸೌಲಭ್ಯವಿರುವ ಕಡೆ ಕಲ್ಲಂಗಡಿ, ಕರಬೂಜ, ಬೇಸಿಗೆ ಶೇಂಗಾ ಮತ್ತು ತರಕಾರಿಗಳನ್ನು ಬೆಳೆಯಲಾಗುತ್ತದೆ."
        ),
        "source_name": "Raitha Mitra - Karnataka State Department of Agriculture",
        "source_url": "https://raitamitra.karnataka.gov.in/",
    },
    {
        "slug": "micro-irrigation-moisture-conservation",
        "category": "water",
        "title_en": "Water Conservation: Drip Irrigation and Rainfed Moisture Practices",
        "title_kn": "ಜಲ ಸಂರಕ್ಷಣೆ: ಹನಿ ನೀರಾವರಿ ಮತ್ತು ಮಳೆಯಾಶ್ರಿತ ತೇವಾಂಶ ನಿರ್ವಹಣೆ",
        "summary_en": "Practical ways to improve crop water-use efficiency through drip fertigation, mulching, and compartmental bunding.",
        "summary_kn": "ಹನಿ ನೀರಾವರಿ, ಮಲ್ಚಿಂಗ್ ಮತ್ತು ಅಡ್ಡ ಬದುಗಳ ಮೂಲಕ ನೀರಿನ ದಕ್ಷತೆಯನ್ನು ಹೆಚ್ಚಿಸುವ ಪ್ರಾಯೋಗಿಕ ವಿಧಾನಗಳು.",
        "content_en": (
            "Agricultural irrigation efficiency improves substantially when water reaches the root zone directly with minimal evaporation loss.\n\n"
            "- Drip and Micro-Sprinklers: Especially valuable in row and horticultural crops (Sugarcane, Pomegranate, Banana, Vegetables), cutting conveyance and evaporation waste compared to flood irrigation.\n"
            "- Mulching: Crop residue or organic mulch reduces soil surface temperature and moisture evaporation between irrigations.\n"
            "- Compartmental Bunding & Broad-Bed Furrow (BBF): Recommended by UAS Dharwad and Bengaluru for dryland black and red soils to capture rainwater in-situ before sowing."
        ),
        "content_kn": (
            "ನೀರು ಆವಿಯಾಗುವುದನ್ನು ತಡೆದು ನೇರವಾಗಿ ಬೇರಿನ ವಲಯಕ್ಕೆ ತಲುಪಿಸಿದಾಗ ಕೃಷಿ ನೀರಿನ ಬಳಕೆ ದಕ್ಷತೆ ಹೆಚ್ಚುತ್ತದೆ.\n\n"
            "- ಹನಿ ಮತ್ತು ತುಂತುರು ನೀರಾವರಿ: ಕಬ್ಬು, ದಾಳಿಂಬೆ, ಬಾಳೆ ಮತ್ತು ತರಕಾರಿ ಬೆಳೆಗಳಲ್ಲಿ ಹರಿ ನೀರಾವರಿಗೆ ಹೋಲಿಸಿದರೆ ಗಮನಾರ್ಹ ನೀರು ಉಳಿತಾಯವಾಗುತ್ತದೆ.\n"
            "- ಹೊದಿಕೆ (Mulching): ಬೆಳೆ ಉಳಿಕೆ ಅಥವಾ ಸಾವಯವ ಹೊದಿಕೆಯಿಂದ ಮಣ್ಣಿನ ತೇವಾಂಶ ದೀರ್ಘಕಾಲ ಉಳಿಯುತ್ತದೆ.\n"
            "- ಅಡ್ಡ ಬದು ಮತ್ತು ಇಳಿಜಾರಿಗೆ ಅಡ್ಡಲಾಗಿ ಉಳುಮೆ: ಒಣ ಭೂಮಿಯಲ್ಲಿ ಮಳೆ ನೀರನ್ನು ಹೊಲದಲ್ಲೇ ಇಂಗಿಸಲು ವಿಶ್ವವಿದ್ಯಾಲಯಗಳು ಶಿಫಾರಸು ಮಾಡುತ್ತವೆ."
        ),
        "source_name": "ICAR & University of Agricultural Sciences (UAS) Bengaluru / Dharwad",
        "source_url": "https://icar.org.in/",
    },
    {
        "slug": "integrated-nutrient-crop-rotation",
        "category": "sustainability",
        "title_en": "Crop Rotation and Integrated Nutrient Management (INM)",
        "title_kn": "ಬೆಳೆ ಪರಿವರ್ತನೆ ಮತ್ತು ಸಮಗ್ರ ಪೋಷಕಾಂಶ ನಿರ್ವಹಣೆ (INM)",
        "summary_en": "How rotating cereals with pulses and combining farmyard manure with soil-test-based fertilizers sustains long-term yield.",
        "summary_kn": "ಏಕದಳ ಬೆಳೆಗಳೊಂದಿಗೆ ದ್ವಿದಳ ಧಾನ್ಯಗಳನ್ನು ಪರಿವರ್ತಿಸುವುದು ಮತ್ತು ಸಾವಯವ-ರಾಸಾಯನಿಕ ಗೊಬ್ಬರ ಸಮತೋಲನದ ಮಹತ್ವ.",
        "content_en": (
            "Continuous monocropping of heavy-feeder cereals (Rice, Maize, Sugarcane) depletes specific soil nutrients and increases pest carry-over.\n\n"
            "Rotating cereals or cotton with legumes (Tur, Chickpea, Blackgram, Greengram, Groundnut) adds biologically fixed nitrogen through root nodules and breaks soil-borne disease cycles.\n\n"
            "Integrated Nutrient Management combines well-decomposed farmyard manure (FYM) or compost, biofertilizers (Rhizobium, Azospirillum, PSB), and balanced NPK matched to an actual Soil Health Card report."
        ),
        "content_kn": (
            "ಒಂದೇ ಬೆಳೆಯನ್ನು (ಭತ್ತ, ಮೆಕ್ಕೆಜೋಳ, ಕಬ್ಬು) ನಿರಂತರವಾಗಿ ಬೆಳೆಯುವುದರಿಂದ ಮಣ್ಣಿನ ಪೋಷಕಾಂಶಗಳು ಕ್ಷೀಣಿಸಿ ಕೀಟ-ರೋಗಗಳ ಬಾಧೆ ಹೆಚ್ಚಾಗುತ್ತದೆ.\n\n"
            "ತೊಗರಿ, ಕಡಲೆ, ಉದ್ದು, ಹೆಸರು ಅಥವಾ ಶೇಂಗಾದಂತಹ ದ್ವಿದಳ ಬೆಳೆಗಳೊಂದಿಗೆ ಬೆಳೆ ಪರಿವರ್ತನೆ ಮಾಡುವುದರಿಂದ ಮಣ್ಣಿನಲ್ಲಿ ನೈಸರ್ಗಿಕ ಸಾರಜನಕ ಸ್ಥಿರೀಕರಣವಾಗುತ್ತದೆ.\n\n"
            "ಸಮಗ್ರ ಪೋಷಕಾಂಶ ನಿರ್ವಹಣೆಯಲ್ಲಿ ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರ, ಜೈವಿಕ ಗೊಬ್ಬರಗಳು (ರೈಜೋಬಿಯಂ, ಪಿ.ಎಸ್.ಬಿ) ಮತ್ತು ಮಣ್ಣು ಪರೀಕ್ಷಾ ವರದಿ ಆಧಾರಿತ ರಸಗೊಬ್ಬರಗಳನ್ನು ಸಮತೋಲನದಲ್ಲಿ ಬಳಸಲಾಗುತ್ತದೆ."
        ),
        "source_name": "ICAR Integrated Nutrient Management Guidelines",
        "source_url": "https://icar.org.in/",
    },
    {
        "slug": "agricultural-terminology-glossary",
        "category": "terminology",
        "title_en": "Essential Agricultural Terminology for Farmers and Students",
        "title_kn": "ರೈತರು ಮತ್ತು ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಪ್ರಮುಖ ಕೃಷಿ ಪದಕೋಶ",
        "summary_en": "Clear definitions of Soil pH, NPK, Agro-Climatic Zone, Crop Duration, Evapotranspiration, and Rainfed vs. Irrigated farming.",
        "summary_kn": "ಮಣ್ಣಿನ ಪಿಎಚ್, ಎನ್.ಪಿ.ಕೆ, ಕೃಷಿ-ಹವಾಮಾನ ವಲಯ, ಬೆಳೆ ಅವಧಿ ಮತ್ತು ಮಳೆಯಾಶ್ರಿತ ಬೇಸಾಯ ಪದಗಳ ಸರಳ ವಿವರಣೆ.",
        "content_en": (
            "- NPK (kg/ha): Available Nitrogen (N - vegetative leaf growth), Phosphorus (P - root and flower development), and Potassium (K - disease tolerance and grain filling).\n"
            "- Soil Health Card (SHC): A standardized Indian government soil-test report detailing macro/micronutrient status and crop-wise corrective recommendations.\n"
            "- Agro-Climatic Zone: A geographic zone classified by rainfall pattern, soil group, temperature, and topography (Karnataka is divided into 10 NARP agro-climatic zones).\n"
            "- Rainfed vs. Protective Irrigation: Rainfed depends solely on rainfall; protective irrigation supplies 1-2 critical waterings during dry spells."
        ),
        "content_kn": (
            "- ಎನ್.ಪಿ.ಕೆ (NPK): ಸಾರಜನಕ (ಸಸ್ಯದ ಎಲೆ ಬೆಳವಣಿಗೆ), ರಂಜಕ (ಬೇರು ಮತ್ತು ಹೂ ಬಿಡಲು), ಮತ್ತು ಪೊಟ್ಯಾಶ್ (ರೋಗ ನಿರೋಧಕತೆ ಹಾಗೂ ಕಾಳು ತುಂಬಲು).\n"
            "- ಮಣ್ಣು ಆರೋಗ್ಯ ಚೀಟಿ (SHC): ಮಣ್ಣು ಪರೀಕ್ಷಾ ಪ್ರಯೋಗಾಲಯದಿಂದ ನೀಡುವ ಮಣ್ಣಿನ ಪೋಷಕಾಂಶಗಳ ಅಧಿಕೃತ ವರದಿ.\n"
            "- ಕೃಷಿ-ಹವಾಮಾನ ವಲಯ: ಮಳೆ, ಮಣ್ಣಿನ ಪ್ರಕಾರ ಮತ್ತು ಹವಾಮಾನದ ಆಧಾರದ ಮೇಲೆ ವಿಂಗಡಿಸಲಾದ ಪ್ರದೇಶ (ಕರ್ನಾಟಕದಲ್ಲಿ 10 ವಲಯಗಳಿವೆ).\n"
            "- ಮಳೆಯಾಶ್ರಿತ ಬೇಸಾಯ: ಸಂಪೂರ್ಣವಾಗಿ ಮಳೆಯನ್ನು ಅವಲಂಬಿಸಿದ ಕೃಷಿ ಪದ್ಧತಿ."
        ),
        "source_name": "SmartKrishi Agricultural Glossary (compiled from ICAR & UAS public glossaries)",
        "source_url": None,
    },
    {
        "slug": "karnataka-official-agricultural-portals",
        "category": "government",
        "title_en": "Official Agricultural Resources and Expert Support Channels",
        "title_kn": "ಅಧಿಕೃತ ಕೃಷಿ ಸಂಪನ್ಮೂಲಗಳು ಮತ್ತು ತಜ್ಞರ ಮಾರ್ಗದರ್ಶನ ಕೇಂದ್ರಗಳು",
        "summary_en": "Verified public portals and local extension institutions where farmers can verify soil tests, weather bulletins, and crop advisories.",
        "summary_kn": "ಮಣ್ಣು ಪರೀಕ್ಷೆ, ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ ಮತ್ತು ಅಧಿಕೃತ ಬೆಳೆ ಸಲಹೆ ಪಡೆಯಲು ಸಂಪರ್ಕಿಸಬಹುದಾದ ಸರ್ಕಾರಿ ಮತ್ತು ವಿಶ್ವವಿದ್ಯಾಲಯದ ಸಂಸ್ಥೆಗಳು.",
        "content_en": (
            "Before finalizing high-investment sowing decisions, verify automated guidance with local agricultural institutions:\n\n"
            "1. Raitha Samparka Kendra (RSK) / Taluk Assistant Director of Agriculture Office: Local seed availability, soil sample collection, and taluk-level advisories (https://raitamitra.karnataka.gov.in/).\n"
            "2. Krishi Vigyan Kendra (KVK): District-level ICAR extension centres operated by UAS Bengaluru, UAS Dharwad, UAS Raichur, and KSNUAHS Shivamogga.\n"
            "3. Soil Health Card Portal: Official repository for soil testing lab locations and nutrient cards (https://soilhealth.dac.gov.in/).\n"
            "4. IMD Agromet Advisory Services: Official district agro-meteorological weather bulletins (https://agromet.imd.gov.in/).\n\n"
            "Note: SmartKrishi does not collect subsidy applications or display live helpline numbers here—please consult your nearest Raitha Samparka Kendra directly for verified district office contacts."
        ),
        "content_kn": (
            "ಹೆಚ್ಚಿನ ಬಂಡವಾಳ ಹೂಡುವ ಬೆಳೆ ನಿರ್ಧಾರಗಳಿಗೆ ಮುನ್ನ ಸ್ಥಳೀಯ ಕೃಷಿ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ:\n\n"
            "1. ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರ (RSK) / ತಾಲ್ಲೂಕು ಕೃಷಿ ಇಲಾಖೆ ಕಚೇರಿ: ಬಿತ್ತನೆ ಬೀಜ, ಮಣ್ಣು ಪರೀಕ್ಷೆ ಮಾಹಿತಿ ಮತ್ತು ತಾಲ್ಲೂಕು ಮಟ್ಟದ ಸಲಹೆಗಾಗಿ (https://raitamitra.karnataka.gov.in/).\n"
            "2. ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರ (KVK): ಬೆಂಗಳೂರು, ಧಾರವಾಡ, ರಾಯಚೂರು ಮತ್ತು ಶಿವಮೊಗ್ಗ ಕೃಷಿ ವಿಶ್ವವಿದ್ಯಾಲಯಗಳ ಜಿಲ್ಲಾ ವಿಸ್ತರಣಾ ಕೇಂದ್ರಗಳು.\n"
            "3. ಮಣ್ಣು ಆರೋಗ್ಯ ಚೀಟಿ ಜಾಲತಾಣ: ಅಧಿಕೃತ ಮಣ್ಣು ಪರೀಕ್ಷಾ ಪ್ರಯೋಗಾಲಯ ಮಾಹಿತಿ (https://soilhealth.dac.gov.in/).\n"
            "4. ಐಎಂಡಿ ಅಗ್ರೋಮೆಟ್: ಜಿಲ್ಲಾ ಕೃಷಿ-ಹವಾಮಾನ ಬುಲೆಟಿನ್ (https://agromet.imd.gov.in/)."
        ),
        "source_name": "Karnataka Dept. of Agriculture / ICAR / IMD Agromet Public Portals",
        "source_url": "https://raitamitra.karnataka.gov.in/",
    },
    {
        "slug": "ragi-and-pulse-intercropping-karnataka",
        "category": "cultivation",
        "title_en": "Ragi + Red Gram (Akkadi) Intercropping in Dryland Karnataka",
        "title_kn": "ಒಣ ಭೂಮಿ ಕರ್ನಾಟಕದಲ್ಲಿ ರಾಗಿ + ತೊಗರಿ ಅಕ್ಕಡಿ ಬೆಳೆ ಪದ್ಧತಿ",
        "summary_en": "Traditional risk-buffering mixed cropping geometry recommended for Southern and Eastern Dry Zones of Karnataka.",
        "summary_kn": "ದಕ್ಷಿಣ ಮತ್ತು ಪೂರ್ವ ಒಣ ವಲಯಗಳಲ್ಲಿ ಮಳೆ ಅನಿಶ್ಚಿತತೆಯನ್ನು ಎದುರಿಸಲು ಶಿಫಾರಸು ಮಾಡಲಾದ ಅಕ್ಕಡಿ ಸಾಲು ಪದ್ಧತಿ.",
        "content_en": (
            "In Karnataka's Eastern and Southern Dry Zones, pairing shallow-rooted Ragi (8 rows) with deep-rooted Pigeonpea/Tur (2 rows) provides dual benefits:\n\n"
            "- Risk mitigation: If mid-season dry spells affect Ragi grain filling, deep-rooted Tur continues utilizing subsoil moisture.\n"
            "- Soil enrichment: Tur leaf litter and root nitrogen fixation improve organic matter for the subsequent crop."
        ),
        "content_kn": (
            "ಕರ್ನಾಟಕದ ಪೂರ್ವ ಮತ್ತು ದಕ್ಷಿಣ ಒಣ ವಲಯಗಳಲ್ಲಿ 8 ಸಾಲು ರಾಗಿಯೊಂದಿಗೆ 2 ಸಾಲು ತೊಗರಿ (ಅಕ್ಕಡಿ ಸಾಲು) ಬೆಳೆಯುವುದರಿಂದ ಎರಡು ಪ್ರಮುಖ ಲಾಭಗಳಿವೆ:\n\n"
            "- ಮಳೆ ಅಪಾಯ ಕಡಿಮೆ: ಮಧ್ಯಂತರ ಬರ ಬಂದರೆ ಆಳ ಬೇರಿನ ತೊಗರಿ ಮಣ್ಣಿನ ಆಳದ ತೇವಾಂಶದಿಂದ ಬೆಳೆ ಉಳಿಸಿಕೊಳ್ಳುತ್ತದೆ.\n"
            "- ಮಣ್ಣಿನ ಫಲವತ್ತತೆ: ತೊಗರಿ ಎಲೆ ಉದುರುವಿಕೆ ಮತ್ತು ಸಾರಜನಕ ಸ್ಥಿರೀಕರಣ ಮಣ್ಣನ್ನು ಉತ್ತಮಗೊಳಿಸುತ್ತದೆ."
        ),
        "source_name": "UAS Bengaluru Dryland Agriculture Project (GKVK)",
        "source_url": "https://uasbangalore.edu.in/",
    },
]
