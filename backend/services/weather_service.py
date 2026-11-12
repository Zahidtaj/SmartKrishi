"""Modular weather and climate intelligence service for SmartKrishi.

Strictly separates:
A. Long-term climate normals (institutional zone/district baselines)
B. Current weather (real external feed if reachable & enabled; otherwise explicit 'unavailable')
C. Short-term 7-day forecast (real external feed if reachable & enabled; otherwise explicit 'unavailable')
D. Seasonal outlook (historical agro-climatic growing-period guidance + official IMD/KSNDMC references)

Never fabricates live weather values or substitutes historical averages as live observations.
"""

from datetime import datetime, timezone
from typing import Any
import httpx

from backend.config import get_settings
from backend.models import Location
from backend.regional_data import ZONE_AGRICULTURAL_PROFILES

# Verified district HQ latitude/longitude centroids across Karnataka for optional Open-Meteo lookups
KARNATAKA_DISTRICT_COORDS: dict[str, tuple[float, float]] = {
    "Bagalkote": (16.185, 75.696),
    "Ballari": (15.139, 76.921),
    "Belagavi": (15.849, 74.497),
    "Bengaluru Rural": (13.249, 77.712),
    "Bengaluru Urban": (12.971, 77.594),
    "Bidar": (17.910, 77.519),
    "Chamarajanagara": (11.926, 76.943),
    "Chikkaballapura": (13.435, 77.731),
    "Chikkamagaluru": (13.316, 75.775),
    "Chitradurga": (14.225, 76.398),
    "Dakshina Kannada": (12.914, 74.856),
    "Davanagere": (14.464, 75.921),
    "Dharwad": (15.458, 75.007),
    "Gadag": (15.431, 75.635),
    "Hassan": (13.007, 76.096),
    "Haveri": (14.795, 75.404),
    "Kalaburagi": (17.329, 76.834),
    "Kodagu": (12.424, 75.738),
    "Kolar": (13.136, 78.129),
    "Koppal": (15.345, 76.154),
    "Mandya": (12.521, 76.895),
    "Mysuru": (12.295, 76.639),
    "Raichur": (16.207, 77.346),
    "Ramanagara": (12.720, 77.281),
    "Shivamogga": (13.929, 75.568),
    "Tumakuru": (13.339, 77.113),
    "Udupi": (13.340, 74.742),
    "Uttara Kannada": (14.793, 74.124),
    "Vijayanagara": (15.268, 76.390),
    "Vijayapura": (16.830, 75.710),
    "Yadgir": (16.770, 77.137),
}


def _fetch_open_meteo(district: str, timeout_s: float) -> dict[str, Any] | None:
    coords = KARNATAKA_DISTRICT_COORDS.get(district)
    if not coords:
        return None
    lat, lon = coords
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        "&forecast_days=7&timezone=Asia%2FKolkata"
    )
    try:
        with httpx.Client(timeout=timeout_s) as client:
            resp = client.get(url)
            resp.raise_for_status()
            return resp.json()
    except Exception:
        return None


