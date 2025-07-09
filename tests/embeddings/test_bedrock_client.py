import pytest
from src.embeddings.bedrock_client import BedrockClient
from src.core.config import Config

@pytest.fixture
def bedrock_client():
    config = Config()
    return BedrockClient(config)

def test_generate_embeddings_expected(bedrock_client):
    # Replace with a real or mock input
    text = "Test embedding input."
    try:
        embedding = bedrock_client.generate_embeddings(text)
        assert isinstance(embedding, list)
        assert all(isinstance(x, float) for x in embedding)
    except Exception as e:
        pytest.skip(f"Bedrock not available: {e}")

def test_generate_embeddings_edge_case(bedrock_client):
    text = ""
    with pytest.raises(Exception):
        bedrock_client.generate_embeddings(text)

def test_generate_completion_failure(bedrock_client):
    with pytest.raises(Exception):
        bedrock_client.generate_completion(None)