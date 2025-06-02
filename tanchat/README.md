# Tangnet Chat Application

A modular chat application designed to work with the current Raspberry Pi setup and seamlessly scale to future GPU hardware.

## Features

- **Model Abstraction**: Easy switching between different inference backends (llama.cpp, ollama, vllm)
- **Multiple Personalities**: Rick, Security Bot, Lorekeeper, and more
- **Persistent Chat History**: SQLite database for conversation storage
- **Real-time Streaming**: WebSocket support for live responses
- **Web Interface**: Clean, responsive chat UI built with Tailwind CSS

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your model server in `config.py` or create a `.env` file:
```env
ACTIVE_SERVER=local_pi
LOCAL_PI_URL=http://192.168.1.31:8080
```

3. Run the server:
```bash
python chat_api.py
```

4. Open http://localhost:8000 in your browser

## Architecture

- `chat_api.py`: Main FastAPI application with REST and WebSocket endpoints
- `inference_client.py`: Abstraction layer for different model servers
- `config.py`: Configuration management
- `database.py`: SQLite models for chat persistence
- `static/index.html`: Web chat interface

## Model Switching

To switch between models, simply change the `ACTIVE_SERVER` in your config:
- `local_pi`: Current Raspberry Pi with TinyLlama
- `remote_3080`: Future 3080 GPU server (Mistral 7B, etc.)
- `ollama`: Ollama server
- `vllm`: vLLM server (coming soon)

## API Endpoints

- `GET /`: Web chat interface
- `POST /chat`: Single message chat
- `POST /chat/stream`: Streaming chat responses
- `WS /ws/{session_id}`: WebSocket for real-time chat
- `GET /new_session`: Create new chat session
- `GET /sessions`: List all sessions
- `GET /sessions/{id}/history`: Get chat history