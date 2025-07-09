# LLMinate RAG AI (tasks.md)

## Task Categories
🏗️ **Setup**: Project initialization and configuration  
🔧 **Core**: Essential functionality implementation  
🧪 **Test**: Testing and validation  
📚 **Docs**: Documentation and guides  
🔧 **Logging**: Logfire  
🛡️ **Security**: Compliance and security features  

## Pydantic AI Documentation to refer:
 
- MCP Client: https://ai.pydantic.dev/mcp/client/
- MCP Server: https://ai.pydantic.dev/mcp/server/
- Agents: https://ai.pydantic.dev/agents/
- RAG: https://ai.pydantic.dev/examples/rag/
- Bedrock: https://ai.pydantic.dev/api/models/bedrock/
- Chat App: https://ai.pydantic.dev/examples/chat-app/

## PHASE 1: INFRASTRUCTURE SETUP

### 🏗️ TASK-001: Project Structure and Dependencies
**Objective**: Initialize the project with standard Python and infrastructure setup

**Implementation**:
- Create `pyproject.toml`, `requirements.txt`, `.env.example`, `.gitignore`
- Initialize Git and directory structure

**Implementation details**:
```toml
# pyproject.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "LLMinate-rag-ai"
version = "0.1.0"
description = "Agentic RAG AI Application with Pydantic AI"
dependencies = [
    "pydantic-ai>=0.0.8",
    "logfire[pydantic]",
    "pydantic>=2.5.0",
    "streamlit>=1.28.0",
    "boto3>=1.34.0",
    "sqlalchemy>=2.0.0",
    "psycopg2-binary>=2.9.7",
    "pgvector>=0.2.0",
    "pypdf>=3.17.0",
    "atlassian-python-api>=3.41.0",
    "cryptography>=41.0.0",
    "python-dotenv>=1.0.0",
    "alembic>=1.12.0",
    "pytest>=7.4.0",
    "fastapi",
    "uvicorn",
    "black>=23.9.0",
    "flake8>=6.1.0"
]
```

**Success criteria**:
- [ ] All dependencies install without conflicts
- [ ] Project structure matches architecture
- [ ] Environment variables properly configured
- [ ] Git repository initialized with proper .gitignore

### 🔧 TASK-002: Core Configuration System
**Objective**: Set up Pydantic-based configuration with environment variable loading

**Implementation**:
- Define config models for AWS, Database, JIRA, Confluence, and general settings in `src/core/config.py`
- Initialize Logfire in `src/core/logger.py`

**Success Criteria**:
- [ ] Logs emit structured JSON
- [ ] Secrets and config values are securely loaded

### 🏗️ TASK-003: Database Setup
**Objective**: Set up PostgreSQL with pgvector and indexing

**Implementation**:
- Create models in `src/core/models.py`
- Write script `scripts/setup_db.py` to:
  - Enable `pgvector`
  - Create tables
    - Schema
        - Agents Table
            -Fields: agent_id (PK), name, description, model_config (JSON), created_at, status.
        - Documents Table
            -Fields: doc_id (PK), agent_id (FK), source_filename, uploaded_at.
        - Embeddings Table
            -Fields: chunk_id (PK), doc_id (FK), agent_id (FK), vector, metadata (JSONB).
  - Create vector
  - Create admin user

**Success Criteria**:
- [ ] Database schema created with all models and indexes
- [ ] `python scripts/setup_db.py` completes without error

## PHASE 2: RAG PIPELINE

### 🔧 TASK-004: Bedrock Integration
**Objective**: Create a BedrockClient that supports both embedding and chat completion

**Implementation**:
- Define `BedrockClient` class with `generate_embeddings()` and `generate_completion()`

**Success criteria**:
- [ ] Bedrock client connects successfully
- [ ] Embeddings generation works
- [ ] LLM completions work
- [ ] Error handling implemented

### 🔧 TASK-005: Document Processor
**Objective**: Build ingestion logic for processing PDFs

