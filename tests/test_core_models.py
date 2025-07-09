import pytest
from src.core.models import Document, ChatMessage, AgentResponse
from datetime import datetime

def test_document_model_expected():
    doc = Document(
        id="1",
        title="Test Doc",
        content="Some content",
        metadata={"source": "test"},
        embedding=[0.1, 0.2],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    assert doc.id == "1"
    assert doc.title == "Test Doc"
    assert isinstance(doc.embedding, list)

def test_chat_message_edge_case():
    with pytest.raises(Exception):
        ChatMessage(
            role="invalid",
            content="Test",
            timestamp=datetime.now()
        )

def test_agent_response_failure():
    with pytest.raises(TypeError):
        AgentResponse(content=None, sources=None, confidence=None, metadata=None)
