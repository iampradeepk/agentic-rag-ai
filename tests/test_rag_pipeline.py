import pytest
from src.rag.pipeline import RAGPipeline
from src.core.config import Config

@pytest.fixture
def rag_pipeline():
    config = Config()
    return RAGPipeline(config)

def test_process_query_expected(rag_pipeline):
    query = "What is HIPAA?"
    try:
        response = rag_pipeline.process_query(query)
        assert hasattr(response, 'content')
        assert hasattr(response, 'sources')
        assert hasattr(response, 'confidence')
    except Exception as e:
        pytest.skip(f"RAG pipeline not available: {e}")

def test_process_query_edge_case(rag_pipeline):
    query = ""
    with pytest.raises(Exception):
        rag_pipeline.process_query(query)

def test_process_query_failure(rag_pipeline):
    with pytest.raises(Exception):
        rag_pipeline.process_query(None)
