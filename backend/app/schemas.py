"""
Pydantic Schemas — Request & Response Models
=============================================
Defines the data contracts for the API. These models enforce
input validation and provide clear response structures.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ── Chat Request / Response ─────────────────────────────────


class ChatRequest(BaseModel):
    """Incoming user query to the chatbot."""

    query: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The user's health-related question or symptom description.",
        examples=["What are the symptoms of dengue fever?"],
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Optional session identifier for conversation continuity.",
    )


class SourceDocument(BaseModel):
    """A single retrieved source document used to ground the response."""

    title: str
    content_snippet: str
    relevance_score: float = Field(ge=0.0, le=1.0)


class ChatResponse(BaseModel):
    """Structured response returned by the chatbot API."""

    answer: str = Field(
        description="The AI-generated response grounded in verified health documents."
    )
    sources: list[SourceDocument] = Field(
        default_factory=list,
        description="List of source documents used to generate the answer.",
    )
    disclaimer: str = Field(
        default=(
            "⚕️ I am an AI providing public health information, not a doctor. "
            "Please consult a healthcare professional for medical advice."
        ),
        description="Mandatory medical disclaimer appended to every response.",
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ── Health Check ────────────────────────────────────────────


class HealthCheckResponse(BaseModel):
    """Response model for the health-check endpoint."""

    status: str = "healthy"
    version: str
    environment: str
    services: dict[str, str] = Field(default_factory=dict)
