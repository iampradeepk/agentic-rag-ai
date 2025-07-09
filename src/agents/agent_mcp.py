"""
MCPAgent: Pydantic AI Agent for interacting with JIRA and Confluence MCP servers.
"""
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from src.mcp_servers.jira_server.tools import JIRATools
from src.mcp_servers.confluence_server.tools import ConfluenceTools
from src.core.config import AppConfig

class MCPContext(BaseModel):
    user_id: str
    session_id: str
    available_tools: List[str]

class MCPResponse(BaseModel):
    action_taken: str
    result: Dict[str, Any]
    success: bool
    message: str

class MCPAgent:
    def __init__(self):
        config = AppConfig()
        self.jira_tools = JIRATools(config)
        self.confluence_tools = ConfluenceTools(config)
        self.agent = Agent(
            model='bedrock:anthropic.claude-3-sonnet-20240229-v1:0',
            result_type=MCPResponse,
            system_prompt=self._get_system_prompt()
        )
        self._register_tools()

    def _get_system_prompt(self) -> str:
        return (
            "You are an AI assistant that can interact with JIRA and Confluence. "
            "You can create issues, update pages, and search for information. "
            "Always confirm actions before executing them."
        )

    def _register_tools(self):
        @self.agent.tool
        async def create_jira_issue(
            project_key: str,
            summary: str,
            description: str,
            issue_type: str = "Task"
        ) -> Dict[str, Any]:
            """Create a new JIRA issue"""
            issue = await self.jira_tools.create_issue(project_key, summary, description, issue_type)
            return issue.dict()

        @self.agent.tool
        async def get_jira_issue(issue_key: str) -> Dict[str, Any]:
            """Get JIRA issue details"""
            issue = await self.jira_tools.get_issue(issue_key)
            return issue.dict()

        @self.agent.tool
        async def search_jira_issues(jql: str) -> List[Dict[str, Any]]:
            """Search JIRA issues using JQL"""
            issues = await self.jira_tools.search_issues(jql)
            return [i.dict() for i in issues]

        @self.agent.tool
        async def create_confluence_page(
            space_key: str,
            title: str,
            content: str,
            parent_id: Optional[str] = None
        ) -> Dict[str, Any]:
            """Create a new Confluence page"""
            page = await self.confluence_tools.create_page(space_key, title, content, parent_id)
            return page.dict()

        @self.agent.tool
        async def update_confluence_page(
            page_id: str,
            title: str,
            content: str
        ) -> Dict[str, Any]:
            """Update existing Confluence page"""
            page = await self.confluence_tools.update_page(page_id, title, content)
            return page.dict()

        @self.agent.tool
        async def get_confluence_page(page_id: str) -> Dict[str, Any]:
            """Get Confluence page details"""
            page = await self.confluence_tools.get_page(page_id)
            return page.dict()

    async def process_action(self, action: str, params: Dict[str, Any], context: MCPContext) -> MCPResponse:
        """
        Process an action (tool call) and return a structured response.
        """
        # This is a placeholder for routing logic; in practice, you may want to use self.agent.run()
        return MCPResponse(
            action_taken=action,
            result={},
            success=True,
            message="Action processed (stub)."
        )
