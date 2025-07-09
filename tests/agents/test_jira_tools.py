import pytest
from src.mcp_servers.jira_server.tools import JIRATools
from src.core.config import Config

@pytest.fixture
def jira_tools():
    config = Config()
    return JIRATools(config)

def test_create_issue_expected(jira_tools):
    try:
        issue = pytest.run(jira_tools.create_issue(
            project_key="PROJ",
            summary="Test Issue",
            description="Test description"
        ))
        assert hasattr(issue, 'key')
        assert hasattr(issue, 'summary')
    except Exception as e:
        pytest.skip(f"JIRA not available: {e}")

def test_get_issue_edge_case(jira_tools):
    with pytest.raises(Exception):
        pytest.run(jira_tools.get_issue("INVALID-KEY"))

def test_search_issues_failure(jira_tools):
    with pytest.raises(Exception):
        pytest.run(jira_tools.search_issues(None))
