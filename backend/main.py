"""FastAPI application entry point for HealthAware AI."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.routers import chat, health


def _parse_cors_origins(raw_origins: str) -> list[str]:
    """Parse comma-separated CORS origins from settings."""
    origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    return origins or ["http://localhost:5173"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown hooks."""
    settings = get_settings()
    print(f"\n[+] {settings.app_name} v{settings.app_version}")
    print(f"    Environment : {settings.app_env}")
    print(f"    Groq Model  : {settings.groq_model}")
    print(f"    Vector DB   : {settings.chroma_persist_dir}")
    print(f"    Docs        : http://{settings.app_host}:{settings.app_port}/docs\n")
    yield
    print(f"\n[*] {settings.app_name} shutting down.\n")


def create_app() -> FastAPI:
    """Build and return the configured FastAPI application."""
    settings = get_settings()
    cors_origins = _parse_cors_origins(settings.cors_origins)

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "An AI-driven chatbot for public health awareness, powered by "
            "local retrieval and Groq cloud language generation. Personal "
            "information is sanitized before prompts are sent to the model."
        ),
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials="*" not in cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(chat.router)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=(settings.app_env == "development"),
    )
