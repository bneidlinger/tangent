# Tangnet API Chat Framework Setup

"""
This file will serve as the foundation for your Tangnet custom chat API,
including backend logic, chat history management, and frontend hooks.
We'll use FastAPI for the backend, WebSockets for real-time chat, and
Tailwind + HTMX or a lightweight JS framework for the frontend later.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import uuid
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global memory for sessions (can later be Redis or file-backed)
chat_sessions = {}

# Simple in-memory chat history per session
class ChatMessage(BaseModel):
    role: str  # 'user' or 'ai'
    message: str

class Session:
    def __init__(self):
        self.history = []

    def add_message(self, role: str, message: str):
        self.history.append(ChatMessage(role=role, message=message))

    def get_messages(self):
        return [m.dict() for m in self.history]

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()

    if session_id not in chat_sessions:
        chat_sessions[session_id] = Session()

    session = chat_sessions[session_id]

    try:
        while True:
            data = await websocket.receive_text()
            session.add_message("user", data)
            
            # --- TODO: Add llama.cpp response hook here ---
            response = f"[Fake AI says]: You said '{data}'"
            session.add_message("ai", response)

            await websocket.send_json({
                "user": data,
                "response": response,
                "history": session.get_messages(),
            })

    except WebSocketDisconnect:
        print(f"Session {session_id} disconnected")
        # Optional: Clean up session

@app.get("/new_session")
def create_session():
    session_id = str(uuid.uuid4())
    chat_sessions[session_id] = Session()
    return {"session_id": session_id}

# For later: POST endpoint to send/receive single messages (non-websocket)
# For later: Save/load chat history to disk or DB
# For later: Frontend chat interface using JS or HTMX

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
