import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
from backend.app.core.config import settings

class RuleEngine:
    def __init__(self):
        self._load_crops()

    def _load_crops(self):
        crops_file = settings.DATA_PATH / "crops_karnataka.json"
        self.crops_data: List[Dict[str, Any]] = []
        if crops_file.exists():
            with open(crops_file, "r", encoding="utf-8") as f:
                self.crops_data = json.load(f)

    def get_all_crops(self) -> List[Dict[str, Any]]:
        return self.crops_data

    def get_crop_by_id(self, crop_id: str) -> Dict[str, Any] | None:
        for c in self.crops_data:
            if c["id"] == crop_id:
                return c
        return None

    def evaluate_hard_constraints(
        self,
        crop: Dict[str, Any],
        location: Dict[str, Any],
        soil_obs: Dict[str, Any],
        water_avail: Dict[str, Any],
        land_profile: Dict[str, Any],
        season: str,
        weather: Dict[str, Any]
    ) -> Tuple[bool, str, str]:
        """
        Evaluates agricultural hard constraints.
        Returns: (is_excluded: bool, reason: str, constraint_type: str)
        """
        crop_id = crop["id"]
        drainage = soil_obs.get("drainage", "Unknown")
        waterlogging = soil_obs.get("waterlogging_observed", False)
        texture = soil_obs.get("soil_texture", "Unknown")
        depth = soil_obs.get("soil_depth", "Unknown")
        slope = land_profile.get("slope_type", "Flat land")
        irrigation = water_avail.get("irrigation_source", "Rainfed farming")
        water_duration = water_avail.get("availability_duration", "Throughout season")
        normal_rain = location.get("normal_rainfall_mm", 750)
        zone_id = location.get("zone_id", 5)

        # 1. WATERLOGGING / DRAINAGE HARD CONSTRAINT
        # Crops that cannot tolerate water stagnation (>24 hours) or severe waterlogging
        waterlog_sensitive = ["groundnut", "red_gram", "chickpea", "sesamum", "onion"]
        if drainage == "Water remains for one or more days" or (waterlogging and slope == "Low-lying land"):
            if crop_id in waterlog_sensitive:
                return (
                    True,
                    f"{crop['crop_name']} cannot tolerate prolonged standing water. Prolonged waterlogging causes root asphyxiation, collar rot, and total crop failure.",
                    "Lethal Drainage Constraint"
                )

        # Paddy in excessively fast-draining coarse sand without water pooling ability
        if crop_id == "paddy" and texture == "Sandy" and drainage == "Water drains quickly" and irrigation == "Rainfed farming":
            return (
                True,
                "Wetland paddy cannot be established in rapidly draining coarse sandy soil under rainfed conditions due to excessive percolation losses.",
                "Percolation Constraint"
            )

        # 2. WATER DEFICIT HARD CONSTRAINT FOR WATER-INTENSIVE CROPS
        # Sugarcane and Paddy require > 1100-1500 mm water. Rainfed in low-rainfall dry zones is impossible.
        if crop_id in ["sugarcane", "paddy"]:
            is_rainfed = "rainfed" in irrigation.lower()
            is_scarce = water_duration in ["Limited water availability", "Uncertain availability"]
            if is_rainfed or (is_scarce and normal_rain < 900):
                return (
                    True,
                    f"{crop['crop_name']} has high water requirements ({crop['water_requirement_mm']['min']}-{crop['water_requirement_mm']['max']} mm) and cannot be cultivated successfully under rainfed or water-deficit conditions in {location.get('district', 'this area')}.",
                    "Critical Water Deficit Constraint"
                )

        # 3. SOIL DEPTH CONSTRAINT FOR DEEP TAPROOT CROPS
        # Sugarcane, Cotton, and long-duration Red Gram need medium to deep profile (>50-75 cm)
        if depth == "Shallow" and crop_id in ["sugarcane", "cotton"]:
            return (
                True,
                f"{crop['crop_name']} develops a deep root system (>1.5 m) and cannot produce economic yields in shallow soil (<25 cm) with an underlying hard pan or rock layer.",
                "Root Depth Restriction"
            )

        # 4. HEAVY CRACKING CLAY CONSTRAINT FOR GROUNDNUT
        # Heavy clay severely impedes peg penetration and causes pod breaking at harvest
        if crop_id == "groundnut" and texture == "Clayey" and soil_obs.get("soil_colour") == "Dark black":
            return (
                True,
                "Groundnut is agronomically unsuitable for heavy, cracking black clay soils. Gynophores (pegs) cannot penetrate compact clay, and pods detach and rot inside the soil during harvest.",
                "Soil Texture Incompatibility"
            )

        # 5. SEASON INCOMPATIBILITY
        suitable_seasons = [s.lower() for s in crop.get("suitable_seasons", [])]
        season_lower = season.lower()
        if season_lower not in suitable_seasons and "any" not in suitable_seasons:
            # Check if season is completely off (e.g. Rabi Chickpea in Summer)
            if crop_id == "chickpea" and season_lower in ["summer"]:
                return (
                    True,
                    "Chickpea is strictly a cool-season Rabi crop. High temperatures during Summer (>32°C) trigger complete flower abortion and scorching.",
                    "Lethal Thermal / Season Mismatch"
                )

        # 6. TOPOGRAPHY / SLOPE CONSTRAINT
        if slope in ["Steep or hilly land", "Rocky land"] and crop_id in ["paddy", "sugarcane"]:
            return (
                True,
                f"Field slopes or rocky terrain prevent uniform water impounding and mechanical cultivation required for {crop['crop_name']}.",
                "Topography Incompatibility"
            )

        return (False, "", "")

    def calculate_compatibility_scores(
        self,
        crop: Dict[str, Any],
        location: Dict[str, Any],
        soil_obs: Dict[str, Any],
        water_avail: Dict[str, Any],
        land_profile: Dict[str, Any],
        season: str,
        weather: Dict[str, Any],
        farming_history: Dict[str, Any] | None = None
    ) -> Dict[str, float]:
        """
        Calculates separate sub-scores (0-100) across 7 agricultural dimensions.
        """
        zone_id = location.get("zone_id", 5)
        district = location.get("district", "")
        normal_rain = location.get("normal_rainfall_mm", 750)
        current_temp = weather.get("current_temperature_c", 28.0)

        # 1. Regional Suitability Score (0 - 100)
        suitable_zones = crop.get("suitable_zones", [])
        suitable_districts = [d.lower() for d in crop.get("suitable_districts", [])]
        
        if zone_id in suitable_zones and district.lower() in suitable_districts:
            regional_score = 100.0
        elif zone_id in suitable_zones:
            regional_score = 90.0
        elif district.lower() in suitable_districts:
            regional_score = 85.0
        else:
            # Secondary zone proximity check
            regional_score = 50.0

        # 2. Soil Texture Compatibility Score (0 - 100)
        texture = soil_obs.get("soil_texture", "Unknown")
        pref_textures = crop.get("preferred_soil_textures", [])
        acc_textures = crop.get("acceptable_soil_textures", [])
        uns_textures = crop.get("unsuitable_soil_textures", [])

        if texture in pref_textures:
            texture_score = 100.0
        elif texture in acc_textures:
            texture_score = 75.0
        elif texture == "Unknown" or texture == "Mixed":
            texture_score = 65.0
        elif texture in uns_textures:
            texture_score = 25.0
        else:
            texture_score = 60.0

        # Soil colour supporting factor
        colour = soil_obs.get("soil_colour", "Unknown")
        pref_colors = crop.get("preferred_soil_colors", [])
        acc_colors = crop.get("acceptable_soil_colors", [])
        if colour in pref_colors:
            texture_score = min(100.0, texture_score + 5.0)
        elif colour in acc_colors:
            pass
        elif colour == "Unknown":
            pass
        else:
            texture_score = max(20.0, texture_score - 10.0)

        # 3. Drainage Compatibility Score (0 - 100)
        drainage = soil_obs.get("drainage", "Unknown")
        drain_pref = crop.get("drainage_requirements", {}).get("preferred", [])
        drain_tol = crop.get("drainage_requirements", {}).get("tolerated", [])
        drain_uns = crop.get("drainage_requirements", {}).get("unsuitable", [])

        if drainage in drain_pref:
            drainage_score = 100.0
        elif drainage in drain_tol:
            drainage_score = 75.0
        elif drainage == "Unknown":
            drainage_score = 65.0
        elif drainage in drain_uns:
            drainage_score = 20.0
        else:
            drainage_score = 60.0

        # Soil depth adjustment
        depth = soil_obs.get("soil_depth", "Unknown")
        min_depth = crop.get("min_soil_depth", "Shallow")
        if depth == "Deep":
            drainage_score = min(100.0, drainage_score + 5.0)
        elif depth == "Shallow" and min_depth in ["Medium", "Deep"]:
            drainage_score = max(30.0, drainage_score - 20.0)

        # 4. Water Availability Compatibility Score (0 - 100)
        irrigation = water_avail.get("irrigation_source", "Rainfed farming")
        water_duration = water_avail.get("availability_duration", "Throughout season")
        water_req = crop.get("water_requirement_mm", {"optimal_min": 450, "optimal_max": 650})
        opt_req = (water_req.get("optimal_min", 450) + water_req.get("optimal_max", 650)) / 2.0

        is_rainfed = "rainfed" in irrigation.lower()
        if not is_rainfed:
            # Irrigated farming: high score if water is available throughout season
            if water_duration == "Throughout season":
                water_score = 95.0
            elif water_duration == "Water available during certain months":
                water_score = 80.0 if crop.get("duration_days", {}).get("category") == "Short" else 65.0
            else:
                water_score = 60.0
        else:
            # Rainfed farming: compare crop requirement against regional normal rainfall
            if normal_rain >= opt_req:
                water_score = 90.0
            elif normal_rain >= water_req.get("min", 350):
                # Crop is viable with rainfall, water tolerance matters
                tol = crop.get("water_scarcity_tolerance", "Moderate")
                water_score = 85.0 if tol in ["High", "Very High", "Extreme"] else 65.0
            else:
                tol = crop.get("water_scarcity_tolerance", "Moderate")
                water_score = 70.0 if tol in ["High", "Extreme"] else 35.0

        # 5. Climate / Rainfall Compatibility Score (0 - 100)
        crop_rain_min = crop.get("rainfall_mm", {}).get("min", 400)
        crop_rain_opt_min = crop.get("rainfall_mm", {}).get("optimal_min", 500)
        crop_rain_opt_max = crop.get("rainfall_mm", {}).get("optimal_max", 900)
        crop_rain_max = crop.get("rainfall_mm", {}).get("max", 1200)

        if crop_rain_opt_min <= normal_rain <= crop_rain_opt_max:
            climate_score = 100.0
        elif crop_rain_min <= normal_rain <= crop_rain_max:
            climate_score = 80.0
        elif normal_rain < crop_rain_min:
            deficit_ratio = normal_rain / max(1.0, crop_rain_min)
            climate_score = max(30.0, 75.0 * deficit_ratio)
        else:
            climate_score = 65.0

        # 6. Temperature Compatibility Score (0 - 100)
        crop_t_min = crop.get("temperature_c", {}).get("optimal_min", 20)
        crop_t_max = crop.get("temperature_c", {}).get("optimal_max", 35)
        if crop_t_min <= current_temp <= crop_t_max:
            temp_score = 100.0
        elif (crop_t_min - 4.0) <= current_temp <= (crop_t_max + 4.0):
            temp_score = 80.0
        else:
            temp_score = 55.0

        # 7. Seasonal Compatibility Score (0 - 100)
        suitable_seasons = [s.lower() for s in crop.get("suitable_seasons", [])]
        season_lower = season.lower()
        if season_lower in suitable_seasons or "any" in suitable_seasons:
            season_score = 100.0
        else:
            season_score = 40.0

        # 8. Farming History Rotation Adjustment
        history_bonus = 0.0
        if farming_history:
            prev_crop = (farming_history.get("previous_crop") or "").lower()
            favored = [f.lower() for f in crop.get("rotation_predecessors_favored", [])]
            discouraged = [d.lower() for d in crop.get("rotation_predecessors_discouraged", [])]
            
            # Legume-cereal or beneficial rotation
            for f in favored:
                if f in prev_crop or prev_crop in f:
                    history_bonus += 8.0
                    break
                    
            # Mono-cropping penalty
            if prev_crop and (crop["crop_name"].lower() in prev_crop or prev_crop in crop["crop_name"].lower()):
                history_bonus -= 12.0

        return {
            "regional_score": regional_score,
            "soil_score": texture_score,
            "drainage_score": drainage_score,
            "water_score": water_score,
            "climate_score": climate_score,
            "temperature_score": temp_score,
            "season_score": season_score,
            "history_adjustment": history_bonus
        }

rule_engine = RuleEngine()
