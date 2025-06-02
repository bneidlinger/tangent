"""
Enhanced Tangnet Chat API with model abstraction and persistence
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
import json
import asyncio

from sqlalchemy.orm import Session
from database import get_db, save_message, get_session_history, create_session, ChatSession
from inference_client import get_inference_client
from config import settings

app = FastAPI(title="Tangnet Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    personality: Optional[str] = "default"
    stream: Optional[bool] = False
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    
class SessionInfo(BaseModel):
    session_id: str
    personality: str
    message_count: int
    created_at: str

# Personality prompts (as outlined in the docs)
PERSONALITIES = {
    "default": "You are a helpful AI assistant.",
    "rick": "You are Rick from Rick and Morty. Respond in his style - cynical, genius, with burps and scientific rambling.",
    "security": "You are a security-focused AI. Analyze everything from a cybersecurity perspective.",
    "lorekeeper": "You are the Lorekeeper, a wise AI that speaks in fantasy/RPG style about the Tangnet cluster."
}

# Active WebSocket connections
active_connections: Dict[str, WebSocket] = {}

@app.get("/")
def root():
    """Redirect to chat interface"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Single message chat endpoint"""
    
    # Create or validate session
    session_id = request.session_id or str(uuid.uuid4())
    
    if not request.session_id:
        create_session(db, session_id, request.personality)
    
    # Save user message
    save_message(db, session_id, "user", request.message)
    
    # Get chat history for context
    history = get_session_history(db, session_id, limit=settings.max_history_messages)
    
    # Build prompt with personality and history
    prompt = build_prompt(request.message, history, request.personality)
    
    # Get inference client
    client = get_inference_client()
    
    # Generate response
    response = await client.generate(
        prompt,
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )
    
    # Save AI response
    save_message(db, session_id, "assistant", response)
    
    return ChatResponse(response=response, session_id=session_id)

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest, db: Session = Depends(get_db)):
    """Streaming chat endpoint"""
    
    # Create or validate session
    session_id = request.session_id or str(uuid.uuid4())
    
    if not request.session_id:
        create_session(db, session_id, request.personality)
    
    # Save user message
    save_message(db, session_id, "user", request.message)
    
    # Get chat history for context
    history = get_session_history(db, session_id, limit=settings.max_history_messages)
    
    # Build prompt with personality and history
    prompt = build_prompt(request.message, history, request.personality)
    
    # Get inference client
    client = get_inference_client()
    
    async def generate():
        full_response = ""
        async for chunk in client.stream_generate(
            prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        ):
            full_response += chunk
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        
        # Save complete response
        save_message(db, session_id, "assistant", full_response)
        yield f"data: {json.dumps({'done': True, 'session_id': session_id})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, db: Session = Depends(get_db)):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    active_connections[session_id] = websocket
    
    # Create session if new
    existing = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not existing:
        create_session(db, session_id)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            message = data.get("message", "")
            personality = data.get("personality", "default")
            
            # Save user message
            save_message(db, session_id, "user", message)
            
            # Get chat history
            history = get_session_history(db, session_id, limit=settings.max_history_messages)
            
            # Build prompt
            prompt = build_prompt(message, history, personality)
            
            # Get inference client
            client = get_inference_client()
            
            # Stream response
            full_response = ""
            async for chunk in client.stream_generate(prompt):
                full_response += chunk
                await websocket.send_json({
                    "type": "chunk",
                    "content": chunk
                })
            
            # Save AI response
            save_message(db, session_id, "assistant", full_response)
            
            # Send completion
            await websocket.send_json({
                "type": "complete",
                "response": full_response,
                "history": format_history(history[-10:])  # Last 10 messages
            })
            
    except WebSocketDisconnect:
        del active_connections[session_id]

@app.get("/sessions", response_model=List[SessionInfo])
def list_sessions(db: Session = Depends(get_db)):
    """List all chat sessions"""
    sessions = db.query(ChatSession).all()
    
    result = []
    for session in sessions:
        message_count = db.query(ChatMessage).filter(
            ChatMessage.session_id == session.id
        ).count()
        
        result.append(SessionInfo(
            session_id=session.id,
            personality=session.personality,
            message_count=message_count,
            created_at=session.created_at.isoformat()
        ))
    
    return result

@app.get("/new_session")
def new_session(personality: str = "default", db: Session = Depends(get_db)):
    """Create a new chat session"""
    session_id = str(uuid.uuid4())
    create_session(db, session_id, personality)
    return {"session_id": session_id}

@app.get("/sessions/{session_id}/history")
def get_history(session_id: str, limit: int = 50, db: Session = Depends(get_db)):
    """Get chat history for a session"""
    messages = get_session_history(db, session_id, limit=limit)
    return format_history(messages)

@app.delete("/sessions/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_db)):
    """Delete a chat session and its history"""
    # Delete messages
    db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
    
    # Delete session
    db.query(ChatSession).filter(ChatSession.id == session_id).delete()
    
    db.commit()
    return {"message": "Session deleted"}

# Helper functions
def build_prompt(message: str, history: List[ChatMessage], personality: str) -> str:
    """Build prompt with personality and conversation history"""
    
    # Get personality prompt
    system_prompt = PERSONALITIES.get(personality, PERSONALITIES["default"])
    
    # Format conversation history
    conversation = f"System: {system_prompt}\n\n"
    
    for msg in history[-settings.max_history_messages:]:
        role = "Human" if msg.role == "user" else "Assistant"
        conversation += f"{role}: {msg.content}\n\n"
    
    # Add current message
    conversation += f"Human: {message}\n\nAssistant:"
    
    return conversation

def format_history(messages: List[ChatMessage]) -> List[Dict[str, Any]]:
    """Format message history for API response"""
    return [
        {
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.created_at.isoformat()
        }
        for msg in messages
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)