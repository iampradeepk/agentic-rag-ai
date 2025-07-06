"""
JIRA tools for MCP server: create, get, and search issues.
"""
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from atlassian import Jira
from src.core.config import AppConfig

class JIRAIssue(BaseModel):
    key: str
    summary: str
    description: str
    status: str
    assignee: Optional[str]
    priority: str
    issue_type: str

class JIRATools:
    def __init__(self, config: AppConfig):
        self.jira = Jira(
            url=config.jira.server_url,
            username=config.jira.username,
            password=config.jira.api_token
        )

    async def create_issue(
        self,
        project_key: str,
        summary: str,
        description: str,
        issue_type: str = "Task"
    ) -> JIRAIssue:
        """Create a new JIRA issue"""
        issue = self.jira.issue_create(
            fields={
                'project': {'key': project_key},
                'summary': summary,
                'description': description,
                'issuetype': {'name': issue_type}
            }
        )
        return JIRAIssue(
            key=issue['key'],
            summary=summary,
            description=description,
            status=issue['fields']['status']['name'],
            assignee=issue['fields'].get('assignee', {}).get('displayName'),
            priority=issue['fields'].get('priority', {}).get('name', ''),
            issue_type=issue_type
        )

    async def get_issue(self, issue_key: str) -> JIRAIssue:
        """Get JIRA issue details"""
        issue = self.jira.issue(issue_key)
        return JIRAIssue(
            key=issue['key'],
            summary=issue['fields']['summary'],
            description=issue['fields']['description'],
            status=issue['fields']['status']['name'],
            assignee=issue['fields'].get('assignee', {}).get('displayName'),
            priority=issue['fields'].get('priority', {}).get('name', ''),
            issue_type=issue['fields']['issuetype']['name']
        )

    async def search_issues(self, jql: str) -> List[JIRAIssue]:
        """Search JIRA issues using JQL"""
        issues = self.jira.jql(jql).get('issues', [])
        return [
            JIRAIssue(
                key=issue['key'],
                summary=issue['fields']['summary'],
                description=issue['fields']['description'],
                status=issue['fields']['status']['name'],
                assignee=issue['fields'].get('assignee', {}).get('displayName'),
                priority=issue['fields'].get('priority', {}).get('name', ''),
                issue_type=issue['fields']['issuetype']['name']
            )
            for issue in issues
        ]
