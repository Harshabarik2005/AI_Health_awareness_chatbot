"""
PII Sanitizer — Privacy-First Input Processing
================================================
Strips personally identifiable information (PII) from user queries
before they reach the retrieval or inference engines.
"""

import re
from typing import NamedTuple

class SanitizationResult(NamedTuple):
    cleaned_text: str
    pii_detected: bool
    categories_found: list[str]

_PII_PATTERNS: dict[str, re.Pattern] = {
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    "phone": re.compile(r"(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit_card": re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),
    "ip_address": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
}

_REPLACEMENT = "[REDACTED]"

def sanitize_query(text: str) -> SanitizationResult:
    cleaned = text
    categories: list[str] = []

    for category, pattern in _PII_PATTERNS.items():
        if pattern.search(cleaned):
            categories.append(category)
            cleaned = pattern.sub(_REPLACEMENT, cleaned)

    return SanitizationResult(
        cleaned_text=cleaned.strip(),
        pii_detected=len(categories) > 0,
        categories_found=categories,
    )
