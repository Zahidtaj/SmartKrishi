"""Recommendation generation and retrieval API routes."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas import RecommendationRequest, RecommendationResponse
from backend.services.recommendation_service import generate_recommendation, get_recommendation_by_id

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


@router.post("", response_model=RecommendationResponse, status_code=status.HTTP_201_CREATED)
def create_recommendation(
    payload: RecommendationRequest,
    db: Session = Depends(get_db),
) -> RecommendationResponse:
    return generate_recommendation(db=db, payload=payload)


@router.get("/{recommendation_id}", response_model=RecommendationResponse)
def read_recommendation(recommendation_id: int, db: Session = Depends(get_db)) -> RecommendationResponse:
    return get_recommendation_by_id(db=db, recommendation_id=recommendation_id)
