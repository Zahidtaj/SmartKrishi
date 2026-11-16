import json
import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from backend.app.db.database import engine, Base, SessionLocal
from backend.app.core.config import settings
from backend.app.models.models import (
    State, AgroClimaticZone, District, Taluk, Crop,
    CropRequirement, CropEconomicData, RegionalCropSuitability,
    KnowledgeArticle, DataSource, AgriculturalAdvisory
)

def seed_database():
    """Idempotent database seeder for SmartKrishi."""
    print("Creating database tables if not existing...")
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    try:
        # 1. Seed State
        karnataka = db.query(State).filter_by(code="KA").first()
        if not karnataka:
            karnataka = State(code="KA", name="Karnataka", kannada_name="ಕರ್ನಾಟಕ")
            db.add(karnataka)
            db.commit()
            db.refresh(karnataka)
            print("Seeded State: Karnataka")

        # 2. Seed Agro-Climatic Zones
        zones_file = settings.DATA_PATH / "karnataka_zones.json"
        if zones_file.exists():
            with open(zones_file, "r", encoding="utf-8") as f:
                zones_data = json.load(f)
                for z in zones_data:
                    existing = db.query(AgroClimaticZone).filter_by(id=z["id"]).first()
                    if not existing:
                        zone_obj = AgroClimaticZone(
                            id=z["id"],
                            code=z["code"],
                            name=z["name"],
                            kannada_name=z.get("kannada_name"),
                            headquarters=z.get("headquarters"),
                            districts_covered=z.get("districts", []),
                            taluks_covered=z.get("taluks", []),
                            climate_description=z.get("climate_description"),
                            annual_rainfall_min_mm=z.get("annual_rainfall_min_mm"),
                            annual_rainfall_max_mm=z.get("annual_rainfall_max_mm"),
                            normal_rainfall_mm=z.get("normal_rainfall_mm"),
                            major_soils=z.get("major_soils", []),
                            primary_crops=z.get("primary_crops", []),
                            critical_risks=z.get("critical_risks", []),
                            verification_status=z.get("verification_status", "verified"),
                            source_reference=z.get("source_reference")
                        )
                        db.add(zone_obj)
                db.commit()
                print("Seeded Agro-Climatic Zones")

        # 3. Seed Districts & Taluks
        districts_file = settings.DATA_PATH / "karnataka_districts.json"
        if districts_file.exists():
            with open(districts_file, "r", encoding="utf-8") as f:
                districts_data = json.load(f)
                for d in districts_data:
                    dist_obj = db.query(District).filter_by(name=d["name"]).first()
                    if not dist_obj:
                        dist_obj = District(
                            id=d["id"],
                            state_id=karnataka.id,
                            zone_id=d["zone_id"],
                            secondary_zone_id=d.get("secondary_zone_id"),
                            name=d["name"],
                            kannada_name=d.get("kannada_name"),
                            headquarters=d.get("headquarters"),
                            latitude=d["latitude"],
                            longitude=d["longitude"],
                            normal_rainfall_mm=d.get("normal_rainfall_mm"),
                            dominant_soils=d.get("dominant_soils", []),
                            drainage_profile=d.get("drainage_profile"),
                            drought_vulnerability=d.get("drought_vulnerability")
                        )
                        db.add(dist_obj)
                        db.commit()
                        db.refresh(dist_obj)

                        # Add taluks for this district
                        for taluk_name in d.get("taluks", []):
                            taluk_obj = Taluk(
                                district_id=dist_obj.id,
                                name=taluk_name,
                                zone_id=d["zone_id"]
                            )
                            db.add(taluk_obj)
                db.commit()
                print("Seeded 31 Districts and Taluks")

        # 4. Seed Crops, Requirements & Economic Benchmarks
        crops_file = settings.DATA_PATH / "crops_karnataka.json"
        if crops_file.exists():
            with open(crops_file, "r", encoding="utf-8") as f:
                crops_data = json.load(f)
                for c in crops_data:
                    crop_obj = db.query(Crop).filter_by(id=c["id"]).first()
                    if not crop_obj:
                        crop_obj = Crop(
                            id=c["id"],
                            name=c["crop_name"],
                            kannada_name=c.get("kannada_name"),
                            scientific_name=c.get("scientific_name"),
                            category=c.get("category"),
                            suitable_zones=c.get("suitable_zones", []),
                            suitable_districts=c.get("suitable_districts", [])
                        )
                        db.add(crop_obj)
                        db.commit()

                        # Requirements
                        req = CropRequirement(
                            crop_id=c["id"],
                            preferred_textures=c.get("preferred_soil_textures", []),
                            acceptable_textures=c.get("acceptable_soil_textures", []),
                            unsuitable_textures=c.get("unsuitable_soil_textures", []),
                            preferred_colors=c.get("preferred_soil_colors", []),
                            acceptable_colors=c.get("acceptable_soil_colors", []),
                            unsuitable_colors=c.get("unsuitable_soil_colors", []),
                            drainage_preferred=c.get("drainage_requirements", {}).get("preferred", []),
                            drainage_unsuitable=c.get("drainage_requirements", {}).get("unsuitable", []),
                            moisture_preferred=c.get("moisture_retention", {}).get("preferred", []),
                            min_soil_depth=c.get("min_soil_depth", "Medium"),
                            water_req_min_mm=c.get("water_requirement_mm", {}).get("min", 400),
                            water_req_opt_min_mm=c.get("water_requirement_mm", {}).get("optimal_min", 450),
                            water_req_opt_max_mm=c.get("water_requirement_mm", {}).get("optimal_max", 650),
                            water_req_max_mm=c.get("water_requirement_mm", {}).get("max", 800),
                            suitable_water_sources=c.get("suitable_water_sources", []),
                            water_scarcity_tolerance=c.get("water_scarcity_tolerance", "Moderate"),
                            temp_min_c=c.get("temperature_c", {}).get("min", 15),
                            temp_opt_min_c=c.get("temperature_c", {}).get("optimal_min", 20),
                            temp_opt_max_c=c.get("temperature_c", {}).get("optimal_max", 35),
                            temp_max_c=c.get("temperature_c", {}).get("max", 40),
                            rain_min_mm=c.get("rainfall_mm", {}).get("min", 400),
                            rain_opt_min_mm=c.get("rainfall_mm", {}).get("optimal_min", 500),
                            rain_opt_max_mm=c.get("rainfall_mm", {}).get("optimal_max", 800),
                            rain_max_mm=c.get("rainfall_mm", {}).get("max", 1100),
                            suitable_seasons=c.get("suitable_seasons", []),
                            sowing_windows=c.get("sowing_windows", {}),
                            duration_min_days=c.get("duration_days", {}).get("min", 100),
                            duration_max_days=c.get("duration_days", {}).get("max", 120),
                            duration_category=c.get("duration_days", {}).get("category", "Medium"),
                            preferred_slopes=c.get("land_suitability", {}).get("preferred_slopes", []),
                            unsuitable_slopes=c.get("land_suitability", {}).get("unsuitable_slopes", []),
                            favored_predecessors=c.get("rotation_predecessors_favored", []),
                            discouraged_predecessors=c.get("rotation_predecessors_discouraged", []),
                            critical_risks=c.get("critical_risks", []),
                            cultivation_practices=c.get("cultivation_practices", ""),
                            verification_status=c.get("verification_status", "verified"),
                            source_reference=c.get("source_reference", "")
                        )
                        db.add(req)

                        # Economics
                        econ = c.get("economics")
                        if econ:
                            econ_obj = CropEconomicData(
                                crop_id=c["id"],
                                seed_cost_per_acre_inr=econ.get("seed_cost_per_acre_inr"),
                                input_cost_per_acre_inr=econ.get("input_cost_per_acre_inr"),
                                labor_cost_per_acre_inr=econ.get("labor_cost_per_acre_inr"),
                                total_cost_per_acre_inr=econ.get("total_cost_per_acre_inr"),
                                avg_yield_quintals_per_acre_min=econ.get("avg_yield_quintals_per_acre_min"),
                                avg_yield_quintals_per_acre_max=econ.get("avg_yield_quintals_per_acre_max"),
                                benchmark_msp_inr_per_quintal=econ.get("benchmark_msp_inr_per_quintal"),
                                data_year=econ.get("data_year", "2024-25"),
                                source_reference=econ.get("source_reference")
                            )
                            db.add(econ_obj)
                db.commit()
                print("Seeded 16 Crops and Agronomic Requirements")

        # 5. Seed Knowledge Articles
        articles_file = settings.DATA_PATH / "knowledge_articles.json"
        if articles_file.exists():
            with open(articles_file, "r", encoding="utf-8") as f:
                articles_data = json.load(f)
                for a in articles_data:
                    existing_art = db.query(KnowledgeArticle).filter_by(id=a["id"]).first()
                    if not existing_art:
                        art_obj = KnowledgeArticle(
                            id=a["id"],
                            title=a["title"],
                            kannada_title=a.get("kannada_title"),
                            category=a.get("category"),
                            summary=a.get("summary"),
                            content=a["content"],
                            source=a.get("source"),
                            verification_status=a.get("verification_status", "verified"),
                            publication_date=a.get("publication_date"),
                            geographic_applicability=a.get("geographic_applicability")
                        )
                        db.add(art_obj)
                db.commit()
                print("Seeded Knowledge Articles")

        # 6. Seed Data Sources
        sources_file = settings.DATA_PATH / "data_sources.json"
        if sources_file.exists():
            with open(sources_file, "r", encoding="utf-8") as f:
                sources_data = json.load(f)
                for s in sources_data:
                    existing_src = db.query(DataSource).filter_by(id=s["id"]).first()
                    if not existing_src:
                        src_obj = DataSource(
                            id=s["id"],
                            source_name=s["source_name"],
                            source_url=s.get("source_url"),
                            data_category=s.get("data_category"),
                            geographic_coverage=s.get("geographic_coverage"),
                            collection_date=s.get("collection_date"),
                            verification_date=s.get("verification_date"),
                            license_or_usage=s.get("license_or_usage"),
                            data_status=s.get("data_status", "verified"),
                            update_frequency=s.get("update_frequency")
                        )
                        db.add(src_obj)
                db.commit()
                print("Seeded Data Sources Registry")

        print("Database seed complete successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
