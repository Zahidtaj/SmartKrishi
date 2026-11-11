"""Crop comparison service scaling documented agronomic and illustrative economic data."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from backend.models import Crop
from backend.schemas import CompareCropsRequest, CompareCropsResponse, ComparedCropItem

COMPARE_DISCLAIMER_EN = (
    "Economic values (where available) are prototype illustrative baselines scaled linearly by land area "
    "under stated assumptions. They do not guarantee market prices, yields, or net profits."
)
COMPARE_DISCLAIMER_KN = (
    "ಆರ್ಥಿಕ ಅಂಕಿಅಂಶಗಳು (ಲಭ್ಯವಿರುವಲ್ಲಿ) ದಾಖಲಿತ ಊಹೆಗಳ ಅಡಿಯಲ್ಲಿ ಜಮೀನು ವಿಸ್ತೀರ್ಣಕ್ಕೆ ಅನುಗುಣವಾಗಿ ತೋರಿಸಲಾದ "
    "ಪ್ರೋಟೋಟೈಪ್ ಮಾದರಿ ಅಂದಾಜುಗಳಾಗಿವೆ; ಇವು ಮಾರುಕಟ್ಟೆ ಬೆಲೆ ಅಥವಾ ಲಾಭದ ಖಾತರಿಯಲ್ಲ."
)


def compare_crops(db: Session, payload: CompareCropsRequest) -> CompareCropsResponse:
    """Compare up to 3 crops side by side across agronomy and economic baselines."""
    unique_ids = list(dict.fromkeys(payload.crop_ids))
    crops = (
        db.query(Crop)
        .options(joinedload(Crop.requirement), joinedload(Crop.economic_data))
        .filter(Crop.id.in_(unique_ids), Crop.is_active.is_(True))
        .all()
    )
    crop_by_id = {c.id: c for c in crops}
    missing = [cid for cid in unique_ids if cid not in crop_by_id]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Requested crop ID(s) not found: {missing}",
        )

    acres = payload.land_area_acres
    items: list[ComparedCropItem] = []
    for cid in unique_ids:
        crop = crop_by_id[cid]
        req = crop.requirement
        econ = crop.economic_data[0] if crop.economic_data else None

        seed_cost = round(econ.seed_cost_inr_per_acre * acres, 0) if econ and econ.seed_cost_inr_per_acre is not None else None
        cost_min = round(econ.cultivation_cost_min_inr_per_acre * acres, 0) if econ and econ.cultivation_cost_min_inr_per_acre is not None else None
        cost_max = round(econ.cultivation_cost_max_inr_per_acre * acres, 0) if econ and econ.cultivation_cost_max_inr_per_acre is not None else None
        yield_min = round(econ.expected_yield_qtl_min * acres, 2) if econ and econ.expected_yield_qtl_min is not None else None
        yield_max = round(econ.expected_yield_qtl_max * acres, 2) if econ and econ.expected_yield_qtl_max is not None else None
        price = econ.indicative_price_inr_per_qtl if econ else None

        gross_min = round(yield_min * price, 0) if yield_min is not None and price is not None else None
        gross_max = round(yield_max * price, 0) if yield_max is not None and price is not None else None
        net_min = round(gross_min - cost_max, 0) if gross_min is not None and cost_max is not None else None
        net_max = round(gross_max - cost_min, 0) if gross_max is not None and cost_min is not None else None

        economic_available = cost_min is not None and yield_min is not None and price is not None

        items.append(
            ComparedCropItem(
                crop_id=crop.id,
                crop_key=crop.crop_key,
                name_en=crop.name_en,
                name_kn=crop.name_kn,
                category=crop.category,
                image_asset=crop.image_asset,
                suitable_soil_types=req.suitable_soil_types if req else [],
                ph_range=f"{req.ph_min:.1f} - {req.ph_max:.1f}" if req else "Unavailable",
                water_requirement_level=crop.water_requirement_level,
                water_requirement_mm_range=f"{crop.water_requirement_mm_min}-{crop.water_requirement_mm_max} mm",
                suitable_seasons=req.suitable_seasons if req else [],
                growing_duration_days_range=f"{crop.growing_duration_days_min}-{crop.growing_duration_days_max} days",
                temperature_range_c=f"{req.temp_min_c:.0f}-{req.temp_max_c:.0f} °C" if req else "Unavailable",
                humidity_range_pct=f"{req.humidity_min_pct:.0f}-{req.humidity_max_pct:.0f}%" if req else "Unavailable",
                rainfall_range_mm=f"{req.rainfall_min_mm:.0f}-{req.rainfall_max_mm:.0f} mm" if req else "Unavailable",
                seed_rate_kg_per_acre=crop.seed_rate_kg_per_acre,
                economic_data_status=econ.data_status if econ else "unavailable",
                economic_available=economic_available,
                seed_cost_inr_total=seed_cost,
                cultivation_cost_min_total=cost_min,
                cultivation_cost_max_total=cost_max,
                expected_yield_qtl_min_total=yield_min,
                expected_yield_qtl_max_total=yield_max,
                indicative_price_inr_per_qtl=price,
                gross_revenue_min_total=gross_min,
                gross_revenue_max_total=gross_max,
                net_return_min_total=net_min,
                net_return_max_total=net_max,
                assumptions_en=econ.assumptions_en if econ else "Economic comparison data unavailable for this crop.",
                assumptions_kn=econ.assumptions_kn if econ else "ಈ ಬೆಳೆಗೆ ಆರ್ಥಿಕ ಹೋಲಿಕೆ ದತ್ತಾಂಶ ಲಭ್ಯವಿಲ್ಲ.",
                economic_source=econ.source if econ else None,
                information_source=crop.information_source,
            )
        )

    return CompareCropsResponse(
        land_area_acres=acres,
        disclaimer_en=COMPARE_DISCLAIMER_EN,
        disclaimer_kn=COMPARE_DISCLAIMER_KN,
        crops=items,
    )
