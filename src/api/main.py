"""
FastAPI application for LLMinate RAG AI API server.
Mounts: /auth, /chat, /documents, /agents
"""
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse

app = FastAPI(title="LLMinate RAG AI API")

# Health check
@app.get("/health")
def health():
    return JSONResponse(content={"status": "ok"}, status_code=200)

# Placeholder routers (to be implemented)
from .chat import router as chat_router

auth_router = APIRouter()
documents_router = APIRouter()
agents_router = APIRouter()

app.include_router(auth_router, prefix="/auth")
app.include_router(chat_router, prefix="/chat")
app.include_router(documents_router, prefix="/documents")
app.include_router(agents_router, prefix="/agents")
