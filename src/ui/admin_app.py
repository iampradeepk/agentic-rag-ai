"""
Streamlit Admin Interface for LLMinate RAG AI.
"""
import streamlit as st
import pandas as pd
from src.embeddings.vector_store import VectorStore

class AdminInterface:
    def __init__(self):
        self.vector_store = VectorStore()

    def render_admin_interface(self):
        st.title("Healthcare AI Admin Dashboard")
        page = st.sidebar.selectbox(
            "Navigation",
            ["Document Management", "Agent Configuration", "Audit Logs", "User Management"]
        )
        if page == "Document Management":
            self.render_document_management()
        elif page == "Agent Configuration":
            st.info("Agent Configuration coming soon.")
        elif page == "Audit Logs":
            st.info("Audit Logs coming soon.")
        elif page == "User Management":
            st.info("User Management coming soon.")

    def render_document_management(self):
        st.header("Document Management")
        st.subheader("Upload Documents")
        uploaded_files = st.file_uploader(
            "Upload PDF documents",
            type=['pdf'],
            accept_multiple_files=True
        )
        if uploaded_files:
            for file in uploaded_files:
                if st.button(f"Process {file.name}"):
                    self.process_document(file)
        st.subheader("Existing Documents")
        documents = self.get_documents()
        if documents:
            df = pd.DataFrame(documents)
            st.dataframe(df)

    def process_document(self, file):
        """Process uploaded document and ingest to RAG pipeline."""
        from src.rag.pipeline import RAGPipeline
        from src.core.config import Config
        import tempfile
        config = Config()
        rag_pipeline = RAGPipeline(config)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name
        try:
            result = rag_pipeline.ingest_document(tmp_path, file.name)
            st.success(f"Document '{file.name}' ingested: {result}")
        except Exception as e:
            st.error(f"Failed to ingest document: {e}")

    def get_documents(self):
        from src.embeddings.vector_store import VectorStore
        vs = VectorStore()
        return vs.list_documents()
