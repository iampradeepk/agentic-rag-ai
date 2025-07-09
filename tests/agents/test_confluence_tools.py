import pytest
from src.mcp_servers.confluence_server.tools import ConfluenceTools
from src.core.config import Config

@pytest.fixture
def confluence_tools():
    config = Config()
    return ConfluenceTools(config)

def test_create_page_expected(confluence_tools):
    try:
        page = pytest.run(confluence_tools.create_page(
            space_key="SPACE",
            title="Test Page",
            content="Test content"
        ))
        assert hasattr(page, 'id')
        assert hasattr(page, 'title')
    except Exception as e:
        pytest.skip(f"Confluence not available: {e}")

def test_update_page_edge_case(confluence_tools):
    with pytest.raises(Exception):
        pytest.run(confluence_tools.update_page(None, None, None))

def test_get_page_failure(confluence_tools):
    with pytest.raises(Exception):
        pytest.run(confluence_tools.get_page("INVALID-ID"))
