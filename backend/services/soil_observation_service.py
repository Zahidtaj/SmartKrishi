"""Physical soil observation interpretation service (no NPK/pH inference from color)."""

from typing import Any


COLOR_NOTES: dict[str, dict[str, str]] = {
    "red": {
        "label_en": "Red soil appearance",
        "label_kn": "ಕೆಂಪು ಮಣ್ಣು",
        "note_en": "Red colour typically reflects iron-oxide presence common across Southern and Central Karnataka uplands; colour alone cannot indicate fertility or pH.",
        "note_kn": "ಕೆಂಪು ಬಣ್ಣವು ಕಬ್ಬಿಣಾಂಶದ ಆಕ್ಸೈಡ್‌ಗಳನ್ನು ಸೂಚಿಸಬಹುದು; ಆದರೆ ಬಣ್ಣದಿಂದಲೇ ಫಲವತ್ತತೆ ಅಥವಾ ರಸಸಾರ (pH) ನಿರ್ಧರಿಸಲು ಸಾಧ್ಯವಿಲ್ಲ.",
    },
    "reddish_brown": {
        "label_en": "Reddish-brown soil appearance",
        "label_kn": "ಕೆಂಪು-ಕಂದು ಮಣ್ಣು",
        "note_en": "Common in transition-zone loams and lateritic pockets; nutrient and pH levels vary widely with organic matter and management.",
        "note_kn": "ಸಂಕ್ರಮಣ ವಲಯದ ಗೋಡು ಮತ್ತು ಜಂಬಿಟ್ಟಿಗೆ ಮಣ್ಣಿನಲ್ಲಿ ಕಂಡುಬರುತ್ತದೆ; ಪೋಷಕಾಂಶಗಳು ನಿರ್ವಹಣೆಯ ಮೇಲೆ ಅವಲಂಬಿತವಾಗಿರುತ್ತವೆ.",
    },
    "dark_black": {
        "label_en": "Dark / Black soil appearance",
        "label_kn": "ಕಪ್ಪು ಮಣ್ಣು",
        "note_en": "Dark colour is common in Vertisols / black cotton belts of North Karnataka; it does not automatically prove high fertility without structural drainage and lab confirmation.",
        "note_kn": "ಉತ್ತರ ಕರ್ನಾಟಕದ ಎರೆ ಮಣ್ಣಿನಲ್ಲಿ ಕಂಡುಬರುತ್ತದೆ; ಕಪ್ಪು ಬಣ್ಣವಿದ್ದ ಮಾತ್ರಕ್ಕೆ ಹೆಚ್ಚಿನ ಫಲವತ್ತತೆ ಖಚಿತವಾಗುವುದಿಲ್ಲ.",
    },
    "brown": {
        "label_en": "Brown soil appearance",
        "label_kn": "ಕಂದು ಮಣ್ಣು",
        "note_en": "Brown surface appearance occurs across alluvial, medium black, and cultivated garden soils; texture and drainage govern water handling more strongly than colour.",
        "note_kn": "ಮೆಕ್ಕಲು ಮತ್ತು ಮಧ್ಯಮ ಕಪ್ಪು ಮಣ್ಣಿನಲ್ಲಿ ಕಂಡುಬರುತ್ತದೆ; ಬಣ್ಣಕ್ಕಿಂತ ಮಣ್ಣಿನ ವಿನ್ಯಾಸ ಮತ್ತು ನೀರು ಬಸಿಯುವಿಕೆ ಮುಖ್ಯ.",
    },
    "yellowish": {
        "label_en": "Yellowish soil appearance",
        "label_kn": "ಹಳದಿ ಮಿಶ್ರಿತ ಮಣ್ಣು",
        "note_en": "Yellowish tones can appear in leached upland soils or sub-surface lateritic layers; physical moisture holding and rooting depth should be checked carefully.",
        "note_kn": "ತೊಳೆದುಹೋದ ಎತ್ತರದ ಪ್ರದೇಶಗಳಲ್ಲಿ ಕಂಡುಬರಬಹುದು; ತೇವಾಂಶ ಹಿಡಿದಿಡುವಿಕೆ ಮತ್ತು ಆಳವನ್ನು ಗಮನಿಸುವುದು ಮುಖ್ಯ.",
    },
    "grey": {
        "label_en": "Grey soil appearance",
        "label_kn": "ಬೂದು ಬಣ್ಣದ ಮಣ್ಣು",
        "note_en": "Greyish soil often occurs in low-lying valleys or seasonally wet soils where drainage slows down; watch closely for ponding during heavy rains.",
        "note_kn": "ತಗ್ಗು ಪ್ರದೇಶ ಅಥವಾ ತೇವಾಂಶ ಹೆಚ್ಚಿರುವ ಮಣ್ಣಿನಲ್ಲಿ ಬೂದು ಬಣ್ಣ ಕಾಣಬಹುದು; ಭಾರಿ ಮಳೆಯಲ್ಲಿ ನೀರು ನಿಲ್ಲದಂತೆ ಗಮನಿಸಿ.",
    },
    "sandy_pale": {
        "label_en": "Sandy / pale soil appearance",
        "label_kn": "ಮರಳು / ತೆಳು ಬಣ್ಣದ ಮಣ್ಣು",
        "note_en": "Pale sandy soils typically drain rapidly and lose surface moisture faster during dry spells; organic mulching helps stabilize moisture.",
        "note_kn": "ತೆಳು ಮರಳು ಮಣ್ಣು ನೀರನ್ನು ಬೇಗ ಬಸಿಯುತ್ತದೆ ಮತ್ತು ಒಣ ದಿನಗಳಲ್ಲಿ ಬೇಗ ಒಣಗುತ್ತದೆ; ಸಾವಯವ ಹೊದಿಕೆ ಸಹಕಾರಿ.",
    },
    "mixed_uncertain": {
        "label_en": "Mixed or uncertain colour",
        "label_kn": "ಮಿಶ್ರ ಅಥವಾ ಖಚಿತವಿಲ್ಲದ ಬಣ್ಣ",
        "note_en": "Soil colour was not specified or varies across the plot. Recommendations rely on texture, drainage, water source, and agro-climatic zone.",
        "note_kn": "ಮಣ್ಣಿನ ಬಣ್ಣ ಖಚಿತವಾಗಿಲ್ಲದ ಕಾರಣ ಶಿಫಾರಸುಗಳು ಮಣ್ಣಿನ ವಿನ್ಯಾಸ, ನೀರು ಬಸಿಯುವಿಕೆ, ನೀರಾವರಿ ಮತ್ತು ಕೃಷಿ-ಹವಾಮಾನ ವಲಯವನ್ನು ಆಧರಿಸಿವೆ.",
    },
}

