"""Recommendation generation and retrieval API routes."""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas import RecommendationRequest, RecommendationResponse
from backend.services.recommendation_service import generate_recommendation, get_recommendation_by_id
from ml.predictor import CropMLPredictor

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


def _get_predictor(request: Request) -> CropMLPredictor:
    predictor = getattr(request.app.state, "predictor", None)
    if predictor is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Recommendation ML engine is not initialized.",
        )
    return predictor


@router.post("", response_model=RecommendationResponse, status_code=status.HTTP_201_CREATED)
def create_recommendation(
    payload: RecommendationRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> RecommendationResponse:
    predictor = _get_predictor(request)
    return generate_recommendation(db=db, payload=payload, predictor=predictor)


@router.get("/{recommendation_id}", response_model=RecommendationResponse)
def read_recommendation(recommendation_id: int, db: Session = Depends(get_db)) -> RecommendationResponse:
    return get_recommendation_by_id(db=db, recommendation_id=recommendation_id)
