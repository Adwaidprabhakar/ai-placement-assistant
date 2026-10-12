import uuid
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.services.llm_service import llm_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    suggestions: List[str]

DEFAULT_SUGGESTIONS = [
    "Amazon SDE Recruitment Rounds & Principles",
    "How to make my resume ATS-friendly?",
    "High-frequency DSA topics for campus placements",
    "Behavioral interview STAR method explanation"
]

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    
    # Generate LLM Response (llm_service will manage appending user and assistant messages to session_id)
    reply_text = await llm_service.generate_response(req.message, session_id=session_id)
    
    return ChatResponse(
        reply=reply_text,
        session_id=session_id,
        suggestions=DEFAULT_SUGGESTIONS
    )
