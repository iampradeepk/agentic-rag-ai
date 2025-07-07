# LLMinate RAG AI

Agentic RAG AI Application using Pydantic AI, Amazon Bedrock, and Aurora PostgreSQL with pgvector.

## Project Structure

```
src/
├── core/               # Configuration and utilities
├── embeddings/         # Bedrock client and vector operations
├── rag/                # RAG pipeline components
├── agents/             # Pydantic AI agent implementations
├── mcp_servers/        # MCP server implementations
├── ui/                 # Streamlit interfaces
└── main.py             # Application entrypoint
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your credentials.
3. Run database setup:
   ```bash
   python scripts/setup_db.py
   ```

## Main Technologies
- Pydantic AI
- Amazon Bedrock (Claude Sonnet)
- Aurora PostgreSQL + pgvector
- Streamlit
- FastAPI
- Logfire

## Features
- Document Q&A via RAG pipeline
- JIRA/Confluence integration via MCP
- Streamlit UI (chat, admin, agent dashboard)
- JWT login authentication
- Full document ingestion from UI
- Admin agent management

## Development Phases
- Infrastructure & Config
- RAG Pipeline
- MCP Integration
- UI
