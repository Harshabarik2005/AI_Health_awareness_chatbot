"""Application configuration for HealthAware AI."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Application-wide configuration loaded from environment variables."""

    # Server
    app_name: str = "HealthAware AI"
    app_version: str = "0.1.0"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_env: str = "development"
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    # Vector database
    chroma_persist_dir: str = "./data/chroma_db"

    # Cloud LLM service (Groq API)
    groq_api_key: str = ""
    groq_model: str = "llama-3.1-8b-instant"
    groq_timeout_seconds: float = 60.0

    # RAG settings
    embedding_model: str = "all-MiniLM-L6-v2"
    retrieval_top_k: int = 5
    chunk_size: int = 512
    chunk_overlap: int = 64

    model_config = {
        "env_file": str(BASE_DIR / ".env"),
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


@lru_cache()
def get_settings() -> Settings:
    """Return a cached singleton of the application settings."""
    return Settings()