**Implementation**:
- `scripts/ingest_documents.py`: Uses `DocumentProcessor`
- `DocumentProcessor` will:
  - Extract text from PDFs
  - Chunk text with overlap
  - Call BedrockClient for embeddings
  - Store vectors using VectorStore
  - Store in Documents Table & Embeddings Table

**Success Criteria**:
- [ ] Valid PDF results in chunks and stored embeddings
- [ ] Metadata and indexes are attached correctly
- [ ] Documents Table & Embeddings Table are populated correctly

### 🔧 TASK-006: Vector Store
**Objective**: Build pgvector-backed vector storage with agent isolation

**Implementation**:
- Define `VectorStore` with:
  - `store_embeddings()`
  - `similarity_search()`
  - `delete_agent_embeddings()`

**Success Criteria**:
- [ ] Document insertion works
- [ ] Retrieval queries isolate by agent_id
- [ ] Vector index used efficiently

### 🔧 TASK-007: Prompt Builder
**Objective**: Dynamically assemble prompts with context and sources

**Implementation**:
- `PromptBuilder` accepts query + context and returns formatted prompt

**Success Criteria**:
- [ ] Source snippets embedded
- [ ] Template follows medical-compliance format

### 🔧 TASK-008: RAG Pipeline
**Objective**: Central pipeline to perform retrieval + prompting + LLM generation

**Implementation**:
- `RAGPipeline.process_query(...)` performs:
  - Retrieval from VectorStore
  - Prompt construction
  - Amazon Bedrock Claude call

**Success Criteria**:
- [ ] Generates relevant, cited answers
- [ ] Confidence metadata included
- [ ] Query processing works correctly
- [ ] Relevant documents retrieved
- [ ] Similarity scoring is accurate
- [ ] Hybrid search improves results
- [ ] Performance is optimized

### 🔧 TASK-009: RAG Agent
**Objective**: Wrap pipeline as a Pydantic AI Agent

**Implementation**:
- `agent_rag.py` defines `create_rag_agent()` and wraps `RAGPipeline`
- Input: query + user context → Output: RAGResponse

**Status:**
- [x] Implemented as `src/agents/agent_rag.py` (see code)
- [x] Agent can be invoked via `process_query()`
- [x] System prompt, context, and output type follow plan

**Success Criteria**:
- [x] Agent can be invoked via `run()`
- [ ] Logs include span trace and source info

## PHASE 3: MCP INTEGRATION

### 🔧 TASK-010: JIRA MCP Server
**Objective**: MCP server with tools to create/read issues
Read this GitHub README to understand best how to create MCP servers with Python:

https://github.com/modelcontextprotocol/python-sdk/tree/main

**Files to create**: `src/mcp_servers/jira_server/main.py`, `src/mcp_servers/jira_server/tools.py`

**Implementation**:
- Define JIRA models, tools, and main server runner
- Endpoint for: create issue, get issue


**Implementation code example**:
```python
# src/mcp_servers/jira_server/tools.py
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from atlassian import Jira
from src.core.config import Config

class JIRAIssue(BaseModel):
    key: str
    summary: str
    description: str
    status: str
    assignee: Optional[str]
    priority: str
    issue_type: str

class JIRATools:
    def __init__(self, config: Config):
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
        # Implementation for issue creation
        pass
    
    async def get_issue(self, issue_key: str) -> JIRAIssue:
        """Get JIRA issue details"""
        # Implementation for issue retrieval
        pass
    
    async def search_issues(self, jql: str) -> List[JIRAIssue]:
        """Search JIRA issues using JQL"""
        # Implementation for issue search
        pass
```

**Success criteria**:
- [ ] JIRA API connection works
- [ ] Issue creation successful
- [ ] Issue retrieval works
- [ ] Search functionality works
- [ ] Error handling implemented

### 🔧 TASK-011: Confluence MCP Server
**Objective**: MCP server to create/update/format pages
**Files to create**: `src/mcp_servers/confluence_server/main.py`, `src/mcp_servers/confluence_server/tools.py`

