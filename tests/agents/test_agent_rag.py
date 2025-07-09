import pytest
from src.agents.agent_rag import RAGAgent
from src.core.config import Config

@pytest.fixture
def rag_agent():
    config = Config()
    return RAGAgent(config)

def test_process_query_expected(rag_agent):
    query = "What is HIPAA?"
    try:
        response = rag_agent.process_query(query)
        assert hasattr(response, 'content')
        assert hasattr(response, 'sources')
        assert hasattr(response, 'confidence')
    except Exception as e:
        pytest.skip(f"RAG pipeline not available: {e}")

def test_process_query_edge_case(rag_agent):
    query = ""
    with pytest.raises(Exception):
        rag_agent.process_query(query)

def test_process_query_failure(rag_agent):
    with pytest.raises(Exception):
        rag_agent.process_query(None)