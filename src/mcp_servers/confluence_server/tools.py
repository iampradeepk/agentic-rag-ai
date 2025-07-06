"""
Confluence tools for MCP server: create, update, and get pages.
"""
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from atlassian import Confluence
from src.core.config import AppConfig

class ConfluencePage(BaseModel):
    id: str
    title: str
    content: str
    space_key: str
    version: int
    url: str

class ConfluenceTools:
    def __init__(self, config: AppConfig):
        self.confluence = Confluence(
            url=config.confluence.server_url,
            username=config.confluence.username,
            password=config.confluence.api_token
        )

    async def create_page(
        self,
        space_key: str,
        title: str,
        content: str,
        parent_id: Optional[str] = None
    ) -> ConfluencePage:
        """Create a new Confluence page"""
        page = self.confluence.create_page(
            space=space_key,
            title=title,
            body=content,
            parent_id=parent_id
        )
        return ConfluencePage(
            id=page['id'],
            title=title,
            content=content,
            space_key=space_key,
            version=page['version']['number'],
            url=page['_links']['base'] + page['_links']['webui']
        )

    async def update_page(
        self,
        page_id: str,
        title: str,
        content: str
    ) -> ConfluencePage:
        """Update existing Confluence page"""
        page = self.confluence.update_page(
            page_id=page_id,
            title=title,
            body=content
        )
        return ConfluencePage(
            id=page['id'],
            title=title,
            content=content,
            space_key=page['_links'].get('space', ''),
            version=page['version']['number'],
            url=page['_links']['base'] + page['_links']['webui']
        )

    async def get_page(self, page_id: str) -> ConfluencePage:
        """Get Confluence page details"""
        page = self.confluence.get_page_by_id(page_id)
        return ConfluencePage(
            id=page['id'],
            title=page['title'],
            content=page['body']['storage']['value'],
            space_key=page['space']['key'],
            version=page['version']['number'],
            url=page['_links']['base'] + page['_links']['webui']
        )
