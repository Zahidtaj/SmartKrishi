import datetime
from typing import List, Dict, Any

class AdvisoryService:
    def generate_advisories_for_location(
        self,
        district_name: str,
        zone_id: int,
        weather: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generates contextual agricultural advisories based on meteorological conditions
        and regional agro-climatic zone parameters.
        """
        advisories: List[Dict[str, Any]] = []
        now = datetime.datetime.utcnow()
        month = now.month
        
        temp_c = weather.get("current_temperature_c", 28.0)
        recent_rain = weather.get("recent_precipitation_mm", 0.0)
        dry_days = weather.get("consecutive_dry_days_forecast", 0)
        heavy_rain_flag = weather.get("heavy_rainfall_alert", False)
        is_live = weather.get("is_live_data", False)

        # 1. Seasonal Sowing Window Advisory
        if month in [6, 7]:
            advisories.append({
                "id": 1,
                "title": "Prime Kharif Sowing Window Active",
                "kannada_title": "ಮುಖ್ಯ ಮುಂಗಾರು ಬಿತ್ತನೆ ಸಮಯ ಸಕ್ರಿಯವಾಗಿದೆ",
                "advisory_type": "Sowing Window",
                "severity": "Info",
                "message": (
                    f"Optimal window for sowing Kharif field crops (Ragi, Red Gram, Groundnut, Maize, Soybean) "
                    f"is active across {district_name}. Ensure seed treatment with recommended bio-fertilizers "
                    f"(Trichoderma and Rhizobium for pulses) before sowing."
                ),
                "kannada_message": "ಮುಂಗಾರು ಬೆಳೆಗಳ ಬಿತ್ತನೆಗೆ ಸೂಕ್ತ ಸಮಯ. ಬಿತ್ತನೆಗೆ ಮುನ್ನ ಜೈವಿಕ ಗೊಬ್ಬರಗಳಿಂದ ಬೀಜೋಪಚಾರ ಮಾಡಿ.",
                "source": "UAS Bengaluru & Dharwad Agrometeorological Advisory",
                "valid_from": now.strftime("%Y-%m-01"),
                "valid_until": (now + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
            })
        elif month in [9, 10]:
            advisories.append({
                "id": 2,
                "title": "Rabi Conserved-Moisture Sowing Advisory",
                "kannada_title": "ಹಿಂಗಾರು ತೇವಾಂಶ ಆಧಾರಿತ ಬಿತ್ತನೆ ಸಲಹೆ",
                "advisory_type": "Sowing Window",
                "severity": "Info",
                "message": (
                    f"Conserve receding September rainfall in medium and deep black soils for Rabi Jowar (Maldandi) "
                    f"and Bengal Gram (Chickpea). Sow when soil temperature drops below 28°C."
                ),
                "kannada_message": "ಹಿಂಗಾರು ಜೋಳ ಮತ್ತು ಕಡಲೆ ಬಿತ್ತನೆಗೆ ಸೆಪ್ಟೆಂಬರ್ ಮಳೆಯ ತೇವಾಂಶವನ್ನು ಸಂರಕ್ಷಿಸಿ.",
                "source": "UAS Dharwad Main Research Station",
                "valid_from": now.strftime("%Y-%m-01"),
                "valid_until": (now + datetime.timedelta(days=35)).strftime("%Y-%m-%d")
            })
        elif month in [1, 2]:
            advisories.append({
                "id": 3,
                "title": "Summer Irrigated Crops Preparation",
                "kannada_title": "ಬೇಸಿಗೆ ನೀರಾವರಿ ಬೆಳೆಗಳ ಪೂರ್ವಸಿದ್ಧತೆ",
                "advisory_type": "Sowing Window",
                "severity": "Info",
                "message": (
                    f"For farmers with assured borewell or open well water, early Summer sowing of Groundnut, "
                    f"Sesamum, or Green Gram should be completed by mid-February to avoid peak summer water stress."
                ),
                "kannada_message": "ಬೋರ್‌ವೆಲ್ ನೀರು ಲಭ್ಯವಿರುವವರು ಫೆಬ್ರವರಿ ಮಧ್ಯದೊಳಗೆ ಬೇಸಿಗೆ ಕಡಲೆಕಾಯಿ/ಎಳ್ಳು ಬಿತ್ತನೆ ಮುಗಿಸಿ.",
                "source": "KSDA Agricultural Advisory",
                "valid_from": now.strftime("%Y-%m-01"),
                "valid_until": (now + datetime.timedelta(days=25)).strftime("%Y-%m-%d")
            })

        # 2. Weather Warnings: Heavy Rainfall
        if heavy_rain_flag or recent_rain > 50.0:
            advisories.append({
                "id": 4,
                "title": "Heavy Rainfall & Drainage Alert",
                "kannada_title": "ಭಾರೀ ಮಳೆ ಮತ್ತು ನೀರುಗಾಲುವೆ ಎಚ್ಚರಿಕೆ",
                "advisory_type": "Heavy Rainfall Warning",
                "severity": "Warning",
                "message": (
                    f"High precipitation detected or projected in {district_name}. Immediately clear field drainage "
                    f"channels to prevent waterlogging around Red Gram, Maize, and Groundnut fields. Postpone top-dressing of nitrogen."
                ),
                "kannada_message": "ಭಾರೀ ಮಳೆಯ ಮುನ್ಸೂಚನೆ ಇರುವುದರಿಂದ ಜಮೀನಿನಲ್ಲಿ ನೀರು ನಿಲ್ಲದಂತೆ ಬಸಿದು ಹೋಗಲು ಕಾಲುವೆಗಳನ್ನು ತೆರವುಗೊಳಿಸಿ.",
                "source": "IMD District Agromet Advisory Service (DAMAS)",
                "valid_from": now.strftime("%Y-%m-%d"),
                "valid_until": (now + datetime.timedelta(days=5)).strftime("%Y-%m-%d")
            })

        # 3. Weather Warnings: Dry Spell Precaution
        if dry_days >= 5:
            advisories.append({
                "id": 5,
                "title": "Dry Spell & In-Situ Moisture Precaution",
                "kannada_title": "ಒಣ ಹವೆಯ ಮುನ್ಸೂಚನೆ ಮತ್ತು ತೇವಾಂಶ ನಿರ್ವಹಣೆ",
                "advisory_type": "Dry Spell Alert",
                "severity": "Alert",
                "message": (
                    f"Extended dry spell ({dry_days} days with <2.5 mm rainfall) indicated in 7-day outlook. "
                    f"Apply straw mulching or shallow inter-cultivation (hoeing) to create a dust mulch and "
                    f"retard capillary evaporation."
                ),
                "kannada_message": "ಮುಂದಿನ ದಿನಗಳಲ್ಲಿ ಮಳೆ ಕೊರತೆ ಇರುವುದರಿಂದ ಬೆಳೆಗಳಿಗೆ ಕಳೆ ಕೀಳುವಿಕೆ ಮತ್ತು ಹೊದಿಕೆ (ಮಲ್ಚಿಂಗ್) ಮಾಡಿ ತೇವಾಂಶ ಕಾಪಾಡಿ.",
                "source": "Agromet Field Unit (AMFU) Karnataka",
                "valid_from": now.strftime("%Y-%m-%d"),
                "valid_until": (now + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
            })

        # 4. Thermal Stress Alert
        if temp_c > 37.0:
            advisories.append({
                "id": 6,
                "title": "High Temperature Caution",
                "kannada_title": "ಹೆಚ್ಚಿನ ತಾಪಮಾನದ ಮುನ್ನೆಚ್ಚರಿಕೆ",
                "advisory_type": "Temperature Alert",
                "severity": "Warning",
                "message": (
                    f"Current temperature ({temp_c}°C) is above normal for {district_name}. "
                    f"Provide light irrigations during evening hours for horticultural crops and avoid pesticide spraying in peak afternoon."
                ),
                "kannada_message": "ತಾಪಮಾನ ಹೆಚ್ಚಾಗಿರುವುದರಿಂದ ಸಂಜೆ ಸಮಯದಲ್ಲಿ ನೀರು ಹಾಯಿಸಿ, ಮಧ್ಯಾಹ್ನ ಸಿಂಪಡಣೆ ಮಾಡಬೇಡಿ.",
                "source": "District Disaster Management & Agromet Service",
                "valid_from": now.strftime("%Y-%m-%d"),
                "valid_until": (now + datetime.timedelta(days=4)).strftime("%Y-%m-%d")
            })

        return advisories

advisory_service = AdvisoryService()
