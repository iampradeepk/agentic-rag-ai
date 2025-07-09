"""
Configuration management for LLMinate RAG AI.
Loads environment variables and provides settings for AWS, DB, and external services.
"""
from pydantic import BaseSettings, Field
from typing import Optional

class AWSSettings(BaseSettings):
    access_key_id: str = Field(..., env="AWS_ACCESS_KEY_ID")
    secret_access_key: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    region: str = Field(default="us-east-1", env="AWS_REGION")
    bedrock_model_id: str = Field(..., env="BEDROCK_MODEL_ID")

class DatabaseSettings(BaseSettings):
    url: str = Field(..., env="DATABASE_URL")

class JiraSettings(BaseSettings):
    server_url: str = Field(..., env="JIRA_SERVER_URL")
    username: str = Field(..., env="JIRA_USERNAME")
    api_token: str = Field(..., env="JIRA_API_TOKEN")

class ConfluenceSettings(BaseSettings):
    server_url: str = Field(..., env="CONFLUENCE_SERVER_URL")
    username: str = Field(..., env="CONFLUENCE_USERNAME")
    api_token: str = Field(..., env="CONFLUENCE_API_TOKEN")

class AppConfig(BaseSettings):
    aws: AWSSettings = AWSSettings()
    db: DatabaseSettings = DatabaseSettings()
    jira: JiraSettings = JiraSettings()
    confluence: ConfluenceSettings = ConfluenceSettings()

    class Config:
        env_file = ".env"
