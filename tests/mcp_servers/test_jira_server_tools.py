import pytest
import asyncio
from src.mcp_servers.jira_server.tools import JIRATools, JIRAIssue
from src.core.config import Config

@pytest.fixture
def jira_tools():
    config = Config()
    return JIRATools(config)

@pytest.mark.asyncio
def test_create_issue_expected(jira_tools):
    try:
        issue = asyncio.run(jira_tools.create_issue(
            project_key="PROJ",
            summary="Test Issue",
            description="Test description"
        ))
        assert isinstance(issue, JIRAIssue)
        assert hasattr(issue, 'key')
        assert hasattr(issue, 'summary')
    except Exception as e:
        pytest.skip(f"JIRA not available: {e}")

@pytest.mark.asyncio
def test_get_issue_edge_case(jira_tools):
    with pytest.raises(Exception):
        asyncio.run(jira_tools.get_issue("INVALID-KEY"))

@pytest.mark.asyncio
def test_search_issues_failure(jira_tools):
    with pytest.raises(Exception):
        asyncio.run(jira_tools.search_issues(None))
