"""
Retriever: Vector similarity search for RAG pipeline.
"""
from typing import List, Dict, Any
from src.embeddings.vector_store import VectorStore, EmbeddingRecord

class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def retrieve(self, agent_id: int, query_vector: List[float], top_k: int = 5) -> List[EmbeddingRecord]:
        """
        Retrieve top-k most similar document chunks for a given agent and query vector.
        Args:
            agent_id (int): Agent ID.
            query_vector (List[float]): Query embedding vector.
            top_k (int): Number of results to return.
        Returns:
            List[EmbeddingRecord]: Top-k similar document chunks.
        """
        return self.vector_store.similarity_search(agent_id, query_vector, top_k=top_k)
