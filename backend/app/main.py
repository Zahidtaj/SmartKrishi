import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.core.config import settings
from backend.app.api.api import router as api_router
from backend.app.seed import seed_database

app = FastAPI(
    title=settings.PROJECT_TITLE,
    description="VTU Community Agricultural Decision Support System for Karnataka. Observation-based crop recommendations without laboratory NPK or pH tests.",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount REST API
app.include_router(api_router, prefix=settings.API_PREFIX)

@app.on_event("startup")
def startup_event():
    # Ensure database is seeded on startup
    try:
        seed_database()
    except Exception as e:
        print(f"Startup seed notice: {e}")

# Frontend static serving if dist exists
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="static_assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = FRONTEND_DIST / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIST / "index.html")
else:
    @app.get("/")
    def root():
        return {
            "project": "SmartKrishi",
            "tagline": "Observation-Based Smart Agricultural Decision Support System",
            "version": "1.0.0",
            "docs": "/docs",
            "api_health": "/api/health",
            "frontend_dev_server": "http://localhost:5173"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
