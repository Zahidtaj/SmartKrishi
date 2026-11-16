from typing import Dict, Any, List, Tuple
from backend.app.core.config import settings
from backend.app.services.rule_engine import rule_engine

class ScoringService:
    def __init__(self):
        self.weights = settings.SCORING_WEIGHTS
        self.penalties = settings.UNCERTAINTY_PENALTIES

    def evaluate_candidates(
        self,
        location: Dict[str, Any],
        soil_obs: Dict[str, Any],
        water_avail: Dict[str, Any],
        land_profile: Dict[str, Any],
        season: str,
        weather: Dict[str, Any],
        farming_history: Dict[str, Any] | None = None
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
        """
        Runs the 15-step recommendation process:
        Filters hard constraints, evaluates sub-scores, calculates weighted total,
        ranks candidates, and measures uncertainty.
        """
        all_crops = rule_engine.get_all_crops()
        recommended: List[Dict[str, Any]] = []
        filtered: List[Dict[str, Any]] = []

        # Calculate data completeness and reliability
        data_quality = self._assess_data_completeness(soil_obs, weather)

        for crop in all_crops:
            # 1. Hard Constraints Check
            is_excluded, reason, constraint_type = rule_engine.evaluate_hard_constraints(
                crop=crop,
                location=location,
                soil_obs=soil_obs,
                water_avail=water_avail,
                land_profile=land_profile,
                season=season,
                weather=weather
            )

            if is_excluded:
                filtered.append({
                    "crop_id": crop["id"],
                    "crop_name": crop["crop_name"],
                    "reason_for_exclusion": reason,
                    "constraint_type": constraint_type
                })
                continue

            # 2. Compatibility Sub-scores
            sub_scores = rule_engine.calculate_compatibility_scores(
                crop=crop,
                location=location,
                soil_obs=soil_obs,
                water_avail=water_avail,
                land_profile=land_profile,
                season=season,
                weather=weather,
                farming_history=farming_history
            )

            # 3. Weighted Overall Score
            weighted_total = (
                sub_scores["regional_score"] * self.weights["regional_suitability"] +
                sub_scores["soil_score"] * self.weights["soil_texture_compatibility"] +
                sub_scores["drainage_score"] * self.weights["drainage_compatibility"] +
                sub_scores["water_score"] * self.weights["water_availability_compatibility"] +
                sub_scores["climate_score"] * self.weights["rainfall_compatibility"] +
                sub_scores["temperature_score"] * self.weights["temperature_compatibility"] +
                sub_scores["season_score"] * self.weights["seasonal_compatibility"]
            )
            # Add rotation history adjustment (bounded)
            final_score = round(max(0.0, min(100.0, weighted_total + sub_scores.get("history_adjustment", 0.0))), 1)

            # Assign Suitability Tier
            if final_score >= 82.0:
                tier = "Highly Suitable"
            elif final_score >= 68.0:
                tier = "Moderately Suitable"
            elif final_score >= 52.0:
                tier = "Marginally Suitable"
            else:
                tier = "Low Suitability"

            recommended.append({
                "crop": crop,
                "suitability_score": final_score,
                "suitability_tier": tier,
                "sub_scores": sub_scores
            })

        # Rank candidates in descending order of suitability score
        recommended.sort(key=lambda x: x["suitability_score"], reverse=True)

        # Assign rank 1, 2, 3...
        for idx, item in enumerate(recommended):
            item["rank"] = idx + 1

        return recommended, filtered, data_quality

    def _assess_data_completeness(self, soil_obs: Dict[str, Any], weather: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates completeness percentage and explicit reliability deductions for missing observations."""
        missing_fields: List[str] = []
        reliability_deductions = 0

        if soil_obs.get("soil_texture") == "Unknown":
            missing_fields.append("Soil Texture")
            reliability_deductions += self.penalties["unknown_soil_texture"]

        if soil_obs.get("soil_colour") == "Unknown":
            missing_fields.append("Soil Colour")
            reliability_deductions += self.penalties["unknown_soil_colour"]

        if soil_obs.get("drainage") == "Unknown":
            missing_fields.append("Drainage Characteristics")
            reliability_deductions += self.penalties["unknown_drainage"]

        if soil_obs.get("moisture_retention") == "Unknown":
            missing_fields.append("Moisture Retention")
            reliability_deductions += self.penalties["unknown_moisture_retention"]

        if soil_obs.get("soil_depth") == "Unknown":
            missing_fields.append("Soil Depth")
            reliability_deductions += self.penalties["unknown_soil_depth"]

        if not weather.get("is_live_data", False):
            missing_fields.append("Real-time Weather Station Data (Using IMD Climatological Normals)")
            reliability_deductions += self.penalties["missing_weather_live"]

        total_checked_fields = 6
        filled_fields = total_checked_fields - len(missing_fields)
        completeness_pct = round((filled_fields / total_checked_fields) * 100.0, 1)
        reliability_pct = round(max(35.0, 100.0 - reliability_deductions), 1)

        return {
            "completeness_pct": completeness_pct,
            "reliability_score_pct": reliability_pct,
            "missing_fields": missing_fields
        }

scoring_service = ScoringService()