**Implementation**:
- Define Confluence models, tools, and server runner

**Implementation code example**:
```python
# src/mcp_servers/confluence_server/tools.py
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from atlassian import Confluence
from src.core.config import Config

class ConfluencePage(BaseModel):
    id: str
    title: str
    content: str
    space_key: str
    version: int
    url: str

class ConfluenceTools:
    def __init__(self, config: Config):
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
        # Implementation for page creation
        pass
    
    async def update_page(
        self, 
        page_id: str, 
        title: str, 
        content: str
    ) -> ConfluencePage:
        """Update existing Confluence page"""
        # Implementation for page update
        pass
    
    async def get_page(self, page_id: str) -> ConfluencePage:
        """Get Confluence page details"""
        # Implementation for page retrieval
        pass
```

**Success criteria**:
- [ ] Confluence API connection works
- [ ] Page creation successful
- [ ] Page updates work
- [ ] Page retrieval works
- [ ] Content formatting preserved


### 🔧 TASK-012: MCP Client Agent
**Objective**: Agent that can call MCP tools (JIRA, Confluence)

**Implementation**:
- `create_mcp_agent()` creates agent with tool route logic
**Files to create**: `src/agents/agent_mcp.py`

**Implementation code example**:
```python
# src/agents/agent_mcp.py
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from src.mcp_servers.jira_server.tools import JIRATools
from src.mcp_servers.confluence_server.tools import ConfluenceTools

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
    def __init__(self, config: Config):
        self.jira_tools = JIRATools(config)
        self.confluence_tools = ConfluenceTools(config)
        self.agent = Agent(
            model='bedrock:anthropic.claude-3-sonnet-20240229-v1:0',
            result_type=MCPResponse,
            system_prompt=self._get_system_prompt()
        )
    
    def _get_system_prompt(self) -> str:
        return """You are an AI assistant that can interact with JIRA and Confluence.
        You can create issues, update pages, and search for information.
        Always confirm actions before executing them."""
    
    @self.agent.tool
    async def create_jira_issue(
        self, 
        project_key: str, 
        summary: str, 
        description: str
    ) -> Dict[str, Any]:
        """Create a new JIRA issue"""
        # Implementation for JIRA issue creation
        pass
    
    @self.agent.tool
    async def create_confluence_page(
        self, 
        space_key: str, 
        title: str, 
        content: str
    ) -> Dict[str, Any]:
        """Create a new Confluence page"""
        # Implementation for Confluence page creation
        pass
```

**Success criteria**:
- [ ] Agent can create JIRA issues
- [ ] Agent can create Confluence pages
- [ ] Tool selection works correctly
- [ ] Error handling implemented
- [ ] User confirmation for actions

## PHASE 4: UI + API

### 🔧 TASK-013: API Server
**Objective**: FastAPI app with routing and middleware

**Implementation**:
- `src/api/main.py` defines app
- Mounts: `/auth`, `/chat`, `/documents`, `/agents`

**Success Criteria**:
- [x] `GET /health` returns 200
- [x] All routers included

### 🔧 TASK-014: Chat API
**Objective**: Route chat queries to RAG/MCP agents

**Implementation**:
- `/chat/query`: POST endpoint
- `/chat/ws/{agent_id}`: WebSocket

**Status:**
- [x] `/chat/query` POST endpoint implemented (routes to RAG/MCP agents)
- [x] `/chat/ws/{agent_id}` WebSocket endpoint stub implemented

**Success Criteria**:
- [x] Agent responses logged (via JSONResponse)
- [x] WebSocket bi-directional streaming works (stub/echo for now)

### 🔧 TASK-015: Streamlit App
**Objective**: Unified UI for Dashboard, Chat, Admin

**Implementation**:
- Main: `src/ui/main.py`
- Pages: `chat_app`, `admin_app` (auth_ui and agent_dashboard: stubs/TODO)

