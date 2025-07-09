"""
Document ingestion pipeline: Extracts, chunks, embeds, and stores documents.
"""
import os
from typing import List, Dict, Any
from pypdf import PdfReader
from src.embeddings.bedrock_client import BedrockClient
from src.embeddings.vector_store import VectorStore
from datetime import datetime

CHUNK_SIZE = 500  # characters
CHUNK_OVERLAP = 100  # characters


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Split text into overlapping chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text from a PDF file.
    """
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def ingest_pdf(pdf_path: str, agent_id: int, vector_store: VectorStore, bedrock_client: BedrockClient):
    """
    Ingest a PDF: extract, chunk, embed, and store in DB.
    """
    # 1. Extract text
    text = extract_text_from_pdf(pdf_path)
    # 2. Chunk text
    chunks = chunk_text(text)
    # 3. Generate embeddings (sync for now, adapt to async if needed)
    import asyncio
    embeddings = asyncio.run(bedrock_client.generate_embeddings(chunks))
    # 4. Store in DB
    metadatas = [{"source": pdf_path, "text": chunk, "ingested_at": datetime.utcnow().isoformat()} for chunk in chunks]
    # Insert document record (simplified, assumes doc_id is auto-incremented)
    # You may want to use SQLAlchemy ORM for more robust handling
    doc_id = None
    with vector_store.engine.begin() as conn:
        result = conn.execute(
            """
            INSERT INTO documents (agent_id, source_filename, uploaded_at)
            VALUES (:agent_id, :source_filename, :uploaded_at)
            RETURNING doc_id
            """,
            {"agent_id": agent_id, "source_filename": os.path.basename(pdf_path), "uploaded_at": datetime.utcnow()}
        )
        doc_id = result.scalar()
    vector_store.store_embeddings(doc_id, agent_id, embeddings, metadatas)
    print(f"Ingested {pdf_path} as doc_id={doc_id} with {len(chunks)} chunks.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ingest a PDF document.")
    parser.add_argument("pdf_path", type=str, help="Path to PDF file")
    parser.add_argument("agent_id", type=int, help="Agent ID")
    args = parser.parse_args()

    vector_store = VectorStore()
    bedrock_client = BedrockClient()
    ingest_pdf(args.pdf_path, args.agent_id, vector_store, bedrock_client)
