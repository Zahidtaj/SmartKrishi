"""Idempotent database seeding module for SmartKrishi."""

from sqlalchemy.orm import Session

from backend.config import get_settings
from backend.database import SessionLocal, init_db
from backend.models import (
    AdminUser,
    Crop,
    CropEconomicData,
    CropRequirement,
    KnowledgeArticle,
    Location,
    RegionalCropRule,
)
from backend.regional_data import (
    CROP_OBSERVATION_PROFILES,
    LAST_VERIFIED_DATE,
    ZONE_AGRICULTURAL_PROFILES,
)
from backend.security import hash_password
from backend.seed_crops import CROP_SEED_DATA
from backend.seed_knowledge import KNOWLEDGE_SEED_DATA
from backend.seed_locations import KARNATAKA_LOCATIONS


def seed_database(db: Session) -> dict[str, int]:
    """Populate initial locations, crops, rules, economic data, knowledge articles, and admin account."""
    counts = {"locations": 0, "crops": 0, "rules": 0, "articles": 0, "admin_users": 0}

    # 1. Seed Locations with verified Karnataka Agro-Climatic Zone profiles
    existing_locs = {
        (row.state, row.district, row.taluk)
        for row in db.query(Location.state, Location.district, Location.taluk).all()
    }
    for loc in KARNATAKA_LOCATIONS:
        key = (loc["state"], loc["district"], loc["taluk"])
        if key not in existing_locs:
            zone_profile = ZONE_AGRICULTURAL_PROFILES[loc["code"]]
            db.add(
                Location(
                    state=loc["state"],
                    district=loc["district"],
                    taluk=loc["taluk"],
                    agro_climatic_zone=loc["zone"],
                    zone_code=loc["code"],
                    normal_annual_rainfall_mm=loc["rain"],
                    typical_rainfall_pattern=zone_profile["typical_rainfall_pattern"],
                    dominant_soil_types=loc["soils"],
                    common_soil_textures=zone_profile["common_soil_textures"],
                    major_crops=zone_profile["major_crops"],
                    recommended_seasons_summary=zone_profile["recommended_seasons_summary"],
                    growing_period_info=zone_profile["growing_period_info"],
                    regional_references=zone_profile["regional_references"],
                    data_source="Karnataka NARP 10 Agro-Climatic Zones Reference (KSDA / UAS Bengaluru / UAS Dharwad / ICAR)",
                    verification_status=zone_profile["verification_status"],
                    last_updated=zone_profile["last_updated"],
                )
            )
            counts["locations"] += 1

    # 2. Seed Crops, Observation Requirements, Regional Rules, and Illustrative Economic Data
    existing_crops = {row.crop_key: row for row in db.query(Crop).all()}
    for item in CROP_SEED_DATA:
        crop_key = item["crop_key"]
        if crop_key in existing_crops:
            continue

        obs = CROP_OBSERVATION_PROFILES[crop_key]
        crop = Crop(
            crop_key=crop_key,
            name_en=item["name_en"],
            name_kn=item["name_kn"],
            scientific_name=item["scientific_name"],
            category=item["category"],
            image_asset=item["image_asset"],
            growing_duration_days_min=item["dur_min"],
            growing_duration_days_max=item["dur_max"],
            duration_category=obs["duration_category"],
            water_requirement_level=item["water_level"],
            water_requirement_mm_min=item["water_mm_min"],
            water_requirement_mm_max=item["water_mm_max"],
            seed_rate_kg_per_acre=item["seed_rate"],
            household_food_crop=obs["household_food_crop"],
            commercial_crop=obs["commercial_crop"],
            cultivation_guidance_en=item["guidance_en"],
            cultivation_guidance_kn=item["guidance_kn"],
            information_source=item["source"],
            record_status="verified_reference",
            verification_status="verified_institutional_reference",
            last_updated=LAST_VERIFIED_DATE,
            in_ml_dataset=item["in_ml_dataset"],
            is_active=True,
        )
        req_data = item["req"]
        crop.requirement = CropRequirement(
            suitable_soil_types=req_data["soils"],
            suitable_textures=obs["suitable_textures"],
            suitable_drainage=obs["suitable_drainage"],
            moisture_needs=obs["moisture_needs"],
            suitable_land_topography=obs["suitable_land_topography"],
            min_soil_depth=obs["min_soil_depth"],
            drought_tolerance=obs["drought_tolerance"],
            waterlogging_tolerance=obs["waterlogging_tolerance"],
            sowing_months=obs["sowing_months"],
            weather_risk_thresholds=obs["weather_risk_thresholds"],
            ph_min=req_data["ph_min"],
            ph_max=req_data["ph_max"],
            ph_optimal_min=req_data["ph_opt_min"],
            ph_optimal_max=req_data["ph_opt_max"],
            nitrogen_min=req_data["n_min"],
            nitrogen_max=req_data["n_max"],
            phosphorus_min=req_data["p_min"],
            phosphorus_max=req_data["p_max"],
            potassium_min=req_data["k_min"],
            potassium_max=req_data["k_max"],
            temp_min_c=req_data["t_min"],
            temp_max_c=req_data["t_max"],
            humidity_min_pct=req_data["h_min"],
            humidity_max_pct=req_data["h_max"],
            rainfall_min_mm=req_data["r_min"],
            rainfall_max_mm=req_data["r_max"],
            suitable_seasons=req_data["seasons"],
            supported_water_levels=req_data["water_levels"],
        )

        # Regional Rules for Karnataka Zones
        zones = item["zones"]
        if not zones:
            for season in req_data["seasons"]:
                crop.regional_rules.append(
                    RegionalCropRule(
                        state="Karnataka",
                        district=None,
                        agro_climatic_zone=None,
                        season=season,
                        suitability_level="restricted",
                        priority_weight=0.1,
                        rule_notes_en=f"{item['name_en']} is outside standard Karnataka agro-climatic cultivation zones.",
                        rule_notes_kn=f"{item['name_kn']} ಕರ್ನಾಟಕದ ಪ್ರಮಾಣಿತ ಕೃಷಿ-ಹವಾಮಾನ ವಲಯಗಳಿಗೆ ಸಾಮಾನ್ಯವಾಗಿ ಸೂಕ್ತವಲ್ಲ.",
                        source=item["source"],
                    )
                )
                counts["rules"] += 1
        else:
            for zone_code in zones:
                for season in req_data["seasons"]:
                    crop.regional_rules.append(
                        RegionalCropRule(
                            state="Karnataka",
                            district=None,
                            agro_climatic_zone=zone_code,
                            season=season,
                            suitability_level="recommended",
                            priority_weight=1.0,
                            rule_notes_en=f"Documented for {zone_code} during {season} when observed land, soil texture, drainage, and water criteria align.",
                            rule_notes_kn=f"{zone_code} ವಲಯದಲ್ಲಿ {season} ಹಂಗಾಮಿಗೆ ಭೂಮಿ, ಮಣ್ಣಿನ ವಿನ್ಯಾಸ, ನೀರು ಬಸಿಯುವಿಕೆ ಮತ್ತು ನೀರಾವರಿ ಪೂರಕವಾಗಿದ್ದಲ್ಲಿ ಸೂಕ್ತ.",
                            source=item["source"],
                        )
                    )
                    counts["rules"] += 1

        econ = item["econ"]
        crop.economic_data.append(
            CropEconomicData(
                region_scope="Karnataka (Prototype Illustrative Baseline)",
                season=econ["season"],
                seed_cost_inr_per_acre=econ["seed_cost"],
                cultivation_cost_min_inr_per_acre=econ["cost_min"],
                cultivation_cost_max_inr_per_acre=econ["cost_max"],
                expected_yield_qtl_min=econ["yield_min"],
                expected_yield_qtl_max=econ["yield_max"],
                indicative_price_inr_per_qtl=econ["price"],
                assumptions_en=econ["assump_en"],
                assumptions_kn=econ["assump_kn"],
                data_status="prototype_demonstration",
                source=item["source"],
            )
        )
        db.add(crop)
        counts["crops"] += 1

    # 3. Seed Knowledge Articles
    existing_slugs = {row[0] for row in db.query(KnowledgeArticle.slug).all()}
    for art in KNOWLEDGE_SEED_DATA:
        if art["slug"] not in existing_slugs:
            db.add(
                KnowledgeArticle(
                    slug=art["slug"],
                    category=art["category"],
                    title_en=art["title_en"],
                    title_kn=art["title_kn"],
                    summary_en=art["summary_en"],
                    summary_kn=art["summary_kn"],
                    content_en=art["content_en"],
                    content_kn=art["content_kn"],
                    source_name=art["source_name"],
                    source_url=art["source_url"],
                    is_published=True,
                )
            )
            counts["articles"] += 1

    # 4. Seed Local Dev Admin User (using PBKDF2-HMAC-SHA256 password hash)
    settings = get_settings()
    admin_exists = db.query(AdminUser).filter(AdminUser.username == settings.admin_username).first()
    if admin_exists is None:
        db.add(
            AdminUser(
                username=settings.admin_username,
                password_hash=hash_password(settings.admin_password),
                role="admin",
                is_active=True,
            )
        )
        counts["admin_users"] += 1

    db.commit()
    return counts


def initialize_and_seed() -> dict[str, int]:
    init_db()
    with SessionLocal() as db:
        return seed_database(db)


if __name__ == "__main__":
    inserted = initialize_and_seed()
    print(f"Database initialized & seeded: {inserted}")