def get_weather_intelligence(
    *,
    location: Location,
    season: str,
    soil_observation: dict[str, Any],
    water_source: str,
    water_reliability: str,
    intended_sowing_month: str | None = None,
    force_live_unavailable: bool = False,
) -> dict[str, Any]:
    """Assemble honest, source-separated climate normals, optional live weather, and farmer weather advisory."""
    settings = get_settings()
    zone_profile = ZONE_AGRICULTURAL_PROFILES[location.zone_code]
    season_normal = zone_profile["climate_normals"].get(
        season, zone_profile["climate_normals"]["Kharif"]
    )

    long_term_climate = {
        "status": "available",
        "data_category": "institution_sourced",
        "zone_name": location.agro_climatic_zone,
        "zone_code": location.zone_code,
        "normal_annual_rainfall_mm": location.normal_annual_rainfall_mm,
        "typical_rainfall_pattern": location.typical_rainfall_pattern,
        "season_reference": season,
        "season_normal_temp_c": season_normal["temp_c"],
        "season_normal_humidity_pct": season_normal["humidity_pct"],
        "season_normal_rainfall_mm": season_normal["seasonal_rain_mm"],
        "growing_period_info": location.growing_period_info,
        "source": location.data_source,
        "verification_status": location.verification_status,
        "last_updated": str(location.last_updated),
    }

    raw_live = None
    if settings.enable_live_weather and not force_live_unavailable:
        raw_live = _fetch_open_meteo(location.district, settings.weather_timeout_seconds)

    if raw_live and "current" in raw_live and "daily" in raw_live:
        curr = raw_live["current"]
        daily = raw_live["daily"]
        rain_7d = sum(float(v or 0.0) for v in daily.get("precipitation_sum", []))
        max_day_rain = max((float(v or 0.0) for v in daily.get("precipitation_sum", [])), default=0.0)
        tmax_vals = [float(v) for v in daily.get("temperature_2m_max", []) if v is not None]
        tmin_vals = [float(v) for v in daily.get("temperature_2m_min", []) if v is not None]

        current_weather = {
            "status": "available",
            "data_category": "weather_provider_sourced",
            "provider": "Open-Meteo District HQ Feed (Reference Only — Confirm with IMD/KSNDMC)",
            "observed_at": curr.get("time") or datetime.now(timezone.utc).isoformat(),
            "temperature_c": curr.get("temperature_2m"),
            "humidity_pct": curr.get("relative_humidity_2m"),
            "precipitation_mm": curr.get("precipitation"),
            "wind_speed_kmh": curr.get("wind_speed_10m"),
            "disclaimer_en": "District centroid feed; local micro-weather may differ across villages.",
            "disclaimer_kn": "ಜಿಲ್ಲಾ ಕೇಂದ್ರದ ಹವಾಮಾನ ಮಾಹಿತಿ; ಗ್ರಾಮ ಮಟ್ಟದಲ್ಲಿ ಸ್ವಲ್ಪ ವ್ಯತ್ಯಾಸವಿರಬಹುದು.",
        }
        short_term_forecast = {
            "status": "available",
            "data_category": "weather_provider_sourced",
            "provider": "Open-Meteo 7-Day District Outlook",
            "next_7_days_rain_total_mm": round(rain_7d, 1),
            "peak_daily_rain_mm": round(max_day_rain, 1),
            "temp_max_c": round(max(tmax_vals), 1) if tmax_vals else None,
            "temp_min_c": round(min(tmin_vals), 1) if tmin_vals else None,
            "dates": daily.get("time", []),
            "daily_rain_mm": daily.get("precipitation_sum", []),
        }
        live_available = True
    else:
        current_weather = {
            "status": "unavailable",
            "data_category": "weather_provider_sourced",
            "provider": "IMD Agromet / KSNDMC Varuna Mitra (External Live Feed Not Connected)",
            "temperature_c": None,
            "humidity_pct": None,
            "precipitation_mm": None,
            "reason_en": "Live weather observations are currently unavailable. SmartKrishi never substitutes simulated values as live weather.",
            "reason_kn": "ಪ್ರಸ್ತುತ ನೇರ ಹವಾಮಾನ ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ. SmartKrishi ಕೃತಕ ಹವಾಮಾನ ಅಂಕಿಗಳನ್ನು ತೋರಿಸುವುದಿಲ್ಲ.",
            "official_links": [
                {"name": "IMD Agromet Advisories", "url": "https://agromet.imd.gov.in/"},
                {"name": "KSNDMC Karnataka", "url": "https://www.ksndmc.org/"},
            ],
        }
        short_term_forecast = {
            "status": "unavailable",
            "data_category": "weather_provider_sourced",
            "provider": "IMD 5-Day Block Forecast / KSNDMC",
            "next_7_days_rain_total_mm": None,
            "peak_daily_rain_mm": None,
            "reason_en": "Short-term rainfall forecast is unavailable offline; verify 5-day block weather via IMD Mausam or Varuna Mitra (1800-425-7111) before sowing.",
            "reason_kn": "ಮುಂದಿನ ದಿನಗಳ ಮಳೆ ಮುನ್ಸೂಚನೆ ಲಭ್ಯವಿಲ್ಲ; ಬಿತ್ತನೆಗೆ ಮುನ್ನ IMD ಅಥವಾ ವರುಣ ಮಿತ್ರ (1800-425-7111) ಸಂಪರ್ಕಿಸಿ.",
        }
        live_available = False

    seasonal_outlook = {
        "status": "reference_normal",
        "data_category": "institution_sourced",
        "outlook_summary_en": f"Historical NARP baseline for {location.agro_climatic_zone}: {location.typical_rainfall_pattern}",
        "outlook_summary_kn": f"{location.agro_climatic_zone} ದೀರ್ಘಕಾಲೀನ ಮಳೆ ಮಾದರಿ: ಸಾಮಾನ್ಯ ವಾರ್ಷಿಕ ಮಳೆ {location.normal_annual_rainfall_mm or 'N/A'} ಮಿ.ಮೀ.",
        "recommended_window_en": zone_profile["recommended_seasons_summary"].get(
            season, "Align sowing with dependable soil moisture onset."
        ),
        "recommended_window_kn": f"{season} ಹಂಗಾಮಿಗೆ ಮಣ್ಣಿನಲ್ಲಿ ಸಾಕಷ್ಟು ತೇವಾಂಶ ಬಂದ ನಂತರ ಬಿತ್ತನೆ ಕೈಗೊಳ್ಳಿ.",
        "limitation_en": "Seasonal outlook reflects long-term zone averages, not an official El-Nino/IMD seasonal monsoon forecast.",
        "limitation_kn": "ಇದು ದೀರ್ಘಕಾಲೀನ ಸರಾಸರಿ ಮಾಹಿತಿಯಾಗಿದ್ದು, ಅಧಿಕೃತ IMD ಮುಂಗಾರು ಮುನ್ಸೂಚನೆಯಲ್ಲ.",
    }

    # Build Practical "Weather and Farming Advisory"
    effective_drainage = soil_observation.get("effective_drainage", "unknown")
    annual_rain = location.normal_annual_rainfall_mm or 700.0
    season_rain = season_normal["seasonal_rain_mm"]

    # Heavy rain / waterlogging assessment
    if (live_available and (short_term_forecast.get("peak_daily_rain_mm") or 0.0) >= 50.0) or (
        effective_drainage == "waterlogging_prone" and (season in ("Kharif", "Perennial") or annual_rain >= 600.0)
    ) or (
        effective_drainage == "slow_draining" and (annual_rain >= 900.0 or season_rain >= 600.0)
    ):
        heavy_rain_risk_level = "high"
        heavy_rain_en = "Elevated waterlogging risk during monsoon showers due to slow field drainage or high rainfall belt. Prepare drainage furrows before sowing."
        heavy_rain_kn = "ಮಣ್ಣಿನಲ್ಲಿ ನೀರು ನಿಲ್ಲುವ ಸಾಧ್ಯತೆ ಅಥವಾ ಅಧಿಕ ಮಳೆ ವಲಯದ ಕಾರಣ ಬಸಿಕಾಲುವೆ ವ್ಯವಸ್ಥೆ ಕಡ್ಡಾಯ."
    elif annual_rain >= 1500.0 or effective_drainage == "slow_draining":
        heavy_rain_risk_level = "moderate"
        heavy_rain_en = "Moderate excess-moisture risk during peak rainy months; avoid low pockets for sensitive pulses and oilseeds."
        heavy_rain_kn = "ಅಧಿಕ ಮಳೆ ತಿಂಗಳುಗಳಲ್ಲಿ ತಗ್ಗು ಭಾಗದಲ್ಲಿ ದ್ವಿದಳ ಧಾನ್ಯ ಮತ್ತು ಎಣ್ಣೆಕಾಳು ಬೆಳೆಗಳಿಗೆ ಎಚ್ಚರಿಕೆ ಅಗತ್ಯ."
    else:
        heavy_rain_risk_level = "low"
        heavy_rain_en = "Low flood risk under normal dry-zone rainfall, though sudden cloudbursts still require field bund outlets."
        heavy_rain_kn = "ಸಾಮಾನ್ಯ ಒಣ ವಲಯದಲ್ಲಿ ನೀರು ನಿಲ್ಲುವ ಅಪಾಯ ಕಡಿಮೆ; ಆದರೂ ಬದುಗಳಲ್ಲಿ ಹೊರಹರಿವು ಇರಲಿ."

    # Dry spell risk assessment
    if water_source == "rainfed" and (
        season in ("Rabi", "Zaid") or annual_rain < 700.0 or soil_observation.get("effective_moisture_retention") in ("low_retention", "likely_low_retention")
    ):
        dry_spell_risk_level = "high"
        dry_spell_en = "High dry-spell sensitivity: rainfed sandy/shallow soil or post-monsoon dry window can stress crops at flowering/grain-fill."
        dry_spell_kn = "ಬರ/ಒಣ ಹವಾಮಾನದ ಅಪಾಯ ಹೆಚ್ಚು: ಮಳೆಯಾಶ್ರಿತ ಅಥವಾ ಬೇಗ ಒಣಗುವ ಮಣ್ಣಿನಲ್ಲಿ ಹೂಬಿಡುವ ಹಂತದಲ್ಲಿ ನೀರಿನ ಕೊರತೆ ಬರಬಹುದು."
    elif water_reliability in ("limited", "uncertain"):
        dry_spell_risk_level = "moderate"
        dry_spell_en = "Moderate dry-spell exposure because irrigation is limited or uncertain; prioritize drought-hardy or short-duration crops."
        dry_spell_kn = "ನೀರಾವರಿ ಸೀಮಿತವಾಗಿರುವುದರಿಂದ ಕಡಿಮೆ ನೀರು ಮತ್ತು ಕಡಿಮೆ ಅವಧಿಯ ಬೆಳೆಗಳಿಗೆ ಆದ್ಯತೆ ನೀಡಿ."
    else:
        dry_spell_risk_level = "low"
        dry_spell_en = "Lower dry-spell vulnerability when irrigation supply remains dependable during critical stages."
        dry_spell_kn = "ನೀರಾವರಿ ಲಭ್ಯತೆ ಸ್ಥಿರವಾಗಿದ್ದರೆ ಒಣ ಹವಾಮಾನದ ಅಪಾಯ ಕಡಿಮೆ ಇರುತ್ತದೆ."

    # Sowing suitability assessment
    if not live_available:
        sowing_suitability_en = f"Based on long-term {season} zone climate normals ({season_normal['temp_c']} C avg, {season_rain:.0f} mm seasonal normal){' and planned month ' + intended_sowing_month if intended_sowing_month else ''}, sow only after confirming local 5-day rain forecast and top-15cm soil moisture."
        sowing_suitability_kn = f"ದೀರ್ಘಕಾಲೀನ {season} ವಲಯದ ಸರಾಸರಿ ಪ್ರಕಾರ, ಸ್ಥಳೀಯ 5-ದಿನಗಳ ಮಳೆ ಮುನ್ಸೂಚನೆ ಮತ್ತು ಮಣ್ಣಿನ ತೇವಾಂಶ ಖಚಿತಪಡಿಸಿಕೊಂಡ ನಂತರವೇ ಬಿತ್ತನೆ ಮಾಡಿ."
    elif (short_term_forecast.get("peak_daily_rain_mm") or 0.0) >= 60.0:
        sowing_suitability_en = f"Delay dryland seed sowing if intense rain ({short_term_forecast['peak_daily_rain_mm']} mm/day forecast) can wash out newly sown seed; wait for drainage."
        sowing_suitability_kn = "ಮುಂದಿನ ದಿನಗಳಲ್ಲಿ ಭಾರಿ ಮಳೆ ಮುನ್ಸೂಚನೆ ಇರುವುದರಿಂದ ಬೀಜ ಕೊಚ್ಚಿಹೋಗದಂತೆ ಸ್ವಲ್ಪ ತಡೆದು ಬಿತ್ತನೆ ಮಾಡುವುದು ಉತ್ತಮ."
    else:
        sowing_suitability_en = f"District 7-day forecast shows moderate conditions ({short_term_forecast.get('next_7_days_rain_total_mm')} mm total rain expected); verify topsoil moisture before sowing."
        sowing_suitability_kn = "ಮುಂದಿನ 7 ದಿನಗಳ ಹವಾಮಾನ ಸಾಮಾನ್ಯವಾಗಿದೆ; ಮಣ್ಣಿನ ಮೇಲ್ಪದರದ ತೇವಾಂಶ ನೋಡಿ ಬಿತ್ತನೆ ಕೈಗೊಳ್ಳಿ."

    # Irrigation planning guidance
    if water_source == "rainfed":
        irrigation_en = "Rainfed field: adopt contour conservation furrows, organic mulching, and wide-row intercultivation to hold soil moisture."
        irrigation_kn = "ಮಳೆಯಾಶ್ರಿತ ಜಮೀನು: ತೇವಾಂಶ ಉಳಿಸಲು ಹರಿ ತೆಗೆಯುವುದು, ಸಾವಯವ ಹೊದಿಕೆ ಮತ್ತು ಎಡೆಕುಂಟೆ ಕ್ರಮ ಅನುಸರಿಸಿ."
    elif water_source == "drip_irrigation":
        irrigation_en = "Drip irrigation helps target scarce water directly to roots during dry spells; avoid over-wetting clay soils."
        irrigation_kn = "ಹನಿ ನೀರಾವರಿ ಮೂಲಕ ನೀರನ್ನು ಮಿತವಾಗಿ ಬೇರುಗಳಿಗೆ ನೀಡಬಹುದು; ಜೇಡಿ ಮಣ್ಣಿನಲ್ಲಿ ಅಧಿಕ ತೇವಾಂಶ ತಪ್ಪಿಸಿ."
    else:
        irrigation_en = "Apply protective irrigation especially at vegetative establishment and flowering/pod-filling stages; avoid irrigation before forecast rain."
        irrigation_kn = "ಮೊಳಕೆ, ಹೂಬಿಡುವ ಮತ್ತು ಕಾಳು ಕಟ್ಟುವ ನಿರ್ಣಾಯಕ ಹಂತಗಳಲ್ಲಿ ಮಾತ್ರ ಸಂರಕ್ಷಣಾ ನೀರಾವರಿ ನೀಡಿ; ಮಳೆ ಮುನ್ಸೂಚನೆ ಇದ್ದಾಗ ನೀರಾವರಿ ತಪ್ಪಿಸಿ."

    return {
        "long_term_climate": long_term_climate,
        "current_weather": current_weather,
        "short_term_forecast": short_term_forecast,
        "seasonal_outlook": seasonal_outlook,
        "farming_advisory": {
            "advisory_basis": "live_forecast_plus_zone_normals" if live_available else "zone_climate_normals_only_live_unavailable",
            "live_weather_available": live_available,
            "sowing_suitability_en": sowing_suitability_en,
            "sowing_suitability_kn": sowing_suitability_kn,
            "heavy_rainfall_risk_level": heavy_rain_risk_level,
            "heavy_rainfall_risk_en": heavy_rain_en,
            "heavy_rainfall_risk_kn": heavy_rain_kn,
            "dry_spell_risk_level": dry_spell_risk_level,
            "dry_spell_risk_en": dry_spell_en,
            "dry_spell_risk_kn": dry_spell_kn,
            "irrigation_planning_en": irrigation_en,
            "irrigation_planning_kn": irrigation_kn,
        },
    }