**Status:**
- [x] Main navigation and page switching implemented
- [x] Chat interface and admin dashboard stubs implemented

**Success Criteria**:
- [x] JWT login works
- [x] Chat history maintained (in session)
- [x] Admin can add agents and its related documents for knowledge base

**Implementation Code example**:
```python
# src/ui/chat_app.py
import streamlit as st
from typing import Dict, Any, List
from src.agents.agent_rag import RAGAgent
from src.agents.agent_mcp import MCPAgent
from src.core.config import Config

class ChatInterface:
    def __init__(self):
        self.config = Config()
        self.rag_agent = RAGAgent(self.config)
        self.mcp_agent = MCPAgent(self.config)
    
    def render_chat_interface(self):
        st.title("Healthcare AI Assistant")
        
        # Agent selection
        selected_agent = st.selectbox(
            "Select Agent",
            ["RAG Agent (Document Q&A)", "MCP Agent (JIRA/Confluence)"]
        )
        
        # Chat interface
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # User input
        if prompt := st.chat_input("Ask a question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.write(prompt)
            
            # Process with selected agent
            if selected_agent.startswith("RAG"):
                response = await self.process_rag_query(prompt)
            else:
                response = await self.process_mcp_query(prompt)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            with st.chat_message("assistant"):
                st.write(response)
    
    async def process_rag_query(self, query: str) -> str:
        """Process query with RAG agent"""
        # Implementation for RAG query processing
        pass
    
    async def process_mcp_query(self, query: str) -> str:
        """Process query with MCP agent"""
        # Implementation for MCP query processing
        pass
```

**Implementation details**:
```python
# src/ui/admin_app.py
import streamlit as st
import pandas as pd
from typing import List, Dict, Any
from src.database.models import Document, AuditLog
from src.embeddings.vector_store import VectorStore

class AdminInterface:
    def __init__(self):
        self.vector_store = VectorStore()
    
    def render_admin_interface(self):
        st.title("Healthcare AI Admin Dashboard")
        
        # Sidebar navigation
        page = st.sidebar.selectbox(
            "Navigation",
            ["Document Management", "Agent Configuration", "Audit Logs", "User Management"]
        )
        
        if page == "Document Management":
            self.render_document_management()
        elif page == "Agent Configuration":
            self.render_agent_configuration()
        elif page == "Audit Logs":
            self.render_audit_logs()
        elif page == "User Management":
            self.render_user_management()
    
    def render_document_management(self):
        st.header("Document Management")
        
        # Document upload
        st.subheader("Upload Documents")
        uploaded_files = st.file_uploader(
            "Upload PDF documents",
            type=['pdf'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            for file in uploaded_files:
                if st.button(f"Process {file.name}"):
                    self.process_document(file)
        
        # Document list
        st.subheader("Existing Documents")
        documents = self.get_documents()
        if documents:
            df = pd.DataFrame(documents)
            st.dataframe(df)
    
    def process_document(self, file):
        """Process uploaded document"""
        # Implementation for document processing
        pass
    
    def get_documents(self):
        # Implementation to get documents, add more parameters if necessary


**Success criteria**:
- [ ] Chat interface renders correctly
- [ ] Agent selection works
- [ ] Message history preserved
- [ ] Both agents accessible
- [ ] User experience is intuitive
- [ ] Admin can add agents and its related documents

## PHASE 5: TESTING & COMPLIANCE

### 🤞 TASK-016: Unit Tests
**Objective**: Write test coverage for core modules

**Test files**:
- `tests/test_embeddings.py`
- `tests/test_agents.py`

**Success Criteria**:
- [ ] Bedrock embedding tests pass
- [ ] RAG/MCP agents validate input/output

### 🔒 TASK-017: Compliance Logging
**Objective**: HIPAA/GDPR compliant audit logging

**Implementation**:
- Use `logfire` and `log_user_action()` from logger module

**Success Criteria**:
- [ ] User actions logged with metadata
- [ ] PHI access tracked and stored


