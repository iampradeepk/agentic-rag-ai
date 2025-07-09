"""
RAGAgent: Pydantic AI Agent wrapping the RAG pipeline.
"""
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from src.rag.pipeline import RAGPipeline
from src.rag.retriever import Retriever
from src.rag.prompt_builder import PromptBuilder
from src.embeddings.bedrock_client import BedrockClient
from src.embeddings.vector_store import VectorStore

class RAGContext(BaseModel):
    user_id: str
    session_id: str
    conversation_history: List[Dict[str, str]]

class RAGResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float
    metadata: Dict[str, Any]

class RAGAgent:
    def __init__(self):
        self.vector_store = VectorStore()
        self.retriever = Retriever(self.vector_store)
        self.prompt_builder = PromptBuilder()
        self.bedrock_client = BedrockClient()
        self.rag_pipeline = RAGPipeline(self.retriever, self.prompt_builder, self.bedrock_client)
        self.agent = Agent(
            model='bedrock:anthropic.claude-3-sonnet-20240229-v1:0',
            result_type=RAGResponse,
            system_prompt=self._get_system_prompt()
        )

    def _get_system_prompt(self) -> str:
        return (
            "You are a helpful AI assistant for healthcare professionals. "
            "You provide accurate, evidence-based information from medical documents. "
            "Always cite your sources and indicate confidence levels. "
            "Follow HIPAA guidelines and maintain patient privacy."
        )

    @staticmethod
    def _get_query_vector(question: str) -> List[float]:
        # Placeholder: In production, use BedrockClient to embed the question
        return [0.0] * 1536

    async def process_query(self, query: str, context: RAGContext) -> RAGResponse:
        """
        Process user query and return a RAGResponse.
        """
        # 1. Embed the query (replace with actual embedding logic)
        query_vector = self._get_query_vector(query)
        # 2. Use user_id as agent_id for isolation (customize as needed)
        agent_id = hash(context.user_id) % (2**31)
        result = await self.rag_pipeline.process_query(agent_id, query, query_vector)
        return RAGResponse(**result)
