"""
RAGPipeline: Orchestrates retrieval, prompt building, and LLM generation.
"""
from typing import List, Dict, Any
from src.rag.retriever import Retriever
from src.rag.prompt_builder import PromptBuilder
from src.embeddings.bedrock_client import BedrockClient

class RAGPipeline:
    def __init__(self, retriever: Retriever, prompt_builder: PromptBuilder, bedrock_client: BedrockClient):
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.bedrock_client = bedrock_client

    async def process_query(self, agent_id: int, question: str, query_vector: List[float], top_k: int = 5) -> Dict[str, Any]:
        """
        Full RAG pipeline: retrieve, build prompt, generate answer.
        Args:
            agent_id (int): Agent ID.
            question (str): User's question.
            query_vector (List[float]): Embedding of the question.
            top_k (int): Number of context chunks to retrieve.
        Returns:
            Dict[str, Any]: Answer, sources, confidence, metadata.
        """
        # 1. Retrieve context
        context_chunks = self.retriever.retrieve(agent_id, query_vector, top_k)
        # 2. Build prompt
        prompt = self.prompt_builder.build(question, [chunk.dict() for chunk in context_chunks])
        # 3. Generate answer
        answer = await self.bedrock_client.generate_completion(prompt)
        sources = [chunk.metadata.get('source', 'N/A') for chunk in context_chunks]
        return {
            "answer": answer,
            "sources": sources,
            "confidence": 1.0,  # Placeholder, can be improved
            "metadata": {}
        }
