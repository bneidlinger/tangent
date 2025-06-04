"""
Tangnet Chat Server - Windows Version
Designed to work from Windows PowerShell/Command Prompt
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

async def run_tangnet_command(prompt: str) -> str:
    """Run tangnet command on the Pi via SSH"""
    # Simple escape for the prompt
    escaped_prompt = prompt.replace('"', '\\"')
    
    # Determine if we're on Windows
    is_windows = sys.platform.startswith('win') or os.name == 'nt'
    
    # Use the correct path to llama-cli
    llama_path = "/home/brand/tangnet/llama.cpp/build/bin/llama-cli"
    model_path = "/home/brand/tangnet/llama.cpp/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    
    # Build the command - use simpler format
    if is_windows:
        # Windows command - use single quotes for the SSH command
        cmd = f"ssh {PI_USER}@{PI_HOST} '{llama_path} -m {model_path} -c 512 -t 2 -n 50 --simple-io -p \"{escaped_prompt}\"'"
    else:
        # Linux/WSL command
        cmd = f'ssh {PI_USER}@{PI_HOST} "{llama_path} -m {model_path} -c 512 -t 2 -n 50 --simple-io -p \\"{escaped_prompt}\\""'
    
    try:
        print(f"Running command: {cmd[:80]}...")
        
        # Create subprocess
        if is_windows:
            # Use shell=True on Windows to properly handle the command
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
        else:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
        
        # Wait for completion with timeout
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), 
                timeout=120.0  # 120 second timeout for model response
            )
        except asyncio.TimeoutError:
            process.kill()
            print("Command timed out after 120 seconds")
            return "Request timed out. The model took too long to respond."
        
        if stdout:
            response = stdout.decode().strip()
            if response:
                print(f"Got response: {response[:100]}...")
                return response
        
        if stderr:
            error_msg = stderr.decode().strip()
            print(f"Error: {error_msg}")
            
            # Check for common errors
            if "No such file or directory" in error_msg:
                return "Error: Cannot find llama.cpp on the Pi. Please check the installation path."
            elif "command not found" in error_msg:
                return "Error: SSH command failed. Please check your SSH configuration."
            elif "Permission denied" in error_msg:
                return "Error: SSH permission denied. Please set up SSH keys."
                
    except Exception as e:
        print(f"Exception: {str(e)}")
        return f"Error connecting to Tangnet: {str(e)}"
    
    return "No response from the model. Please check the Pi connection."

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

if __name__ == "__main__":
    import uvicorn
    print("Starting Tangnet Chat Server (Windows Version)...")
    print(f"Configured to connect to Pi at {PI_USER}@{PI_HOST}")
    print("Make sure you can SSH to the Pi without a password (SSH keys configured)")
    print("\nAccess the chat at http://localhost:8000")
    
    # Check SSH connectivity
    print("\nTesting SSH connection...")
    test_cmd = f'ssh {PI_USER}@{PI_HOST} "echo Connection successful"'
    try:
        result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✓ SSH connection test passed!")
        else:
            print("✗ SSH connection failed!")
            print("  Please run: ssh-copy-id brand@192.168.1.31")
    except:
        print("✗ SSH test failed")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)