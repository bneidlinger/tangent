"""
Tangnet Chat Server - Streaming Version
Real-time streaming from the Pi's model output
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uuid
import asyncio
import subprocess
import json
import sys
import os
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

async def stream_tangnet_response(prompt: str, websocket: WebSocket):
    """Stream response from the Pi in real-time"""
    # Simple escape for the prompt
    escaped_prompt = prompt.replace('"', '\\"').replace("'", "\\'").replace('\n', ' ')
    
    # Build command for streaming - using the working command from docs
    # First cd to the directory, then run llama-cli with relative paths
    cmd = f'''ssh {PI_USER}@{PI_HOST} "cd /home/brand/tangnet/llama.cpp && ./llama-cli -m models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -c 512 -t 4 -n 100 --no-display-prompt -p '{escaped_prompt}'"'''
    
    print(f"\n[DEBUG] Received prompt: {prompt}")
    print(f"[DEBUG] Streaming command: {cmd[:100]}...")
    
    try:
        # Create subprocess for streaming
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            shell=True
        )
        
        # Collect full response
        full_response = ""
        buffer = ""
        
        # Stream stdout
        while True:
            # Read a chunk
            chunk = await process.stdout.read(100)  # Read 100 bytes at a time
            if not chunk:
                break
                
            # Decode and add to buffer
            text = chunk.decode('utf-8', errors='ignore')
            buffer += text
            full_response += text
            
            # Send chunks that look like complete words
            if ' ' in buffer or '\n' in buffer:
                # Send the buffer content
                await websocket.send_json({
                    "type": "chunk",
                    "content": buffer
                })
                buffer = ""
        
        # Send any remaining buffer
        if buffer:
            await websocket.send_json({
                "type": "chunk",
                "content": buffer
            })
        
        # Wait for process to complete
        await process.wait()
        
        # Check for errors
        if process.returncode != 0:
            stderr = await process.stderr.read()
            error_msg = stderr.decode('utf-8', errors='ignore')
            print(f"Error from Pi: {error_msg}")
            if not full_response:
                full_response = f"Error: {error_msg}"
        
        return full_response.strip()
        
    except Exception as e:
        print(f"Streaming error: {str(e)}")
        return f"Error: {str(e)}"

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

@app.get("/test_pi")
async def test_pi():
    """Test endpoint to verify Pi connection"""
    cmd = f'ssh {PI_USER}@{PI_HOST} "echo Connection works && ls -la /home/brand/tangnet/llama.cpp/models/"'
    try:
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            return {"status": "success", "output": stdout.decode()}
        else:
            return {"status": "error", "error": stderr.decode()}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/new_session")
def new_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = []
    return {"session_id": session_id}

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    print(f"\n[DEBUG] WebSocket connected for session: {session_id}")
    
    # Initialize session if needed
    if session_id not in sessions:
        sessions[session_id] = []
    
    try:
        while True:
            data = await websocket.receive_json()
            print(f"[DEBUG] Received WebSocket data: {data}")
            
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
            
            # Stream response from Pi
            response = await stream_tangnet_response(full_prompt, websocket)
            
            # Add to history
            sessions[session_id].append({"role": "assistant", "content": response})
            
            # Send completion
            await websocket.send_json({
                "type": "complete",
                "response": response,
                "history": sessions[session_id][-10:]  # Last 10 messages
            })
            
    except WebSocketDisconnect:
        print(f"[DEBUG] Session {session_id} disconnected")
    except Exception as e:
        print(f"[DEBUG] WebSocket error: {e}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    print("Starting Tangnet Chat Server (Streaming Version)...")
    print(f"Configured to connect to Pi at {PI_USER}@{PI_HOST}")
    print("Make sure you can SSH to the Pi without a password (SSH keys configured)")
    print("\nAccess the chat at http://localhost:8000")
    
    # Check SSH connectivity
    print("\nTesting SSH connection...")
    test_cmd = ['ssh', '-o', 'ConnectTimeout=3', '-o', 'BatchMode=yes', 
               f'{PI_USER}@{PI_HOST}', 'echo "Connection successful"']
    try:
        result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✓ SSH connection test passed!")
            print("\nStarting server...")
        else:
            print("✗ SSH connection failed!")
            print(f"  Error: {result.stderr.strip()}")
            print("\n  To fix this:")
            print("  1. Make sure the Pi is on and accessible")
            print("  2. Run: ssh-copy-id brand@192.168.1.31")
            print("  3. Or run the test script: python test_ssh_windows.py")
            print("\n  Starting server anyway (SSH may work with password)...")
    except subprocess.TimeoutExpired:
        print("✗ SSH test timed out")
        print("  The Pi may be offline or network is slow")
        print("  Starting server anyway...")
    except Exception as e:
        print(f"✗ SSH test error: {e}")
        print("  Starting server anyway...")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)