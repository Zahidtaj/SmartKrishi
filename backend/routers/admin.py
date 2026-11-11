"""Protected Administrative routes for crops, regional rules, knowledge articles, datasets, and feedback."""

import json
from pathlib import Path
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import AdminUser, Crop, Feedback, KnowledgeArticle, Recommendation, RegionalCropRule
from backend.schemas import (
    AdminArticleCreateRequest,
    AdminCropUpdateRequest,
    AdminFeedbackUpdateRequest,
    AdminLoginRequest,
    AdminLoginResponse,
    AdminRuleCreateRequest,
)
from backend.security import create_access_token, require_admin, verify_password
from ml.config import PROVENANCE_PATH, VALIDATION_REPORT_PATH

router = APIRouter(prefix="/api/admin", tags=["Administration"])


@router.post("/login", response_model=AdminLoginResponse)
def admin_login(payload: AdminLoginRequest, db: Session = Depends(get_db)) -> AdminLoginResponse:
    user = db.query(AdminUser).filter(AdminUser.username == payload.username.strip()).first()
    if user is None or not user.is_active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid administrator username or password.",
        )
    token = create_access_token(user.username, user.role)
    return AdminLoginResponse(
        access_token=token,
        username=user.username,
        role=user.role,
        local_dev_notice="Local development administrator token (PBKDF2-SHA256 verified); not configured for public production deployment.",
    )


@router.get("/overview")
def admin_overview(
    request: Request,
    admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    predictor = getattr(request.app.state, "predictor", None)
    metrics = predictor.get_metrics() if predictor else None
    provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8")) if Path(PROVENANCE_PATH).exists() else {}
    validation = json.loads(VALIDATION_REPORT_PATH.read_text(encoding="utf-8")) if Path(VALIDATION_REPORT_PATH).exists() else {}

    recent_recs = db.query(Recommendation).order_by(Recommendation.created_at.desc()).limit(20).all()
    feedback_rows = db.query(Feedback).order_by(Feedback.created_at.desc()).limit(30).all()
    rules = db.query(RegionalCropRule).order_by(RegionalCropRule.id.desc()).limit(50).all()

    return {
        "admin_username": admin.username,
        "dataset_provenance": provenance,
        "dataset_validation": validation,
        "ml_metrics": metrics,
        "recent_recommendations": [
            {
                "id": r.id,
                "mode_used": r.mode_used,
                "confidence_level": r.confidence_level,
                "district": (r.input_snapshot or {}).get("district"),
                "season": (r.input_snapshot or {}).get("season"),
                "created_at": r.created_at,
            }
            for r in recent_recs
        ],
        "feedback": [
            {
                "id": f.id,
                "category": f.category,
                "rating": f.rating,
                "district": f.district,
                "comment": f.comment,
                "review_status": f.review_status,
                "admin_notes": f.admin_notes,
                "created_at": f.created_at,
            }
            for f in feedback_rows
        ],
        "regional_rules": [
            {
                "id": rule.id,
                "crop_id": rule.crop_id,
                "state": rule.state,
                "agro_climatic_zone": rule.agro_climatic_zone,
                "season": rule.season,
                "suitability_level": rule.suitability_level,
                "rule_notes_en": rule.rule_notes_en,
                "source": rule.source,
                "is_active": rule.is_active,
            }
            for rule in rules
        ],
    }


@router.patch("/crops/{crop_id}")
def update_crop(
    crop_id: int,
    payload: AdminCropUpdateRequest,
    _admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if crop is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found.")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(crop, field, value)
    db.commit()
    db.refresh(crop)
    return {"id": crop.id, "name_en": crop.name_en, "is_active": crop.is_active}


@router.post("/rules", status_code=status.HTTP_201_CREATED)
def create_regional_rule(
    payload: AdminRuleCreateRequest,
    _admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    crop = db.query(Crop).filter(Crop.id == payload.crop_id).first()
    if crop is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target crop not found.")
    rule = RegionalCropRule(**payload.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return {"id": rule.id, "crop_id": rule.crop_id, "suitability_level": rule.suitability_level}


@router.post("/knowledge", status_code=status.HTTP_201_CREATED)
def create_knowledge_article(
    payload: AdminArticleCreateRequest,
    _admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    existing = db.query(KnowledgeArticle).filter(KnowledgeArticle.slug == payload.slug).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Article slug already exists.")
    article = KnowledgeArticle(**payload.model_dump(), is_published=True)
    db.add(article)
    db.commit()
    db.refresh(article)
    return {"id": article.id, "slug": article.slug, "title_en": article.title_en}


@router.patch("/feedback/{feedback_id}")
def review_feedback(
    feedback_id: int,
    payload: AdminFeedbackUpdateRequest,
    _admin: AdminUser = Depends(require_admin),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    fb = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if fb is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback record not found.")
    fb.review_status = payload.review_status
    fb.admin_notes = payload.admin_notes
    db.commit()
    db.refresh(fb)
    return {"id": fb.id, "review_status": fb.review_status, "admin_notes": fb.admin_notes}
