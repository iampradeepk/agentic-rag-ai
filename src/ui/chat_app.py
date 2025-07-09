"""
Streamlit Chat Interface for LLMinate RAG AI.
"""
import streamlit as st
from src.agents.agent_rag import RAGAgent
from src.agents.agent_mcp import MCPAgent

class ChatInterface:
    def __init__(self):
        self.rag_agent = RAGAgent()
        self.mcp_agent = MCPAgent()

    def render_chat_interface(self):
        st.title("Healthcare AI Assistant")
        selected_agent = st.selectbox(
            "Select Agent",
            ["RAG Agent (Document Q&A)", "MCP Agent (JIRA/Confluence)"]
        )
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        if prompt := st.chat_input("Ask a question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            if selected_agent.startswith("RAG"):
                response = self.process_rag_query(prompt)
            else:
                response = self.process_mcp_query(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)

    def process_rag_query(self, query: str) -> str:
        # Synchronous wrapper for demo; in production, use asyncio
        import asyncio
        context = self._get_rag_context()
        response = asyncio.run(self.rag_agent.process_query(query, context))
        return response.answer

    def process_mcp_query(self, query: str) -> str:
        import asyncio
        context = self._get_mcp_context()
        response = asyncio.run(self.mcp_agent.process_action("manual", {}, context))
        return response.message

    def _get_rag_context(self):
        return self.rag_agent.agent.result_type(
            user_id="demo_user",
            session_id="demo_session",
            conversation_history=[]
        )

    def _get_mcp_context(self):
        return self.mcp_agent.agent.result_type(
            user_id="demo_user",
            session_id="demo_session",
            available_tools=[]
        )
