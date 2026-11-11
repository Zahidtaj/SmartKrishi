"""Soil health reference interpretation using ICAR / Soil Health Card standard agronomic thresholds."""

from backend.schemas import NutrientInterpretation, SoilAnalysisRequest, SoilAnalysisResponse

# Reference agronomic classes commonly used in Indian Soil Health Card (SHC) evaluations (kg/ha):
# Available Nitrogen (Alkaline KMnO4 method): Low < 280, Medium 280-560, High > 560 (dataset scale 0-140 maps relative availability)
# Available Phosphorus (Olsen/Bray P): Low < 10-12.5, Medium 12.5-25, High > 25 (Note: P2O5 equivalent ~23-57 kg/ha; dataset P is ~5-145)
# Available Potassium (Neutral Normal NH4OAc K): Low < 110-120, Medium 120-280, High > 280 (dataset K is ~5-205)
# Note: SmartKrishi clearly documents scale/testing-method context and refuses to prescribe fertilizer dosages blindly.


def analyze_soil_health(payload: SoilAnalysisRequest) -> SoilAnalysisResponse:
    interpretations: list[NutrientInterpretation] = []
    guidance_en: list[str] = []
    guidance_kn: list[str] = []

    # pH interpretation
    if payload.ph is None:
        interpretations.append(
            NutrientInterpretation(
                parameter="Soil pH",
                value=None,
                unit="pH",
                status="Not Provided",
                interpretation_en="No soil pH value supplied. Submit a Soil Health Card sample to verify acidity or alkalinity.",
                interpretation_kn="ಮಣ್ಣಿನ ಪಿಎಚ್ ಮೌಲ್ಯ ನೀಡಿಲ್ಲ. ಮಣ್ಣು ಆರೋಗ್ಯ ಚೀಟಿ ಪರೀಕ್ಷೆಯ ಮೂಲಕ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.",
                reference_range="6.0 - 7.5 (Neutral / Optimal for most crops)",
            )
        )
    elif payload.ph < 5.5:
        interpretations.append(
            NutrientInterpretation(
                parameter="Soil pH",
                value=payload.ph,
                unit="pH",
                status="Strongly Acidic",
                interpretation_en="Acidic soil can limit Phosphorus, Calcium, and Magnesium uptake and reduce pulse nodulation.",
                interpretation_kn="ಆಮ್ಲೀಯ ಮಣ್ಣು ರಂಜಕ ಲಭ್ಯತೆ ಮತ್ತು ದ್ವಿದಳ ಧಾನ್ಯಗಳ ಬೇರು ಗಂಟು ಬೆಳವಣಿಗೆಯನ್ನು ಕುಂಠಿತಗೊಳಿಸಬಹುದು.",
                reference_range="6.0 - 7.5 (Neutral / Optimal)",
            )
        )
        guidance_en.append("For acidic soils (pH < 5.5), consult a soil lab for lime-requirement testing before applying agricultural lime.")
        guidance_kn.append("ಆಮ್ಲೀಯ ಮಣ್ಣಿಗೆ (pH < 5.5) ಸುಣ್ಣ ಬಳಸುವ ಮುನ್ನ ಪ್ರಯೋಗಾಲಯದಲ್ಲಿ ಸುಣ್ಣದ ಅಗತ್ಯ ಪರೀಕ್ಷೆ ಮಾಡಿಸಿ.")
    elif payload.ph <= 7.5:
        interpretations.append(
            NutrientInterpretation(
                parameter="Soil pH",
                value=payload.ph,
                unit="pH",
                status="Optimal / Neutral",
                interpretation_en="Favorable pH range supporting balanced availability of major and micro nutrients.",
                interpretation_kn="ಪ್ರಮುಖ ಮತ್ತು ಸೂಕ್ಷ್ಮ ಪೋಷಕಾಂಶಗಳ ಸಮತೋಲಿತ ಲಭ್ಯತೆಗೆ ಉತ್ತಮ ಪಿಎಚ್ ವ್ಯಾಪ್ತಿ.",
                reference_range="6.0 - 7.5 (Neutral / Optimal)",
            )
        )
    elif payload.ph <= 8.4:
        interpretations.append(
            NutrientInterpretation(
                parameter="Soil pH",
                value=payload.ph,
                unit="pH",
                status="Mildly Alkaline",
                interpretation_en="Slightly alkaline; monitor Zinc and Iron availability, especially in calcareous black soils.",
                interpretation_kn="ಸ್ವಲ್ಪ ಕ್ಷಾರೀಯವಾಗಿದೆ; ಕಪ್ಪು ಮಣ್ಣಿನಲ್ಲಿ ಸತು ಮತ್ತು ಕಬ್ಬಿಣದ ಲಭ್ಯತೆಯನ್ನು ಗಮನಿಸಿ.",
                reference_range="6.0 - 7.5 (Neutral / Optimal)",
            )
        )
        guidance_en.append("Apply well-decomposed farmyard manure or green manure to buffer mild alkalinity and support micronutrient uptake.")
        guidance_kn.append("ಸ್ವಲ್ಪ ಕ್ಷಾರೀಯ ಮಣ್ಣನ್ನು ಸಮತೋಲನಗೊಳಿಸಲು ಕಳಿತ ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರ ಅಥವಾ ಹಸಿರೆಲೆ ಗೊಬ್ಬರ ಬಳಸಿ.")
    else:
        interpretations.append(
            NutrientInterpretation(
                parameter="Soil pH",
                value=payload.ph,
                unit="pH",
                status="Strongly Alkaline / Sodic Risk",
                interpretation_en="High pH (>8.4) restricts micronutrient solubility and impairs soil structure.",
                interpretation_kn="ಅಧಿಕ ಕ್ಷಾರೀಯತೆ (>8.4) ಸೂಕ್ಷ್ಮ ಪೋಷಕಾಂಶಗಳ ಲಭ್ಯತೆ ಮತ್ತು ಮಣ್ಣಿನ ರಚನೆಗೆ ಅಡ್ಡಿಯಾಗುತ್ತದೆ.",
                reference_range="6.0 - 7.5 (Neutral / Optimal)",
            )
        )
        guidance_en.append("High alkalinity (>8.4) requires EC/ESP lab diagnosis before gypsum and drainage reclamation.")
        guidance_kn.append("ಅಧಿಕ ಕ್ಷಾರೀಯ ಮಣ್ಣಿಗೆ (pH > 8.4) ಜಿಪ್ಸಂ ಮತ್ತು ಬಸಿದುಹೋಗುವ ಸುಧಾರಣೆಗೆ ಮುನ್ನ ಇ.ಸಿ/ಇ.ಎಸ್.ಪಿ ಪರೀಕ್ಷೆ ಅಗತ್ಯ.")

    # Nitrogen interpretation (Input scale 0-500 kg/ha; SHC available N standard <280 low, 280-560 med, >560 high;
    # note: many user inputs come from 0-140 ML/index scale, so explain clearly)
    if payload.nitrogen is None:
        interpretations.append(
            NutrientInterpretation(
                parameter="Nitrogen (N)",
                value=None,
                unit="kg/ha",
                status="Not Provided",
                interpretation_en="Available Nitrogen value missing; cannot assess vegetative nutrient status.",
                interpretation_kn="ಸಾರಜನಕದ ಮೌಲ್ಯ ನೀಡಿಲ್ಲ; ಲಭ್ಯತೆಯನ್ನು ಮೌಲ್ಯಮಾಪನ ಮಾಡಲು ಸಾಧ್ಯವಿಲ್ಲ.",
                reference_range="SHC Standard: <280 Low | 280-560 Medium | >560 High kg/ha",
            )
        )
    else:
        n_status = "Low" if payload.nitrogen < 60 else ("Moderate / Medium" if payload.nitrogen <= 140 else "High / Adequate")
        interpretations.append(
            NutrientInterpretation(
                parameter="Nitrogen (N)",
                value=payload.nitrogen,
                unit="kg/ha (or soil index)",
                status=n_status,
                interpretation_en="Evaluated against standard crop demand index; note that Indian Soil Health Cards measure Alkaline KMnO4-N (<280 Low, 280-560 Medium kg/ha).",
                interpretation_kn="ಬೆಳೆ ಬೇಡಿಕೆ ಸೂಚ್ಯಂಕಕ್ಕೆ ಹೋಲಿಸಲಾಗಿದೆ; ಮಣ್ಣು ಆರೋಗ್ಯ ಚೀಟಿಯಲ್ಲಿ <280 ಕಡಿಮೆ ಮತ್ತು 280-560 ಮಧ್ಯಮ ಎಂದು ಪರಿಗಣಿಸಲಾಗುತ್ತದೆ.",
                reference_range="Dataset index: 0-140 | SHC Alkaline KMnO4-N: 280-560 kg/ha Medium",
            )
        )

    # Phosphorus interpretation
    if payload.phosphorus is None:
        interpretations.append(
            NutrientInterpretation(
                parameter="Phosphorus (P)",
                value=None,
                unit="kg/ha",
                status="Not Provided",
                interpretation_en="Available Phosphorus value missing; cannot evaluate root/flowering P status.",
                interpretation_kn="ರಂಜಕದ ಮೌಲ್ಯ ನೀಡಿಲ್ಲ; ಬೇರು ಮತ್ತು ಹೂ ಬಿಡುವ ಪೋಷಕಾಂಶ ಸ್ಥಿತಿ ಅಜ್ಞಾತವಾಗಿದೆ.",
                reference_range="SHC Olsen-P: <10 Low | 10-25 Medium | >25 High kg/ha (P2O5 ~23-57)",
            )
        )
    else:
        p_status = "Low" if payload.phosphorus < 25 else ("Medium" if payload.phosphorus <= 60 else "High")
        interpretations.append(
            NutrientInterpretation(
                parameter="Phosphorus (P)",
                value=payload.phosphorus,
                unit="kg/ha",
                status=p_status,
                interpretation_en="Phosphorus supports root establishment and flowering; availability depends heavily on soil pH and organic matter.",
                interpretation_kn="ರಂಜಕವು ಬೇರು ಬೆಳವಣಿಗೆ ಮತ್ತು ಹೂ ಬಿಡಲು ನೆರವಾಗುತ್ತದೆ; ಇದರ ಲಭ್ಯತೆ ಮಣ್ಣಿನ ಪಿಎಚ್ ಮೇಲೆ ಅವಲಂಬಿತವಾಗಿದೆ.",
                reference_range="SHC Olsen-P: 10-25 kg/ha Medium (P2O5 eq. 23-57 kg/ha)",
            )
        )

    # Potassium interpretation
    if payload.potassium is None:
        interpretations.append(
            NutrientInterpretation(
                parameter="Potassium (K)",
                value=None,
                unit="kg/ha",
                status="Not Provided",
                interpretation_en="Available Potassium value missing.",
                interpretation_kn="ಪೊಟ್ಯಾಶ್ ಮೌಲ್ಯ ನೀಡಿಲ್ಲ.",
                reference_range="SHC NH4OAc-K: <110 Low | 110-280 Medium | >280 High kg/ha",
            )
        )
    else:
        k_status = "Low" if payload.potassium < 30 else ("Medium" if payload.potassium <= 110 else "High")
        interpretations.append(
            NutrientInterpretation(
                parameter="Potassium (K)",
                value=payload.potassium,
                unit="kg/ha",
                status=k_status,
                interpretation_en="Potassium regulates water balance, stalk strength, and drought/disease resilience.",
                interpretation_kn="ಪೊಟ್ಯಾಶ್ ಸಸ್ಯದ ನೀರಿನ ಸಮತೋಲನ, ಕಾಂಡದ ಬಲ ಮತ್ತು ರೋಗ ನಿರೋಧಕತೆಯನ್ನು ನಿಯಂತ್ರಿಸುತ್ತದೆ.",
                reference_range="SHC NH4OAc-K: 110-280 kg/ha Medium",
            )
        )

    # General soil-type guidance
    soil_notes = {
        "Red": (
            "Red soils in Karnataka are generally well-drained but often low in organic carbon and water-holding capacity; incorporate FYM/compost and tank silt.",
            "ಕರ್ನಾಟಕದ ಕೆಂಪು ಮಣ್ಣು ನೀರು ಬಸಿದುಹೋಗಲು ಉತ್ತಮವಾಗಿದ್ದರೂ ಸಾವಯವ ಇಂಗಾಲ ಕಡಿಮೆ ಇರುತ್ತದೆ; ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರ/ಕಾಂಪೋಸ್ಟ್ ಸೇರಿಸಿ.",
        ),
        "Black": (
            "Black cotton soils hold moisture well but swell when wet and crack when dry; avoid waterlogging and adopt broad-bed furrows.",
            "ಕಪ್ಪು ಮಣ್ಣು ತೇವಾಂಶ ಹಿಡಿದಿಟ್ಟುಕೊಳ್ಳುತ್ತದೆ; ಆದರೆ ನೀರು ನಿಲ್ಲದಂತೆ ಬಸಿಗಾಲುವೆ ಅಥವಾ ಅಡ್ಡ ಬದು ಪದ್ಧತಿ ಅನುಸರಿಸಿ.",
        ),
        "Laterite": (
            "Laterite soils in Malnad/Coastal zones are frequently acidic and leached; verify soil pH and organic matter before fertilizer application.",
            "ಮಲೆನಾಡು/ಕರಾವಳಿಯ ಲ್ಯಾಟರೈಟ್ ಮಣ್ಣು ಆಮ್ಲೀಯವಾಗಿರುತ್ತದೆ; ಗೊಬ್ಬರ ಬಳಸುವ ಮುನ್ನ ಮಣ್ಣಿನ ಪಿಎಚ್ ಪರೀಕ್ಷಿಸಿ.",
        ),
        "Alluvial": (
            "Alluvial river-basin soils are fertile and suit diverse crops when salinity and drainage are monitored.",
            "ನದಿ ದಡದ ಮೆಕ್ಕಲು ಮಣ್ಣು ಫಲವತ್ತಾಗಿದ್ದು ನೀರು ಬಸಿಯುವಿಕೆ ಮತ್ತು ಲವಣಾಂಶವನ್ನು ಗಮನಿಸಿದರೆ ವಿವಿಧ ಬೆಳೆಗಳಿಗೆ ಸೂಕ್ತ.",
        ),
        "Sandy": (
            "Sandy soils drain fast and leach mobile nutrients quickly; split fertilizer applications and add organic mulch.",
            "ಮರಳು ಮಣ್ಣಿನಲ್ಲಿ ನೀರು ಮತ್ತು ಪೋಷಕಾಂಶಗಳು ಬೇಗ ಬಸಿದುಹೋಗುತ್ತವೆ; ಸಾವಯವ ಗೊಬ್ಬರ ಮತ್ತು ಕಂತುಗಳಲ್ಲಿ ಗೊಬ್ಬರ ನೀಡುವುದು ಉತ್ತಮ.",
        ),
        "Loamy": (
            "Loamy soil provides balanced aeration, drainage, and nutrient retention across most field and horticultural crops.",
            "ಗೋಡು ಮಣ್ಣು ಗಾಳಿಯಾಡಲು, ತೇವಾಂಶ ಮತ್ತು ಪೋಷಕಾಂಶ ಹಿಡಿದಿಟ್ಟುಕೊಳ್ಳಲು ಸಮತೋಲಿತವಾಗಿದೆ.",
        ),
        "Clay": (
            "Clay soils retain water tightly and compact easily; avoid tillage when overly wet and add organic matter to improve structure.",
            "ಜೇಡಿ ಮಣ್ಣು ನೀರನ್ನು ಹೆಚ್ಚು ಹಿಡಿದಿಟ್ಟುಕೊಳ್ಳುತ್ತದೆ; ತೇವಾಂಶ ಹೆಚ್ಚಿದ್ದಾಗ ಉಳುಮೆ ಮಾಡಬೇಡಿ ಮತ್ತು ಸಾವಯವ ಗೊಬ್ಬರ ಸೇರಿಸಿ.",
        ),
    }
    s_en, s_kn = soil_notes.get(payload.soil_type, ("Maintain organic carbon through compost and crop residues.", "ಕಾಂಪೋಸ್ಟ್ ಮೂಲಕ ಸಾವಯವ ಇಂಗಾಲ ಕಾಪಾಡಿ."))
    guidance_en.append(s_en)
    guidance_kn.append(s_kn)

    if payload.measurement_source != "soil_test":
        guidance_en.append(
            "Values entered are estimates or unverified; collect a representative zig-zag soil sample (15 cm depth) for your nearest Soil Testing Lab."
        )
        guidance_kn.append(
            "ನಮೂದಿಸಿದ ಮೌಲ್ಯಗಳು ಅಂದಾಜು ಮಾತ್ರ; 15 ಸೆಂ.ಮೀ ಆಳದಿಂದ ಮಣ್ಣಿನ ಮಾದರಿ ಸಂಗ್ರಹಿಸಿ ಹತ್ತಿರದ ಮಣ್ಣು ಪರೀಕ್ಷಾ ಕೇಂದ್ರದಲ್ಲಿ ಪರೀಕ್ಷಿಸಿ."
        )

    overview_en = f"{payload.soil_type} soil profile reviewed using {payload.measurement_source.replace('_', ' ')} inputs."
    overview_kn = f"{payload.soil_type} ಮಣ್ಣಿನ ವಿವರಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗಿದೆ."

    return SoilAnalysisResponse(
        soil_type=payload.soil_type,
        measurement_source=payload.measurement_source,
        overview_en=overview_en,
        overview_kn=overview_kn,
        interpretations=interpretations,
        guidance_en=guidance_en,
        guidance_kn=guidance_kn,
        fertilizer_caution_en=(
            "SmartKrishi does not prescribe chemical fertilizer dosages without a verified laboratory Soil Health Card "
            "(matching the local lab's extraction method) and target crop recommendation from your Raitha Samparka Kendra."
        ),
        fertilizer_caution_kn=(
            "ಅಧಿಕೃತ ಪ್ರಯೋಗಾಲಯದ ಮಣ್ಣು ಆರೋಗ್ಯ ಚೀಟಿ ಮತ್ತು ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರದ ಬೆಳೆ ಶಿಫಾರಸು ಇಲ್ಲದೆ SmartKrishi "
            "ರಾಸಾಯನಿಕ ಗೊಬ್ಬರದ ಪ್ರಮಾಣವನ್ನು ಸೂಚಿಸುವುದಿಲ್ಲ."
        ),
    )
