"""Health check endpoint verifying database and ML artifact readiness."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Crop, KnowledgeArticle, Location, Recommendation
from backend.schemas import HealthResponse

router = APIRouter(prefix="/api", tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health_check(request: Request, db: Session = Depends(get_db)) -> HealthResponse:
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

    predictor = getattr(request.app.state, "predictor", None)
    ml_loaded = bool(predictor and predictor.is_loaded)
    metrics = predictor.get_metrics() if predictor else None
    ml_version = f"rf_acc_{metrics['test_accuracy']:.3f}" if metrics and "test_accuracy" in metrics else None

    overall = "ok" if db_ok and ml_loaded else "degraded"
    return HealthResponse(
        status=overall,
        service="SmartKrishi API",
        database_connected=db_ok,
        ml_model_loaded=ml_loaded,
        ml_model_version=ml_version,
        record_counts=counts,
    )
