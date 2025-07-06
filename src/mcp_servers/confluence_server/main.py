"""
Confluence MCP Server main entrypoint using FastMCP.
"""
from mcp.server.fastmcp import FastMCP
from src.core.config import AppConfig
from .tools import ConfluenceTools, ConfluencePage

config = AppConfig()
confluence_tools = ConfluenceTools(config)

app = FastMCP("Confluence MCP Server")

@app.tool()
async def create_page(
    space_key: str,
    title: str,
    content: str,
    parent_id: str = None
) -> ConfluencePage:
    return await confluence_tools.create_page(space_key, title, content, parent_id)

@app.tool()
async def update_page(
    page_id: str,
    title: str,
    content: str
) -> ConfluencePage:
    return await confluence_tools.update_page(page_id, title, content)

@app.tool()
async def get_page(page_id: str) -> ConfluencePage:
    return await confluence_tools.get_page(page_id)

if __name__ == "__main__":
    app.run()
