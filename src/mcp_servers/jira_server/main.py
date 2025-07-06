"""
JIRA MCP Server main entrypoint using FastMCP.
"""
from mcp.server.fastmcp import FastMCP
from src.core.config import AppConfig
from .tools import JIRATools, JIRAIssue

config = AppConfig()
jira_tools = JIRATools(config)

app = FastMCP("JIRA MCP Server")

@app.tool()
async def create_issue(
    project_key: str,
    summary: str,
    description: str,
    issue_type: str = "Task"
) -> JIRAIssue:
    return await jira_tools.create_issue(project_key, summary, description, issue_type)

@app.tool()
async def get_issue(issue_key: str) -> JIRAIssue:
    return await jira_tools.get_issue(issue_key)

@app.tool()
async def search_issues(jql: str) -> list[JIRAIssue]:
    return await jira_tools.search_issues(jql)

if __name__ == "__main__":
    app.run()
