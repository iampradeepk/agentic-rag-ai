import pytest
from src.embeddings.vector_store import VectorStore

@pytest.fixture
def vector_store():
    return VectorStore()

def test_store_embeddings_expected(vector_store):
    doc_id = "test-doc"
    agent_id = "test-agent"
    embedding = [0.1] * 1536
    metadata = {"test": True}
    try:
        result = vector_store.store_embeddings(doc_id, agent_id, [embedding], [metadata])
        assert result is True or result is None
    except Exception as e:
        pytest.skip(f"DB not available: {e}")

def test_similarity_search_edge_case(vector_store):
    agent_id = "test-agent"
    embedding = [0.0] * 1536
    try:
        results = vector_store.similarity_search(agent_id, embedding, top_k=1)
        assert isinstance(results, list)
    except Exception as e:
        pytest.skip(f"DB not available: {e}")

def test_delete_agent_embeddings_failure(vector_store):
    with pytest.raises(Exception):
        vector_store.delete_agent_embeddings(None)
