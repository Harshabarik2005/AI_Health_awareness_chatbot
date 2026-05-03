"""
Retrieval Service — RAG Context Fetcher
========================================
Queries the ChromaDB vector store for the top-k most relevant
public health document chunks based on a user query.

Returns structured results that feed into the cloud LLM prompt.
"""

from dataclasses import dataclass
from app.services.vector_store import get_collection
from app.core.config import get_settings


@dataclass
class RetrievedChunk:
    """A single chunk retrieved from the vector database."""

    content: str
    source: str
    chunk_id: str
    relevance_score: float  # 0.0 = perfect match (distance), converted to similarity


def retrieve_context(query: str, top_k: int | None = None) -> list[RetrievedChunk]:
    """
    Retrieve the most relevant document chunks for a user query.

    Parameters
    ----------
    query : str
        The sanitized user query.
    top_k : int, optional
        Number of results to return. Defaults to config value.

    Returns
    -------
    list[RetrievedChunk]
        Ordered by relevance (highest similarity first).
        Returns an empty list if no relevant documents are found.
    """
    settings = get_settings()
    k = top_k or settings.retrieval_top_k

    collection = get_collection()

    # If the collection is empty, return nothing
    if collection.count() == 0:
        return []

    # Query ChromaDB — it handles embedding the query internally
    results = collection.query(
        query_texts=[query],
        n_results=min(k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    chunks: list[RetrievedChunk] = []

    if not results or not results["documents"] or not results["documents"][0]:
        return chunks

    documents = results["documents"][0]
    metadatas = results["metadatas"][0] if results["metadatas"] else [{}] * len(documents)
    distances = results["distances"][0] if results["distances"] else [0.0] * len(documents)
    ids = results["ids"][0] if results["ids"] else [""] * len(documents)

    for doc, meta, dist, chunk_id in zip(documents, metadatas, distances, ids):
        # ChromaDB cosine distance: 0 = identical, 2 = opposite
        # Convert to similarity score: 1 - (distance / 2)
        similarity = max(0.0, min(1.0, 1.0 - (dist / 2.0)))

        chunks.append(
            RetrievedChunk(
                content=doc,
                source=meta.get("source", "Unknown"),
                chunk_id=chunk_id,
                relevance_score=round(similarity, 4),
            )
        )

    return chunks


def format_context_for_prompt(chunks: list[RetrievedChunk]) -> str:
    """
    Format retrieved chunks into a string block for the cloud LLM prompt.

    Parameters
    ----------
    chunks : list[RetrievedChunk]
        Retrieved document chunks.

    Returns
    -------
    str
        A formatted context block, or a "no context" message if empty.
    """
    if not chunks:
        return "NO RELEVANT DOCUMENTS FOUND. You must inform the user that you do not have verified information on this topic."

    context_parts: list[str] = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(
            f"--- Source {i}: {chunk.source} (Relevance: {chunk.relevance_score:.0%}) ---\n"
            f"{chunk.content}\n"
        )

    return "\n".join(context_parts)
