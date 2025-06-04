#!/usr/bin/env python3
"""
Tangnet Chat - HTTP API Version
Connects to llama.cpp server running on Pi
Much more reliable than SSH command execution
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import httpx
import asyncio
import json
import uuid
from typing import Dict

app = FastAPI(title="Tangnet API Chat")

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
PI_PORT = 8080
API_BASE = f"http://{PI_HOST}:{PI_PORT}"

# Simple session storage
sessions: Dict[str, list] = {}

class ChatRequest(BaseModel):
    message: str

async def query_llama(prompt: str) -> str:
    """Query the llama.cpp server"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Use the OpenAI-compatible endpoint
            response = await client.post(
                f"{API_BASE}/v1/chat/completions",
                json={
                    "model": "gpt-3.5-turbo",  # llama.cpp ignores this
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 200,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                return f"API Error: {response.status_code} - {response.text}"
                
        except httpx.ConnectError:
            return "Cannot connect to Pi. Make sure llama.cpp server is running on port 8080"
        except httpx.TimeoutException:
            return "Request timed out. The model might be processing a long request."
        except Exception as e:
            return f"Error: {str(e)}"

async def stream_llama(prompt: str, websocket: WebSocket):
    """Stream response from llama.cpp server"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            # Stream the response
            async with client.stream(
                "POST",
                f"{API_BASE}/v1/chat/completions",
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 200,
                    "stream": True
                }
            ) as response:
                full_response = ""
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        if line == "data: [DONE]":
                            break
                        try:
                            data = json.loads(line[6:])
                            if "choices" in data and len(data["choices"]) > 0:
                                content = data["choices"][0].get("delta", {}).get("content", "")
                                if content:
                                    full_response += content
                                    await websocket.send_json({
                                        "type": "chunk",
                                        "content": content
                                    })
                        except json.JSONDecodeError:
                            continue
                
                return full_response
                
        except Exception as e:
            error_msg = f"Streaming error: {str(e)}"
            await websocket.send_json({
                "type": "error",
                "content": error_msg
            })
            return error_msg

@app.get("/")
def root():
    return RedirectResponse(url="/static/simple.html")

@app.get("/health")
async def health_check():
    """Check if we can connect to the llama.cpp server"""
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(f"{API_BASE}/health")
            return {
                "status": "connected",
                "pi": PI_HOST,
                "api": API_BASE,
                "server_status": response.status_code
            }
        except:
            return {
                "status": "disconnected",
                "pi": PI_HOST,
                "api": API_BASE,
                "error": "Cannot reach llama.cpp server"
            }

@app.post("/chat")
async def chat(request: ChatRequest):
    """Simple chat endpoint"""
    response = await query_llama(request.message)
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
            
            # Stream response from llama.cpp
            response = await stream_llama(message, websocket)
            
            # Add to history
            sessions[session_id].append({"role": "assistant", "content": response})
            
            # Send completion
            await websocket.send_json({
                "type": "complete",
                "response": response
            })
            
    except WebSocketDisconnect:
        print(f"Session {session_id} disconnected")
        if session_id in sessions:
            del sessions[session_id]

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Tangnet API Chat Server")
    print(f"📡 Connecting to llama.cpp server at {API_BASE}")
    print("🌐 Access the chat at http://localhost:8000\n")
    print("⚠️  Make sure llama.cpp server is running on the Pi!")
    print(f"   Run: python start_llama_server.py\n")
    
    # Quick health check
    import requests
    try:
        r = requests.get(f"{API_BASE}/health", timeout=2)
        print(f"✅ llama.cpp server is responding!\n")
    except:
        print(f"❌ Cannot reach llama.cpp server at {API_BASE}")
        print("   Please start it first with: python start_llama_server.py\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)