TEXTURE_BEHAVIOR: dict[str, dict[str, str]] = {
    "sandy": {
        "drainage_class": "rapid",
        "retention_class": "low",
        "summary_en": "Sandy feel (gritty & loose): aerates easily, allows root/peg penetration, but loses water quickly.",
        "summary_kn": "ಮರಳು ಮಿಶ್ರಿತ ವಿನ್ಯಾಸ: ಗಾಳಿಯಾಡಲು ಮತ್ತು ಬೇರು ಇಳಿಯಲು ಉತ್ತಮ; ಆದರೆ ತೇವಾಂಶ ಬೇಗ ಆವಿಯಾಗುತ್ತದೆ.",
    },
    "clayey": {
        "drainage_class": "slow",
        "retention_class": "high",
        "summary_en": "Clayey feel (sticky, forms ribbon): holds moisture longer for Rabi crops, but risks compaction and waterlogging under heavy rain.",
        "summary_kn": "ಜೇಡಿ ಮಣ್ಣಿನ ವಿನ್ಯಾಸ: ಹಿಂಗಾರು ಬೆಳೆಗೆ ತೇವಾಂಶ ಹಿಡಿದಿಡುತ್ತದೆ; ಆದರೆ ಅಧಿಕ ಮಳೆಯಲ್ಲಿ ನೀರು ನಿಲ್ಲುವ ಅಪಾಯವಿದೆ.",
    },
    "loamy": {
        "drainage_class": "balanced",
        "retention_class": "moderate",
        "summary_en": "Loamy feel (crumbly & balanced): offers a practical balance of drainage, aeration, and plant-available moisture.",
        "summary_kn": "ಗೋಡು ಮಣ್ಣಿನ ವಿನ್ಯಾಸ: ನೀರು ಬಸಿಯುವಿಕೆ ಮತ್ತು ತೇವಾಂಶ ಹಿಡಿದಿಡುವಿಕೆಯ ಸಮತೋಲನ ಹೊಂದಿದೆ.",
    },
    "silty": {
        "drainage_class": "moderate",
        "retention_class": "moderate_high",
        "summary_en": "Silty feel (smooth & soft): retains water moderately well; surface crusting can occur after intense showers.",
        "summary_kn": "ಮೆಕ್ಕಲು/ಮೃದು ವಿನ್ಯಾಸ: ಉತ್ತಮ ತೇವಾಂಶ ಹಿಡಿದಿಡುತ್ತದೆ; ಜೋರು ಮಳೆಯ ನಂತರ ಮೇಲ್ಮೈ ಗಟ್ಟಿಯಾಗದಂತೆ ಎಚ್ಚರವಹಿಸಿ.",
    },
    "mixed": {
        "drainage_class": "variable",
        "retention_class": "moderate",
        "summary_en": "Mixed field texture across plots: field checks across higher and lower patches help decide drainage needs.",
        "summary_kn": "ಮಿಶ್ರ ವಿನ್ಯಾಸ: ಜಮೀನಿನ ಎತ್ತರ ಮತ್ತು ತಗ್ಗು ಭಾಗಗಳಿಗೆ ಅನುಗುಣವಾಗಿ ನೀರು ನಿರ್ವಹಣೆ ಅಗತ್ಯ.",
    },
    "not_sure": {
        "drainage_class": "unknown",
        "retention_class": "unknown",
        "summary_en": "Soil texture marked uncertain: physical moisture/drainage suitability cannot be narrowed precisely.",
        "summary_kn": "ಮಣ್ಣಿನ ವಿನ್ಯಾಸ ತಿಳಿದಿಲ್ಲದ ಕಾರಣ ಭೌತಿಕ ತೇವಾಂಶ/ಬಸಿಯುವಿಕೆ ನಿಖರತೆ ಸೀಮಿತವಾಗಿದೆ.",
    },
}


