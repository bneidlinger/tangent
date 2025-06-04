"""
Tangnet Chat Server - Connects to your Raspberry Pi
Minimal dependencies version
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uuid
import asyncio
import subprocess
import json
from typing import Dict

app = FastAPI(title="Tangnet Chat Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration
PI_HOST = "192.168.1.31"
PI_USER = "brand"

# Active sessions
sessions: Dict[str, list] = {}

# Personality prompts
PERSONALITIES = {
    "default": "",
    "rick": "Respond as Rick from Rick and Morty with burps and cynical genius rambling. ",
    "security": "Analyze everything from a cybersecurity perspective. ",
    "lorekeeper": "Speak as a wise fantasy RPG character about the Tangnet cluster. "
}

async def run_tangnet_command(prompt: str) -> str:
    """Run tangnet command on the Pi via SSH"""
    # Escape quotes for PowerShell and bash
    escaped_prompt = prompt.replace('"', '`"').replace("'", "''")
    
    # Try different command formats
    commands = [
        # PowerShell command to SSH and run tangnet
        f'powershell.exe -Command "ssh {PI_USER}@{PI_HOST} \'tangnet `\\"{escaped_prompt}`\\\'\'"',
        # Try with bash -l
        f'powershell.exe -Command "ssh {PI_USER}@{PI_HOST} \'bash -l -c `\\"tangnet `\\\\`\\"{escaped_prompt}`\\\\`\\"`\\\'\'"',
        # Direct llama.cpp command
        f'powershell.exe -Command "ssh {PI_USER}@{PI_HOST} \'cd /home/{PI_USER} && ./llama.cpp/llama-cli -m ./models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -c 2048 -t 4 -ngl 33 --no-display-prompt -p `\\"{escaped_prompt}`\\\'\'"',
        # Fallback without PowerShell (for Linux/WSL with proper SSH setup)
        f'ssh {PI_USER}@{PI_HOST} "cd /home/{PI_USER} && ./llama.cpp/llama-cli -m ./models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -c 2048 -t 4 -ngl 33 --no-display-prompt -p \\"{escaped_prompt}\\""'
    ]
    
    for i, cmd in enumerate(commands):
        try:
            print(f"Trying command format {i+1}: {cmd[:50]}...")
            
            # Run command with timeout
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=30.0  # 30 second timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                continue
            
            if process.returncode == 0 and stdout:
                response = stdout.decode().strip()
                if response:  # Got a valid response
                    print(f"Success with format {i+1}")
                    return response
            else:
                error_msg = stderr.decode().strip()
                print(f"Format {i+1} failed: {error_msg}")
                
        except Exception as e:
            print(f"Format {i+1} error: {str(e)}")
            continue
    
    return "Unable to connect to the Tangnet. Please check the connection and try again."

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

@app.get("/new_session")
def new_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = []
    return {"session_id": session_id}

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    
    # Initialize session if needed
    if session_id not in sessions:
        sessions[session_id] = []
    
    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message", "")
            personality = data.get("personality", "default")
            
            # Add to history
            sessions[session_id].append({"role": "user", "content": message})
            
            # Build prompt with personality
            personality_prompt = PERSONALITIES.get(personality, "")
            full_prompt = f"{personality_prompt}{message}"
            
            # Send typing indicator
            await websocket.send_json({
                "type": "status",
                "content": "Connecting to Pi..."
            })
            
            # Get response from Pi
            response = await run_tangnet_command(full_prompt)
            
            # Add to history
            sessions[session_id].append({"role": "assistant", "content": response})
            
            # Stream response word by word for effect
            words = response.split()
            for i, word in enumerate(words):
                await websocket.send_json({
                    "type": "chunk",
                    "content": word + " " if i < len(words) - 1 else word
                })
                await asyncio.sleep(0.03)  # Small delay for streaming effect
            
            # Send completion
            await websocket.send_json({
                "type": "complete",
                "response": response,
                "history": sessions[session_id][-10:]  # Last 10 messages
            })
            
    except WebSocketDisconnect:
        print(f"Session {session_id} disconnected")

@app.post("/chat")
async def chat_endpoint(session_id: str, message: str, personality: str = "default"):
    """Simple REST endpoint for single messages"""
    if session_id not in sessions:
        sessions[session_id] = []
    
    # Add to history
    sessions[session_id].append({"role": "user", "content": message})
    
    # Build prompt
    personality_prompt = PERSONALITIES.get(personality, "")
    full_prompt = f"{personality_prompt}{message}"
    
    # Get response
    response = await run_tangnet_command(full_prompt)
    
    # Add to history
    sessions[session_id].append({"role": "assistant", "content": response})
    
    return {
        "response": response,
        "session_id": session_id
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Tangnet Chat Server...")
    print(f"Configured to connect to Pi at {PI_USER}@{PI_HOST}")
    print("Make sure you can SSH to the Pi without a password (SSH keys configured)")
    print("\nAccess the chat at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)