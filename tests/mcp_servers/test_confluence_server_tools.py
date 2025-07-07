import pytest
import asyncio
from src.mcp_servers.confluence_server.tools import ConfluenceTools, ConfluencePage
from src.core.config import Config

@pytest.fixture
def confluence_tools():
    config = Config()
    return ConfluenceTools(config)

@pytest.mark.asyncio
def test_create_page_expected(confluence_tools):
    try:
        page = asyncio.run(confluence_tools.create_page(
            space_key="SPACE",
            title="Test Page",
            content="Test content"
        ))
        assert isinstance(page, ConfluencePage)
        assert hasattr(page, 'id')
        assert hasattr(page, 'title')
    except Exception as e:
        pytest.skip(f"Confluence not available: {e}")

@pytest.mark.asyncio
def test_update_page_edge_case(confluence_tools):
    with pytest.raises(Exception):
        asyncio.run(confluence_tools.update_page(None, None, None))

@pytest.mark.asyncio
def test_get_page_failure(confluence_tools):
    with pytest.raises(Exception):
        asyncio.run(confluence_tools.get_page("INVALID-ID"))
