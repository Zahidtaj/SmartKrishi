import datetime
from typing import List, Dict, Any
from backend.app.services.rule_engine import rule_engine

class ComparisonService:
    def compare_crops(self, crop_ids: List[str]) -> Dict[str, Any]:
        """
        Compares 2 to 3 selected crops side-by-side across agronomic requirements,
        soil texture, water needs, duration, risks, and verified economic indicators.
        """
        comparison_list: List[Dict[str, Any]] = []
        
        for cid in crop_ids:
            crop = rule_engine.get_crop_by_id(cid)
            if not crop:
                continue
                
            drain_pref = crop.get("drainage_requirements", {}).get("preferred", [])
            temp_range = f"{crop['temperature_c']['optimal_min']}°C - {crop['temperature_c']['optimal_max']}°C"
            rain_range = f"{crop['rainfall_mm']['optimal_min']} - {crop['rainfall_mm']['optimal_max']} mm"
            
            comparison_list.append({
                "crop_id": crop["id"],
                "crop_name": crop["crop_name"],
                "kannada_name": crop.get("kannada_name"),
                "scientific_name": crop.get("scientific_name"),
                "category": crop.get("category"),
                "suitable_zones": crop.get("suitable_zones", []),
                "preferred_soil_textures": crop.get("preferred_soil_textures", []),
                "drainage_preference": ", ".join(drain_pref) if drain_pref else "Well drained",
                "water_requirement_mm": crop.get("water_requirement_mm", {}),
                "water_scarcity_tolerance": crop.get("water_scarcity_tolerance", "Moderate"),
                "temperature_range_c": temp_range,
                "rainfall_range_mm": rain_range,
                "duration_days": crop.get("duration_days", {}),
                "suitable_seasons": crop.get("suitable_seasons", []),
                "key_risks": crop.get("critical_risks", []),
                "cultivation_practices": crop.get("cultivation_practices", ""),
                "economics": crop.get("economics")
            })

        names = [c["crop_name"] for c in comparison_list]
        summary = (
            f"Comparison of {', '.join(names)}. "
            f"Review the differing water requirements, soil texture affinities, and duration categories "
            f"to make a well-informed planting decision tailored to your land constraints."
        )

        return {
            "crops": comparison_list,
            "comparison_summary": summary,
            "comparison_timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }

comparison_service = ComparisonService()
