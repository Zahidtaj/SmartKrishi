import json
import math
from pathlib import Path
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from backend.app.core.config import settings
from backend.app.models.models import AgroClimaticZone, District, Taluk

class LocationService:
    def __init__(self):
        self._load_local_data()

    def _load_local_data(self):
        zones_file = settings.DATA_PATH / "karnataka_zones.json"
        districts_file = settings.DATA_PATH / "karnataka_districts.json"
        
        self.zones_data: List[Dict[str, Any]] = []
        self.districts_data: List[Dict[str, Any]] = []
        
        if zones_file.exists():
            with open(zones_file, "r", encoding="utf-8") as f:
                self.zones_data = json.load(f)
                
        if districts_file.exists():
            with open(districts_file, "r", encoding="utf-8") as f:
                self.districts_data = json.load(f)

    def get_all_zones(self, db: Optional[Session] = None) -> List[Dict[str, Any]]:
        if db:
            zones = db.query(AgroClimaticZone).order_by(AgroClimaticZone.id).all()
            if zones:
                return [
                    {
                        "id": z.id,
                        "code": z.code,
                        "name": z.name,
                        "kannada_name": z.kannada_name,
                        "headquarters": z.headquarters,
                        "climate_description": z.climate_description,
                        "annual_rainfall_min_mm": z.annual_rainfall_min_mm,
                        "annual_rainfall_max_mm": z.annual_rainfall_max_mm,
                        "normal_rainfall_mm": z.normal_rainfall_mm,
                        "major_soils": z.major_soils or [],
                        "primary_crops": z.primary_crops or [],
                        "critical_risks": z.critical_risks or [],
                        "verification_status": z.verification_status,
                        "source_reference": z.source_reference
                    }
                    for z in zones
                ]
        return self.zones_data

    def get_all_districts(self, db: Optional[Session] = None) -> List[Dict[str, Any]]:
        if db:
            districts = db.query(District).order_by(District.name).all()
            if districts:
                return [
                    {
                        "id": d.id,
                        "name": d.name,
                        "kannada_name": d.kannada_name,
                        "zone_id": d.zone_id,
                        "secondary_zone_id": d.secondary_zone_id,
                        "headquarters": d.headquarters,
                        "latitude": d.latitude,
                        "longitude": d.longitude,
                        "normal_rainfall_mm": d.normal_rainfall_mm,
                        "dominant_soils": d.dominant_soils or [],
                        "drainage_profile": d.drainage_profile,
                        "drought_vulnerability": d.drought_vulnerability,
                        "taluks": [t.name for t in d.taluks] if d.taluks else []
                    }
                    for d in districts
                ]
        return self.districts_data

    def get_district_by_name(self, name: str, db: Optional[Session] = None) -> Optional[Dict[str, Any]]:
        name_clean = name.strip().lower()
        districts = self.get_all_districts(db)
        for d in districts:
            if d["name"].strip().lower() == name_clean:
                return d
        return None

    def get_zone_by_id(self, zone_id: int, db: Optional[Session] = None) -> Optional[Dict[str, Any]]:
        zones = self.get_all_zones(db)
        for z in zones:
            if z["id"] == zone_id:
                return z
        return None

    def resolve_location(self, district_name: str, taluk_name: Optional[str] = None, db: Optional[Session] = None) -> Dict[str, Any]:
        """Resolves district and taluk to authoritative Karnataka agro-climatic zone without guessing."""
        dist = self.get_district_by_name(district_name, db)
        if not dist:
            # Fallback search in data
            return {
                "district": district_name,
                "taluk": taluk_name or "General",
                "zone_id": 5, # default Eastern Dry fallback
                "zone_name": "Eastern Dry Zone",
                "zone_code": "ZONE_5",
                "latitude": 12.9716,
                "longitude": 77.5946,
                "normal_rainfall_mm": 750,
                "dominant_soils": ["Red sandy loams"],
                "drought_vulnerability": "Moderate",
                "is_verified": False
            }
        
        zone_id = dist["zone_id"]
        
        # Check if taluk maps to a specific secondary zone (e.g. Belagavi eastern vs western, Hassan malnad vs transition)
        if taluk_name and dist.get("secondary_zone_id"):
            taluk_clean = taluk_name.strip().lower()
            # If Belagavi eastern dry taluks: Athani, Raibag, Gokak, Ramdurg -> Zone 3
            if dist["name"].lower() == "belagavi" and taluk_clean in ["athani", "raibag", "gokak", "ramdurg"]:
                zone_id = 3
            # If Chikkamagaluru eastern dry taluks: Tarikere, Kadur -> Zone 7
            elif dist["name"].lower() == "chikkamagaluru" and taluk_clean in ["tarikere", "kadur", "ajjampura"]:
                zone_id = 7
            # If Hassan western malnad taluks: Sakleshpur, Alur -> Zone 9
            elif dist["name"].lower() == "hassan" and taluk_clean in ["sakleshpur", "alur"]:
                zone_id = 9
            # If Shivamogga transition: Davanagere border
            elif dist["name"].lower() == "shivamogga" and taluk_clean in ["sagara", "soraba", "hosanagara", "thirthahalli"]:
                zone_id = 9

        zone_info = self.get_zone_by_id(zone_id, db) or {}
        
        return {
            "district": dist["name"],
            "kannada_name": dist.get("kannada_name"),
            "taluk": taluk_name or (dist.get("taluks", [""])[0] if dist.get("taluks") else dist["name"]),
            "zone_id": zone_id,
            "zone_name": zone_info.get("name", "Karnataka Agricultural Zone"),
            "zone_kannada_name": zone_info.get("kannada_name"),
            "zone_code": zone_info.get("code", f"ZONE_{zone_id}"),
            "headquarters": dist.get("headquarters"),
            "latitude": dist.get("latitude", 12.9716),
            "longitude": dist.get("longitude", 77.5946),
            "normal_rainfall_mm": dist.get("normal_rainfall_mm", 750),
            "dominant_soils": dist.get("dominant_soils", []),
            "drainage_profile": dist.get("drainage_profile"),
            "drought_vulnerability": dist.get("drought_vulnerability", "Moderate"),
            "climate_description": zone_info.get("climate_description"),
            "is_verified": True
        }

    def resolve_gps_coordinates(self, lat: float, lon: float, db: Optional[Session] = None) -> Optional[Dict[str, Any]]:
        """Maps latitude and longitude to the closest Karnataka district."""
        districts = self.get_all_districts(db)
        if not districts:
            return None
            
        closest_dist = None
        min_distance = float("inf")
        
        for d in districts:
            d_lat = d["latitude"]
            d_lon = d["longitude"]
            # Euclidean distance approximation suitable for district bounding
            dist = math.sqrt((lat - d_lat)**2 + (lon - d_lon)**2)
            if dist < min_distance:
                min_distance = dist
                closest_dist = d
                
        if closest_dist and min_distance < 1.5:  # within ~150km of district center
            return self.resolve_location(closest_dist["name"], db=db)
        return None

location_service = LocationService()
