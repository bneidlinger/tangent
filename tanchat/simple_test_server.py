"""
Simple test server without model dependencies
For testing the chat interface before connecting to the Pi
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uuid
import asyncio
import random

app = FastAPI(title="Tangnet Chat Test Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Test responses
TEST_RESPONSES = [
    "I'm running on a simulated Pi cluster!",
    "The Tangnet is growing stronger every day.",
    "Processing your request through the neural mesh...",
    "My circuits are humming with anticipation!",
    "Quantum entanglement achieved. Response incoming.",
]

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

@app.get("/new_session")
def new_session():
    return {"session_id": str(uuid.uuid4())}

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message", "")
            personality = data.get("personality", "default")
            
            # Simulate processing delay
            await asyncio.sleep(0.5)
            
            # Generate test response based on personality
            if personality == "rick":
                response = f"*burp* Listen Morty, '{message}' is the dumbest thing I've heard all day. *burp*"
            elif personality == "security":
                response = f"SECURITY ANALYSIS: Message '{message}' scanned. No threats detected. Proceed with caution."
            elif personality == "lorekeeper":
                response = f"Ah, traveler, you speak of '{message}'. The ancient texts foretold of such queries..."
            else:
                response = random.choice(TEST_RESPONSES)
            
            # Send streaming response
            words = response.split()
            for i, word in enumerate(words):
                await websocket.send_json({
                    "type": "chunk",
                    "content": word + " " if i < len(words) - 1 else word
                })
                await asyncio.sleep(0.05)  # Simulate streaming
            
            await websocket.send_json({
                "type": "complete",
                "response": response,
                "history": []
            })
            
    except WebSocketDisconnect:
        print(f"Session {session_id} disconnected")

if __name__ == "__main__":
    import uvicorn
    print("Starting Tangnet Chat Test Server...")
    print("This is a test server without real AI models.")
    print("Access the chat at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)