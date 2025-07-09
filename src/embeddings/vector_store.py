"""
VectorStore: pgvector-backed storage for document embeddings with agent isolation.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

class EmbeddingRecord(BaseModel):
    chunk_id: int
    doc_id: int
    agent_id: int
    vector: List[float]
    metadata: Dict[str, Any]

class VectorStore:
    def __init__(self, database_url: Optional[str] = None):
        self.engine: Engine = create_engine(database_url or DATABASE_URL)

    def store_embeddings(self, doc_id: int, agent_id: int, vectors: List[List[float]], metadatas: List[Dict[str, Any]]):
        """
        Store multiple embeddings for a document.
        Args:
            doc_id (int): Document ID.
            agent_id (int): Agent ID.
            vectors (List[List[float]]): List of embedding vectors.
            metadatas (List[Dict[str, Any]]): List of metadata dicts.
        """
        with self.engine.begin() as conn:
            for vector, metadata in zip(vectors, metadatas):
                conn.execute(
                    text("""
                        INSERT INTO embeddings (doc_id, agent_id, vector, metadata)
                        VALUES (:doc_id, :agent_id, :vector, :metadata)
                    """),
                    {"doc_id": doc_id, "agent_id": agent_id, "vector": vector, "metadata": metadata}
                )

    def similarity_search(self, agent_id: int, query_vector: List[float], top_k: int = 5) -> List[EmbeddingRecord]:
        """
        Retrieve top-k most similar embeddings for an agent.
        Args:
            agent_id (int): Agent ID to filter.
            query_vector (List[float]): Query embedding vector.
            top_k (int): Number of results to return.
        Returns:
            List[EmbeddingRecord]: Top-k similar embeddings.
        """
        with self.engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT chunk_id, doc_id, agent_id, vector, metadata
                    FROM embeddings
                    WHERE agent_id = :agent_id
                    ORDER BY vector <-> :query_vector
                    LIMIT :top_k
                """),
                {"agent_id": agent_id, "query_vector": query_vector, "top_k": top_k}
            )
            rows = result.fetchall()
            return [EmbeddingRecord(**dict(row)) for row in rows]

    def delete_agent_embeddings(self, agent_id: int):
        """
        Delete all embeddings for a given agent.
        Args:
            agent_id (int): Agent ID.
        """
        with self.engine.begin() as conn:
            conn.execute(
                text("DELETE FROM embeddings WHERE agent_id = :agent_id"),
                {"agent_id": agent_id}
            )
