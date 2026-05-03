"""
Document Ingestion Script
=========================
Reads all text files from `data/documents`, chunks them, and
ingests them into the ChromaDB vector store.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to sys.path so we can import app modules
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from app.services.vector_store import get_collection

DOCUMENTS_DIR = backend_dir / "data" / "documents"

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """Simple character-based chunking with overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def run_ingestion():
    collection = get_collection()
    
    if not DOCUMENTS_DIR.exists():
        print(f"Directory not found: {DOCUMENTS_DIR}")
        return
        
    for filepath in DOCUMENTS_DIR.glob("*.txt"):
        print(f"Processing: {filepath.name}...")
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        chunks = chunk_text(content)
        
        ids = [f"{filepath.stem}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": filepath.name} for _ in chunks]
        
        collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        print(f"  -> Added {len(chunks)} chunks.")
        
    print("\nIngestion complete!")
    print(f"Total chunks in Vector DB: {collection.count()}")

if __name__ == "__main__":
    run_ingestion()
