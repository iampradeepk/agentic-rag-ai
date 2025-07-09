"""
Chat API endpoints for LLMinate RAG AI.
- POST /chat/query: Route queries to RAG or MCP agents
- WebSocket /chat/ws/{agent_id}: Bi-directional streaming (stub)
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.agents.agent_rag import RAGAgent, RAGContext
from src.agents.agent_mcp import MCPAgent, MCPContext
from typing import Dict, Any
import asyncio

router = APIRouter()

class ChatQueryRequest(BaseModel):
    agent_type: str  # 'rag' or 'mcp'
    query: str
    user_id: str
    session_id: str
    conversation_history: list[dict[str, str]] = []

@router.post("/query")
async def chat_query(request: ChatQueryRequest):
    if request.agent_type == 'rag':
        agent = RAGAgent()
        context = RAGContext(
            user_id=request.user_id,
            session_id=request.session_id,
            conversation_history=request.conversation_history
        )
        response = await agent.process_query(request.query, context)
        return JSONResponse(content=response.dict())
    elif request.agent_type == 'mcp':
        agent = MCPAgent()
        context = MCPContext(
            user_id=request.user_id,
            session_id=request.session_id,
            available_tools=[]
        )
        # For demo, just echo action; in production, parse intent/tool
        response = await agent.process_action("manual", {}, context)
        return JSONResponse(content=response.dict())
    else:
        return JSONResponse(content={"error": "Invalid agent_type"}, status_code=400)

# WebSocket endpoint (stub)
@router.websocket("/ws/{agent_id}")
async def chat_ws(websocket: WebSocket, agent_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Echo for now; implement streaming agent response in production
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        pass
