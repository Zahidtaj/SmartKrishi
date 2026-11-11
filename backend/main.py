"""FastAPI application entry point for SmartKrishi."""

from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from backend.config import get_settings
from backend.routers import admin, crops, health, knowledge, locations, recommendations
from backend.seed import initialize_and_seed
from ml.predictor import CropMLPredictor, ModelLoadError

logger = logging.getLogger("smartkrishi")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    initialize_and_seed()
    predictor = CropMLPredictor(artifacts_dir=settings.model_dir)
    try:
        predictor.load()
    except ModelLoadError as exc:
        logger.warning("ML model could not be loaded at startup: %s", exc)
    app.state.predictor = predictor
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="SmartKrishi API",
        version="1.0.0",
        description="Hybrid ML + Agronomic Rule-Based Crop Recommendation and Decision Support REST API.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_request: Request, exc: RequestValidationError):
        field_errors = {}
        for err in exc.errors():
            loc = ".".join(str(part) for part in err.get("loc", []) if part != "body")
            field_errors[loc or "request"] = err.get("msg", "Invalid input value")
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation Error",
                "detail": "One or more submitted fields are invalid or missing.",
                "code": "VALIDATION_ERROR",
                "field_errors": field_errors,
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "Request Error",
                "detail": str(exc.detail),
                "code": f"HTTP_{exc.status_code}",
                "field_errors": None,
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(_request: Request, exc: SQLAlchemyError):
        logger.exception("Database operation error: %s", exc)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Database Error",
                "detail": "A database operation failed safely without exposing internal details.",
                "code": "DATABASE_ERROR",
                "field_errors": None,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_request: Request, exc: Exception):
        logger.exception("Unhandled server error: %s", exc)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": "An unexpected server error occurred. Please try again.",
                "code": "INTERNAL_ERROR",
                "field_errors": None,
            },
        )

    app.include_router(health.router)
    app.include_router(locations.router)
    app.include_router(crops.router)
    app.include_router(recommendations.router)
    app.include_router(knowledge.soil_router)
    app.include_router(knowledge.knowledge_router)
    app.include_router(knowledge.feedback_router)
    app.include_router(admin.router)

    return app


app = create_app()
