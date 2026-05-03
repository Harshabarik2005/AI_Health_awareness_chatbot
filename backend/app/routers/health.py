"""System status and diagnostics endpoints."""

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.schemas import HealthCheckResponse
from app.services.llm import check_llm_health
from app.services.vector_store import check_vector_db_health

router = APIRouter(tags=["System"])


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Health Check",
    description="Returns the current health status of the API and its dependent services.",
)
async def health_check(
    settings: Settings = Depends(get_settings),
) -> HealthCheckResponse:
    """Return server status plus vector DB and Groq connectivity."""
    vdb_health = check_vector_db_health()
    llm_health = await check_llm_health()

    services: dict[str, str] = {
        "api": "operational",
        "vector_db": vdb_health.get("status", "unknown"),
        "vector_db_docs": vdb_health.get("document_count", "0"),
        "cloud_llm": llm_health.get("status", "unknown"),
        "llm_model": llm_health.get("model_loaded", settings.groq_model),
    }

    return HealthCheckResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.app_env,
        services=services,
    )


@router.get(
    "/",
    summary="Root",
    description="Welcome endpoint with basic API information.",
)
async def root(settings: Settings = Depends(get_settings)):
    """Landing page response with API metadata."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
    }
