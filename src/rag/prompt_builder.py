"""
PromptBuilder: Assembles prompts for healthcare-compliant RAG.
"""
from typing import List, Dict, Any

class PromptBuilder:
    def __init__(self, template: str = None):
        self.template = template or (
            """You are a healthcare assistant. Use the following context to answer the user's question.\n\n"
            "Context:\n{context}\n\nQuestion: {question}\n\nCite sources in your answer."
        )

    def build(self, question: str, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Build a prompt from the user question and retrieved context.
        Args:
            question (str): User's question.
            context_chunks (List[Dict[str, Any]]): Retrieved context (e.g., from Retriever).
        Returns:
            str: Assembled prompt.
        """
        context_str = "\n---\n".join(
            f"Source: {chunk['metadata'].get('source', 'N/A')}\n{chunk['metadata'].get('text', '')}"
            for chunk in context_chunks
        )
        return self.template.format(context=context_str, question=question)
