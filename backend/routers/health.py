"""Health check endpoint verifying database and observation engine readiness."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Crop, KnowledgeArticle, Location, Recommendation
from backend.schemas import HealthResponse

router = APIRouter(prefix="/api", tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)) -> HealthResponse:
    db_ok = True
    counts = {"locations": 0, "crops": 0, "knowledge_articles": 0, "recommendations": 0}
    try:
        db.execute(text("SELECT 1"))
        counts["locations"] = db.query(Location).count()
        counts["crops"] = db.query(Crop).filter(Crop.is_active.is_(True)).count()
        counts["knowledge_articles"] = db.query(KnowledgeArticle).filter(KnowledgeArticle.is_published.is_(True)).count()
        counts["recommendations"] = db.query(Recommendation).count()
    except Exception:
        db_ok = False

    overall = "ok" if db_ok else "degraded"
    return HealthResponse(
        status=overall,
        service="SmartKrishi API",
        engine_mode="observation_rule_based",
        database_connected=db_ok,
        ml_model_loaded=False,
        ml_model_version="observation-rules-v2.0",
        record_counts=counts,
    )
