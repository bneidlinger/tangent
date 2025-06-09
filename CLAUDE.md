# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

TANGNET is a decentralized AI cluster project building a 100-node Raspberry Pi network for distributed AI inference. Currently in Phase 1 with a single Pi running TinyLlama.

## Development Commands

### Accessing the Raspberry Pi
```bash
ssh brand@192.168.1.31
```

### Running the Model
```bash
# On the Pi - using the tangnet alias
tangnet "Your prompt here"

# Direct llama.cpp command
./llama.cpp/llama-cli -m models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -c 2048 -t 4 -ngl 33 --no-display-prompt -p "prompt"
```

### Chat API Server
The chat interface is being redesigned. Legacy tanchat system has been archived in `/archive/`.

## Architecture

- **docs/**: All project documentation (HTML & markdown)
  - **setup/**: Configuration and setup instructions
  - **architecture/mesh/**: Mesh network documentation
  - **guides/**: Model setup guides
- **archive/**: Legacy tanchat system (deprecated)
- **llama.cpp/**: (gitignored submodule) The LLM inference engine

## Key Technical Details

- Primary Pi: Raspberry Pi 5 (8GB) at 192.168.1.31
- Model: TinyLlama 1.1B Chat (Q4_K_M quantization)
- Chat API: FastAPI with WebSocket support on port 8000
- Future: 100 Pi nodes + 10 RTX 5090 GPU rigs for Phase 5