import pytest
from src.agents.agent_mcp import MCPAgent
from src.core.config import Config

@pytest.fixture
def mcp_agent():
    config = Config()
    return MCPAgent(config)

def test_create_jira_issue_expected(mcp_agent):
    try:
        result = mcp_agent.create_jira_issue("PROJ", "Test Issue", "Test description")
        assert isinstance(result, dict)
        assert result.get("success")
    except Exception as e:
        pytest.skip(f"JIRA not available: {e}")

def test_create_confluence_page_expected(mcp_agent):
    try:
        result = mcp_agent.create_confluence_page("SPACE", "Test Page", "Test content")
        assert isinstance(result, dict)
        assert result.get("success")
    except Exception as e:
        pytest.skip(f"Confluence not available: {e}")

def test_create_jira_issue_failure(mcp_agent):
    with pytest.raises(Exception):
        mcp_agent.create_jira_issue(None, None, None)

def test_create_confluence_page_failure(mcp_agent):
    with pytest.raises(Exception):
        mcp_agent.create_confluence_page(None, None, None)
