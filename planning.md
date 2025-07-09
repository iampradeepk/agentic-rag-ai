# Healthcare RAG AI Application - Cursor AI Implementation Plan

## Project Overview
Healthcare RAG AI application using Pydantic AI, Amazon Bedrock Claude Sonnet, and Aurora PostgreSQL with pgvector for HIPAA/GDPR compliant document processing and question answering.

## Architecture Components

### Core Services
- **RAG Agent**: Pydantic AI agent with Bedrock Claude Sonnet for document Q&A
- **MCP Agent**: Pydantic AI agent with MCP client for JIRA/Confluence integration
- **Vector Store**: Aurora PostgreSQL with pgvector for embeddings
- **MCP Servers**: Standalone servers for JIRA and Confluence operations
- **UI**: Streamlit interfaces for chat and admin functions

### Technology Stack
```yaml
AI Framework: pydantic-ai>=0.0.8
LLM: Amazon Bedrock Claude Sonnet 4
Database: Aurora PostgreSQL with pgvector
Frontend: Streamlit
Security: HIPAA/GDPR compliance with audit logging
```

## File Structure Context
```
src/
├── core/               # Configuration and utilities
├── embeddings/         # Bedrock client and vector operations
├── rag/               # RAG pipeline components
├── agents/            # Pydantic AI agent implementations
├── mcp_servers/       # MCP server implementations
├── ui/                # Streamlit interfaces
└── main.py            # Application entrypoint
```

## Core Dependencies
```python
# requirements.txt
pydantic-ai>=0.0.8
pydantic>=2.5.0
streamlit>=1.28.0
boto3>=1.34.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.7
pgvector>=0.2.0
pypdf>=3.17.0
atlassian-python-api>=3.41.0
cryptography>=41.0.0
python-dotenv>=1.0.0
```

## Environment Configuration
```bash
# .env.example
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
DATABASE_URL=postgresql://user:pass@localhost:5432/healthcare_rag
JIRA_SERVER_URL=https://your-domain.atlassian.net
JIRA_USERNAME=your_username
JIRA_API_TOKEN=your_api_token
CONFLUENCE_SERVER_URL=https://your-domain.atlassian.net
CONFLUENCE_USERNAME=your_username
CONFLUENCE_API_TOKEN=your_api_token
```

## Implementation Phases

### Phase 1: Core Infrastructure
**Files to implement:**
- `src/core/config.py` - Environment and configuration management
- `src/core/logger.py` - Structured logging with compliance
- `src/embeddings/bedrock_client.py` - Bedrock integration
- `src/embeddings/vector_store.py` - PostgreSQL pgvector operations
- `scripts/setup_db.py` - Database initialization

### Phase 2: RAG Pipeline
**Files to implement:**
- `src/rag/retriever.py` - Vector similarity search
- `src/rag/prompt_builder.py` - Healthcare-specific prompts
- `src/rag/pipeline.py` - RAG orchestration
- `src/agents/agent_rag.py` - Main RAG agent
- `scripts/ingest_documents.py` - Document processing pipeline

### Phase 3: MCP Integration
**Files to implement:**
- `src/mcp_servers/jira_server/main.py` - JIRA MCP server
- `src/mcp_servers/jira_server/tools.py` - JIRA operations
- `src/mcp_servers/confluence_server/main.py` - Confluence MCP server
- `src/mcp_servers/confluence_server/tools.py` - Confluence operations
- `src/agents/agent_mcp.py` - MCP client agent

### Phase 4: User Interfaces
**Files to implement:**
- `src/ui/chat_app.py` - Main chat interface
- `src/ui/admin_app.py` - Admin dashboard
- `src/main.py` - Application entrypoint

## Data Models

### Core Pydantic Models
```python
# Document models
class Document(BaseModel):
    id: str
    title: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]]
    created_at: datetime
    updated_at: datetime

# Chat models
class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]]

# Agent models
class AgentResponse(BaseModel):
    content: str
    sources: List[str]
    confidence: float
    metadata: Dict[str, Any]
```

## Security and Compliance Requirements

### HIPAA Compliance
- Audit logging for all data access
- Encrypted storage and transmission
- Access controls and authentication
- Data minimization principles

### GDPR Compliance
- Data subject rights implementation
- Consent management
- Data processing records
- Privacy by design

### Implementation Requirements
```python
# Audit logging structure
class AuditLog(BaseModel):
    timestamp: datetime
    user_id: str
    action: str
    resource: str
    details: Dict[str, Any]
    ip_address: str
    user_agent: str
```

## Performance Requirements

### Response Time Targets
- RAG queries: <5 seconds
- MCP operations: <10 seconds
- Document upload: <30 seconds per MB
- UI interactions: <2 seconds

### Scalability Targets
- Support 10+ concurrent users
- Handle 1000+ documents in knowledge base
- Process 100+ queries per hour
- Maintain 99% uptime

## Testing Strategy

### Unit Tests
- Core component functionality
- Data model validation
- API integration testing
- Security function testing

### Integration Tests
- End-to-end RAG pipeline
- MCP server communication
- Database operations
- UI workflow testing

### Compliance Tests
- Audit trail validation
- Data encryption verification
- Access control testing
- Privacy feature validation

## Error Handling Patterns

### Standard Error Response
```python
class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[Dict[str, Any]]
    timestamp: datetime
    trace_id: str
```

### Retry Logic
- Exponential backoff for AWS services
- Circuit breaker for external APIs
- Graceful degradation for non-critical features
- User-friendly error messages

## Monitoring and Observability

### Key Metrics
- RAG query response times
- Embedding generation latency
- Database query performance
- MCP server availability
- User session metrics

### Logging Requirements
- Structured JSON logging
- Correlation IDs for request tracing
- Security event logging
- Performance metrics logging

## Deployment Configuration

### Docker Setup
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
EXPOSE 8501
CMD ["streamlit", "run", "src/main.py"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    depends_on:
      - postgres
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/healthcare_rag
  
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      - POSTGRES_DB=healthcare_rag
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    ports:
      - "5432:5432"
```

## Code Quality Standards

### Type Hints
- All functions must have type hints
- Use Pydantic models for data validation
- Generic types for collections
- Optional types for nullable values

### Code Structure
- Single responsibility principle
- Dependency injection patterns
- Configuration through environment variables
- Consistent error handling

### Documentation
- Docstrings for all public functions
- Type annotations for clarity
- README files for each major component
- API documentation generation