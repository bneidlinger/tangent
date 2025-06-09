#!/usr/bin/env python3
"""
Simple Tangnet Chat Server - Clean, minimal implementation
Works with the Pi running TinyLlama
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import asyncio
import paramiko
import json
import uuid
from typing import Dict

app = FastAPI(title="Tangnet Simple Chat")

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
PI_PASSWORD = None  # Set this if SSH keys aren't configured

# Simple session storage
sessions: Dict[str, list] = {}

class PiConnection:
    """Manages SSH connection to the Pi"""
    def __init__(self):
        self.client = None
        self.connect()
    
    def connect(self):
        """Establish SSH connection"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Try key-based auth first, then password
            try:
                self.client.connect(PI_HOST, username=PI_USER, timeout=10)
                print(f"✓ Connected to Pi via SSH key")
            except:
                if PI_PASSWORD:
                    self.client.connect(PI_HOST, username=PI_USER, password=PI_PASSWORD, timeout=10)
                    print(f"✓ Connected to Pi via password")
                else:
                    raise Exception("SSH key auth failed and no password provided")
                    
        except Exception as e:
            print(f"✗ Failed to connect to Pi: {e}")
            self.client = None
    
    def run_model(self, prompt: str) -> str:
        """Run the model with the given prompt"""
        if not self.client:
            return "Error: Not connected to Pi"
        
        try:
            # Simple prompt escaping - just escape single quotes
            escaped_prompt = prompt.replace("'", "'\"'\"'")
            
            # Direct path to llama-cli (most common location)
            llama_path = "/home/brand/llama.cpp/llama-cli"
            model_path = "/home/brand/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
            
            # Build command with proper parameters
            command = f"{llama_path} -m {model_path} -c 512 -t 4 -n 100 --no-display-prompt -p '{escaped_prompt}'"
            
            print(f"Running command: {command[:50]}...")
            
            # Execute command
            stdin, stdout, stderr = self.client.exec_command(command, timeout=60)
            
            # Get output
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            
            if error and not output:
                print(f"Model error: {error}")
                # Try alternate path
                command = f"/home/brand/llama.cpp/build/bin/llama-cli -m {model_path} -c 512 -t 4 -n 100 --no-display-prompt -p '{escaped_prompt}'"
                print(f"Trying alternate: {command[:50]}...")
                stdin, stdout, stderr = self.client.exec_command(command, timeout=60)
                output = stdout.read().decode().strip()
                error = stderr.read().decode().strip()
                
                if error and not output:
                    return f"Model error: {error}"
                
            return output if output else "No response from model"
            
        except Exception as e:
            print(f"Error running model: {e}")
            # Try to reconnect
            self.connect()
            return f"Error: {str(e)}"

# Global connection
pi_conn = PiConnection()

@app.get("/")
def root():
    return RedirectResponse(url="/static/simple.html")

@app.get("/health")
async def health_check():
    """Check if we can connect to the Pi"""
    if pi_conn.client and pi_conn.client.get_transport() and pi_conn.client.get_transport().is_active():
        return {"status": "connected", "pi": PI_HOST}
    else:
        pi_conn.connect()
        return {"status": "reconnecting", "pi": PI_HOST}

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    """Simple chat endpoint"""
    response = await asyncio.get_event_loop().run_in_executor(
        None, pi_conn.run_model, request.message
    )
    return {"response": response}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    sessions[session_id] = []
    
    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message", "")
            
            # Add to history
            sessions[session_id].append({"role": "user", "content": message})
            
            # Send status
            await websocket.send_json({
                "type": "status",
                "content": "Processing..."
            })
            
            # Get response from Pi
            response = await asyncio.get_event_loop().run_in_executor(
                None, pi_conn.run_model, message
            )
            
            # Add to history
            sessions[session_id].append({"role": "assistant", "content": response})
            
            # Send response
            await websocket.send_json({
                "type": "complete",
                "response": response
            })
            
    except WebSocketDisconnect:
        print(f"Session {session_id} disconnected")
        del sessions[session_id]

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Tangnet Simple Chat Server")
    print(f"📡 Connecting to Pi at {PI_USER}@{PI_HOST}")
    print("🌐 Access the chat at http://localhost:8000\n")
    
    if not PI_PASSWORD:
        print("⚠️  No password set. Using SSH key authentication.")
        print("   If this fails, edit PI_PASSWORD in this file.\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)