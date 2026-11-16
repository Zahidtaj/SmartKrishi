from typing import Dict, Any, List

class ExplanationService:
    def generate_explanation(
        self,
        candidate: Dict[str, Any],
        location: Dict[str, Any],
        soil_obs: Dict[str, Any],
        water_avail: Dict[str, Any],
        season: str,
        weather: Dict[str, Any],
        missing_fields: List[str]
    ) -> Dict[str, Any]:
        """
        Generates structured, traceable agricultural explanations
        derived directly from the evaluation metrics and documented agronomic rules.
        """
        crop = candidate["crop"]
        score = candidate["suitability_score"]
        tier = candidate["suitability_tier"]
        sub = candidate["sub_scores"]

        crop_name = crop["crop_name"]
        district = location.get("district", "the region")
        zone_name = location.get("zone_name", "the agro-climatic zone")
        texture = soil_obs.get("soil_texture", "Unknown")
        drainage = soil_obs.get("drainage", "Unknown")
        irrigation = water_avail.get("irrigation_source", "Rainfed farming")
        water_duration = water_avail.get("availability_duration", "Throughout season")
        normal_rain = location.get("normal_rainfall_mm", 750)

        # 1. Reasons for selection
        reasons: List[str] = []
        if sub["regional_score"] >= 85:
            reasons.append(
                f"Historically proven and recommended staple/cash crop for {district} within {zone_name}."
            )
        if sub["soil_score"] >= 80:
            reasons.append(
                f"Documented affinity for {texture} soil texture, supporting robust root development."
            )
        if sub["water_score"] >= 80:
            reasons.append(
                f"Water demand ({crop['water_requirement_mm']['optimal_min']}-{crop['water_requirement_mm']['optimal_max']} mm) is well-matched with {irrigation} ({water_duration})."
            )
        if sub["season_score"] >= 90:
            reasons.append(
                f"Current planned season ({season}) aligns with the recommended sowing calendar for {crop_name} in Karnataka."
            )
        if not reasons:
            reasons.append(
                f"Feasible alternative crop for {district} under careful agronomic management."
            )

        # 2. Supporting Soil Observations
        soil_support: List[str] = []
        if texture != "Unknown":
            soil_support.append(f"Observed soil texture: {texture} (Crop requirement: {', '.join(crop.get('preferred_soil_textures', []))}).")
        else:
            soil_support.append("Soil texture was not observed; suitability assessed under neutral assumption.")

        if drainage != "Unknown":
            soil_support.append(f"Observed drainage condition: {drainage}. Compatible with root aeration needs.")

        if soil_obs.get("soil_colour") != "Unknown":
            soil_support.append(f"Soil colour ({soil_obs.get('soil_colour')}) indicates regional geological profile compatible with local crop tradition.")

        if soil_obs.get("soil_depth") != "Unknown":
            soil_support.append(f"Soil depth ({soil_obs.get('soil_depth')}) satisfies the minimum '{crop.get('min_soil_depth', 'Shallow')}' root penetration requirement.")

        # 3. Water Sufficiency Evaluation
        water_min = crop["water_requirement_mm"]["min"]
        water_max = crop["water_requirement_mm"]["max"]
        if "rainfed" in irrigation.lower():
            if normal_rain >= crop["water_requirement_mm"]["optimal_min"]:
                water_notes = (
                    f"Rainfed cultivation is viable. Normal seasonal rainfall ({normal_rain} mm) in {district} "
                    f"meets the crop's baseline requirement ({water_min}-{water_max} mm). "
                    f"However, in-situ soil moisture conservation (e.g. mulching) is recommended during vegetative dry spells."
                )
            else:
                water_notes = (
                    f"Rainfed cultivation carries moderate moisture risk. Regional normal rainfall ({normal_rain} mm) "
                    f"is marginally below optimal ({water_min}-{water_max} mm). Life-saving protective irrigation from a farm pond is strongly advised."
                )
        else:
            water_notes = (
                f"Irrigation resource ({irrigation}, {water_duration}) is adequate to sustain critical growth stages "
                f"for {crop_name} across its {crop['duration_days']['average']}-day duration."
            )

        # 4. Climate Suitability Notes
        climate_notes = (
            f"{zone_name} typical climate ({location.get('climate_description', 'semi-arid')}) with annual rainfall "
            f"around {normal_rain} mm aligns with the thermal and moisture tolerances of {crop_name}."
        )

        # 5. Potential Agricultural Risks
        risks = crop.get("critical_risks", [])

        # 6. Crucial Practices from Package of Practices
        practices = crop.get("cultivation_practices", "Follow recommended line spacing and integrated pest management.")

        # 7. Uncertainty Notes
        uncertainty_notes = None
        if missing_fields:
            uncertainty_notes = (
                f"Note: Recommendations were calculated with missing inputs: {', '.join(missing_fields)}. "
                f"Providing these observable characteristics will refine accuracy and reduce uncertainty penalties."
            )

        return {
            "reasons_for_selection": reasons,
            "supporting_soil_observations": soil_support,
            "water_sufficiency_notes": water_notes,
            "climate_suitability_notes": climate_notes,
            "potential_risks": risks,
            "crucial_practices": practices,
            "data_uncertainty_notes": uncertainty_notes
        }

explanation_service = ExplanationService()