def interpret_soil_observations(
    *,
    soil_color: str = "mixed_uncertain",
    soil_texture: str = "not_sure",
    drainage_after_rain: str = "not_sure",
    moisture_retention: str = "not_sure",
    soil_depth: str = "unknown",
    visible_stones: str = "not_sure",
    waterlogging_issue: str = "not_sure",
    erosion_issue: str = "not_sure",
    land_topography: str | None = None,
) -> dict[str, Any]:
    """Synthesize physical soil & land observations cleanly without inventing NPK/pH values."""
    color_info = COLOR_NOTES.get(soil_color, COLOR_NOTES["mixed_uncertain"])
    texture_info = TEXTURE_BEHAVIOR.get(soil_texture, TEXTURE_BEHAVIOR["not_sure"])

    unknown_fields: list[str] = []
    if soil_color == "mixed_uncertain":
        unknown_fields.append("soil_color")
    if soil_texture == "not_sure":
        unknown_fields.append("soil_texture")
    if drainage_after_rain == "not_sure":
        unknown_fields.append("drainage_after_rain")
    if moisture_retention == "not_sure":
        unknown_fields.append("moisture_retention")
    if soil_depth == "unknown":
        unknown_fields.append("soil_depth")
    if visible_stones == "not_sure":
        unknown_fields.append("visible_stones")
    if waterlogging_issue == "not_sure":
        unknown_fields.append("waterlogging_issue")

    # Determine synthesized drainage status (rain observation + waterlogging overrides texture guess)
    if waterlogging_issue == "frequent" or drainage_after_rain == "remains_days":
        effective_drainage = "waterlogging_prone"
    elif drainage_after_rain == "remains_hours" or waterlogging_issue == "occasional":
        effective_drainage = "slow_draining"
    elif drainage_after_rain == "very_quickly":
        effective_drainage = "rapid_draining"
    elif drainage_after_rain == "moderately":
        effective_drainage = "well_drained"
    elif texture_info["drainage_class"] == "rapid":
        effective_drainage = "likely_rapid"
    elif texture_info["drainage_class"] == "slow":
        effective_drainage = "likely_slow"
    elif texture_info["drainage_class"] in ("balanced", "moderate"):
        effective_drainage = "likely_balanced"
    else:
        effective_drainage = "unknown"

    # Moisture holding synthesis
    if moisture_retention == "dries_quickly":
        effective_moisture = "low_retention"
    elif moisture_retention == "short_period":
        effective_moisture = "moderate_retention"
    elif moisture_retention == "several_days":
        effective_moisture = "high_retention"
    elif texture_info["retention_class"] == "low":
        effective_moisture = "likely_low_retention"
    elif texture_info["retention_class"] in ("high", "moderate_high"):
        effective_moisture = "likely_high_retention"
    elif texture_info["retention_class"] == "moderate":
        effective_moisture = "likely_moderate_retention"
    else:
        effective_moisture = "unknown"

    # Confidence calculation based on physical observation completeness
    core_unknowns = sum(
        1
        for val in (soil_texture, drainage_after_rain, moisture_retention, soil_depth)
        if val in ("not_sure", "unknown")
    )
    if core_unknowns >= 3 or (soil_texture == "not_sure" and drainage_after_rain == "not_sure"):
        confidence = "low"
    elif core_unknowns >= 1 or soil_color == "mixed_uncertain":
        confidence = "moderate"
    else:
        confidence = "high"

    insights_en: list[str] = [
        f"{color_info['label_en']}: {color_info['note_en']}",
        texture_info["summary_en"],
    ]
    insights_kn: list[str] = [
        f"{color_info['label_kn']}: {color_info['note_kn']}",
        texture_info["summary_kn"],
    ]

    management_en: list[str] = []
    management_kn: list[str] = []

    if effective_drainage == "waterlogging_prone":
        management_en.append("Field shows waterlogging risk: provide surface drainage furrows or raised-bed sowing before growing upland crops.")
        management_kn.append("ಜಮೀನಿನಲ್ಲಿ ನೀರು ನಿಲ್ಲುವ ಸಾಧ್ಯತೆ ಇದೆ: ಬೆಳೆಗಳಿಗೆ ಏರು ಮಡಿ ಅಥವಾ ಬಸಿಕಾಲುವೆ ವ್ಯವಸ್ಥೆ ಮಾಡುವುದು ಸುರಕ್ಷಿತ.")
    elif effective_drainage == "rapid_draining" or effective_moisture == "low_retention":
        management_en.append("Fast-draining soil loses moisture rapidly: add farmyard manure/compost, practice mulching, or prefer drought-tolerant crops.")
        management_kn.append("ನೀರು ಬೇಗ ಬಸಿದುಹೋಗುವ ಮಣ್ಣಿನಲ್ಲಿ ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರ, ಹೊದಿಕೆ ಮತ್ತು ಬರ ಸಹಿಷ್ಣು ಬೆಳೆಗಳು ಉಪಯುಕ್ತ.")

    if soil_depth == "shallow" or visible_stones == "many_stony" or land_topography == "rocky_stony":
        management_en.append("Shallow or stony root zone limits deep taproot, tuber/root, and perennial plantation establishment.")
        management_kn.append("ಆಳ ಕಡಿಮೆ ಅಥವಾ ಕಲ್ಲು ಮಿಶ್ರಿತ ಮಣ್ಣು ಆಳವಾದ ಬೇರು ಮತ್ತು ತೋಟಗಾರಿಕಾ ಬೆಳೆಗಳಿಗೆ ಮಿತಿಯಾಗಬಹುದು.")

    if erosion_issue in ("mild", "severe") or land_topography == "steep_hilly":
        management_en.append("Slope/erosion observed: contour bunding, vegetative barriers, and minimal tillage help protect topsoil.")
        management_kn.append("ಇಳಿಜಾರು/ಮಣ್ಣು ಸವಕಳಿ ಕಂಡುಬಂದಿದೆ: ಕಾಂಟೂರ್ ಬದುಗಳು ಮತ್ತು ಕನಿಷ್ಠ ಉಳುಮೆ ಮೇಲ್ಮಣ್ಣನ್ನು ರಕ್ಷಿಸುತ್ತವೆ.")

    if not management_en:
        management_en.append("Physical observations show no severe structural obstruction; confirm seasonal moisture timing before sowing.")
        management_kn.append("ಭೌತಿಕ ವೀಕ್ಷಣೆಯಲ್ಲಿ ಗಂಭೀರ ಮಣ್ಣಿನ ಅಡಚಣೆ ಕಂಡುಬಂದಿಲ್ಲ; ಬಿತ್ತನೆಗೆ ಮುನ್ನ ಹಂಗಾಮಿ ತೇವಾಂಶ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.")

    return {
        "soil_color": soil_color,
        "soil_color_label_en": color_info["label_en"],
        "soil_color_label_kn": color_info["label_kn"],
        "color_disclaimer_en": "Visual soil colour is only a surface field cue; it cannot measure pH, Nitrogen, Phosphorus, Potassium, or organic carbon.",
        "color_disclaimer_kn": "ಮಣ್ಣಿನ ಬಣ್ಣವು ಕೇವಲ ಪ್ರಾಥಮಿಕ ದೃಶ್ಯ ಸೂಚನೆಯಾಗಿದೆ; ಇದರಿಂದ pH ಅಥವಾ N-P-K ಪೋಷಕಾಂಶಗಳನ್ನು ಅಳೆಯಲು ಸಾಧ್ಯವಿಲ್ಲ.",
        "soil_texture": soil_texture,
        "effective_drainage": effective_drainage,
        "effective_moisture_retention": effective_moisture,
        "soil_depth": soil_depth,
        "visible_stones": visible_stones,
        "waterlogging_issue": waterlogging_issue,
        "erosion_issue": erosion_issue,
        "observation_confidence": confidence,
        "unknown_fields": unknown_fields,
        "insights_en": insights_en,
        "insights_kn": insights_kn,
        "management_guidance_en": management_en,
        "management_guidance_kn": management_kn,
        "optional_lab_note_en": "Soil testing is NOT required to use SmartKrishi. For fertilizer dosage decisions, farmers can optionally request a Soil Health Card at the nearest Raitha Samparka Kendra (RSK) or KVK.",
        "optional_lab_note_kn": "SmartKrishi ಬಳಸಲು ಮಣ್ಣು ಪರೀಕ್ಷೆ ಕಡ್ಡಾಯವಲ್ಲ. ರಸಗೊಬ್ಬರ ಪ್ರಮಾಣ ನಿಖರವಾಗಿ ತಿಳಿಯಲು ಬಯಸಿದಲ್ಲಿ ಹತ್ತಿರದ ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರ (RSK) ಅಥವಾ ಕೆವಿಕೆ ಮೂಲಕ ಮಣ್ಣು ಆರೋಗ್ಯ ಕಾರ್ಡ್ ಪಡೆಯಬಹುದು.",
    }
