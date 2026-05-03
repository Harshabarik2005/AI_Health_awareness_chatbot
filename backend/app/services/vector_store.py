"""
Vector Store Manager — ChromaDB Wrapper
========================================
Manages the ChromaDB vector database lifecycle:
  • Initialization and connection
  • Collection creation and access
  • Health checks for the /health endpoint

All data stays local on disk — no cloud vector DB services.
"""

import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import get_settings

# Module-level singleton
_client: chromadb.ClientAPI | None = None
_collection: chromadb.Collection | None = None

COLLECTION_NAME = "health_documents"


def get_chroma_client() -> chromadb.ClientAPI:
    """
    Return a persistent ChromaDB client (singleton).

    The database is stored at the path specified by CHROMA_PERSIST_DIR
    in the environment configuration.
    """
    global _client
    if _client is None:
        settings = get_settings()
        _client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
    return _client


def get_collection() -> chromadb.Collection:
    """
    Return the health documents collection, creating it if needed.

    Uses ChromaDB's default embedding function (all-MiniLM-L6-v2)
    which runs locally via sentence-transformers.
    """
    global _collection
    if _collection is None:
        client = get_chroma_client()
        _collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={
                "description": "Verified public health guidelines from WHO/CDC",
                "hnsw:space": "cosine",
            },
        )
    return _collection


def check_vector_db_health() -> dict[str, str]:
    """
    Check the vector database connectivity and return status info.

    Returns
    -------
    dict
        Keys: 'status', 'collection', 'document_count'
    """
    try:
        collection = get_collection()
        count = collection.count()
        return {
            "status": "operational",
            "collection": COLLECTION_NAME,
            "document_count": str(count),
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
        }
