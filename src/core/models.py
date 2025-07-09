"""
Pydantic models for core data structures: Document, ChatMessage, AgentResponse, ErrorResponse.
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Literal
from datetime import datetime

class Document(BaseModel):
    id: str
    title: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
    created_at: datetime
    updated_at: datetime

class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    content: str
    sources: List[str]
    confidence: float
    metadata: Dict[str, Any]

class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime
    trace_id: str
