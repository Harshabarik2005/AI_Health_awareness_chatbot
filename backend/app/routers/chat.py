"""
Chat Router — RAG-Powered Chat Endpoint
========================================
Handles the full pipeline:
  Request -> PII Sanitization -> Retrieve -> Generate -> Respond

Retrieval is local. Generation is handled by the configured Groq model.
"""

from fastapi import APIRouter, Query
from app.schemas import ChatRequest, ChatResponse, SourceDocument
from app.services.pii_sanitizer import sanitize_query
from app.services.retrieval import retrieve_context, format_context_for_prompt
from app.services.llm import generate_response

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with HealthAware AI",
    description=(
        "Submit a health-related question. The system retrieves relevant "
        "verified public health documents and generates a grounded response "
        "using Groq cloud language generation after sanitizing personal information."
    ),
)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Full chat pipeline.

    Phase 2: PII sanitization + retrieval are active.
    PII sanitization, retrieval, and cloud LLM generation are active.
    """
    # Step 1: Sanitize PII from the query
    sanitized = sanitize_query(request.query)

    # Step 2: Retrieve relevant context from the vector store
    chunks = retrieve_context(sanitized.cleaned_text)

    # Step 3: Format context for the cloud LLM prompt
    context_block = format_context_for_prompt(chunks)

    # Step 4: Build sources list for the response
    sources = [
        SourceDocument(
            title=chunk.source,
            content_snippet=chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content,
            relevance_score=chunk.relevance_score,
        )
        for chunk in chunks
    ]

    # Step 5: Generate response
    if not chunks:
        answer = (
            "I don't have verified information on this topic in my knowledge base. "
            "Please consult a healthcare professional or visit WHO (who.int) or CDC (cdc.gov) "
            "for reliable health information."
        )
    else:
        answer = await generate_response(
            query=sanitized.cleaned_text, 
            context=context_block
        )

    return ChatResponse(
        answer=answer,
        sources=sources,
    )


@router.get(
    "/search",
    summary="Search Knowledge Base",
    description="Test endpoint to search the vector database directly and view retrieved chunks.",
)
async def search_knowledge_base(
    q: str = Query(..., min_length=1, description="Search query"),
    top_k: int = Query(default=3, ge=1, le=10, description="Number of results"),
):
    """
    Debug / test endpoint for verifying retrieval quality.
    Returns raw retrieved chunks with scores.
    """
    chunks = retrieve_context(q, top_k=top_k)

    return {
        "query": q,
        "results_count": len(chunks),
        "results": [
            {
                "chunk_id": c.chunk_id,
                "source": c.source,
                "relevance_score": c.relevance_score,
                "content": c.content,
            }
            for c in chunks
        ],
    }
