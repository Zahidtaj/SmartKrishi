"""Soil health analysis, Agricultural Knowledge Centre, and Feedback endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Feedback, KnowledgeArticle
from backend.schemas import (
    FeedbackCreateRequest,
    FeedbackResponse,
    KnowledgeArticleDetail,
    KnowledgeArticleSummary,
    SoilAnalysisRequest,
    SoilAnalysisResponse,
    SoilObservationRequest,
)
from backend.services.soil_health_service import analyze_soil_health
from backend.services.soil_observation_service import interpret_soil_observations

soil_router = APIRouter(prefix="/api/soil", tags=["Soil Health"])
knowledge_router = APIRouter(prefix="/api/knowledge", tags=["Knowledge Centre"])
feedback_router = APIRouter(prefix="/api/feedback", tags=["Feedback"])


@soil_router.post("/observe")
def observe_soil(payload: SoilObservationRequest) -> dict:
    return interpret_soil_observations(**payload.model_dump())


@soil_router.post("/analyze", response_model=SoilAnalysisResponse)
def analyze_soil(payload: SoilAnalysisRequest) -> SoilAnalysisResponse:
    return analyze_soil_health(payload)


@knowledge_router.get("", response_model=list[KnowledgeArticleSummary])
def list_knowledge_articles(
    category: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[KnowledgeArticleSummary]:
    query = db.query(KnowledgeArticle).filter(KnowledgeArticle.is_published.is_(True))
    if category and category.lower() != "all":
        query = query.filter(KnowledgeArticle.category == category.strip().lower())
    articles = query.order_by(KnowledgeArticle.id.asc()).all()

    if search and search.strip():
        q = search.strip().lower()
        articles = [
            a for a in articles
            if q in a.title_en.lower() or q in a.title_kn.lower() or q in a.summary_en.lower() or q in a.content_en.lower()
        ]

    return [
        KnowledgeArticleSummary(
            id=a.id,
            slug=a.slug,
            category=a.category,
            title_en=a.title_en,
            title_kn=a.title_kn,
            summary_en=a.summary_en,
            summary_kn=a.summary_kn,
            source_name=a.source_name,
            source_url=a.source_url,
            updated_at=a.updated_at,
        )
        for a in articles
    ]


@knowledge_router.get("/{article_id}", response_model=KnowledgeArticleDetail)
def get_knowledge_article(article_id: int, db: Session = Depends(get_db)) -> KnowledgeArticleDetail:
    article = (
        db.query(KnowledgeArticle)
        .filter(KnowledgeArticle.id == article_id, KnowledgeArticle.is_published.is_(True))
        .first()
    )
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Knowledge article not found.")
    return KnowledgeArticleDetail(
        id=article.id,
        slug=article.slug,
        category=article.category,
        title_en=article.title_en,
        title_kn=article.title_kn,
        summary_en=article.summary_en,
        summary_kn=article.summary_kn,
        content_en=article.content_en,
        content_kn=article.content_kn,
        source_name=article.source_name,
        source_url=article.source_url,
        updated_at=article.updated_at,
    )


@feedback_router.post("", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def submit_feedback(payload: FeedbackCreateRequest, db: Session = Depends(get_db)) -> FeedbackResponse:
    row = Feedback(
        recommendation_id=payload.recommendation_id,
        category=payload.category,
        rating=payload.rating,
        district=payload.district.strip() if payload.district else None,
        comment=payload.comment.strip(),
        review_status="pending",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return FeedbackResponse(
        id=row.id,
        category=row.category,
        rating=row.rating,
        district=row.district,
        comment=row.comment,
        review_status=row.review_status,
        created_at=row.created_at,
    )
