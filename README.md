# 🧠 TANGNET - Decentralized AI Cluster Project

TANGNET is an ambitious project to build a 100-node Raspberry Pi cluster for distributed AI inference, combining edge computing with powerful GPU nodes to create a self-contained synthetic intelligence ecosystem.

## 🌟 Project Vision

TANGNET (Tangential Network) aims to create a fully offline-capable AI infrastructure that includes:
- **100 Raspberry Pi 5 units** (8GB) for distributed edge computing
- **10 RTX 5090 GPU rigs** for heavy inference tasks
- Voice transcription, document retrieval, and AI inference capabilities
- No reliance on cloud APIs - complete autonomy

## 📁 Project Structure

```
tangnet/
├── overview/              # Project documentation and vision
│   ├── index.html        # About the project and creator
│   ├── guide.html        # Pi setup and usage guide
│   ├── implementationidea.html  # Phase-by-phase implementation plan
│   ├── materials.html    # Hardware requirements and build manual
│   └── modeloverview.html # Model details and commands
├── set-up docs/          # Configuration and setup documentation
│   ├── cana_setup.html   # Setup instructions
│   ├── dets.txt          # Network and command details
│   └── modelsetup.html   # Model configuration
├── tanchat/              # Custom chat API implementation
│   ├── chatapi.py        # FastAPI WebSocket chat server
│   └── requirements.txt  # Python dependencies
└── llama.cpp/            # (gitignored) LLM inference engine
```

## 🚀 Current Status

### Phase 1: Single Pi Setup ✅
- Raspberry Pi 5 (8GB) running at IP: `192.168.1.31`
- TinyLlama 1.1B Chat model deployed via llama.cpp
- SSH and VNC access configured
- Basic inference working with custom alias

### In Development
- FastAPI-based chat API with WebSocket support
- Web interface for cluster management
- Integration with llama.cpp for real-time inference

## 🛠️ Quick Start

### Accessing the Pi
```bash
# SSH into the Pi
ssh brand@192.168.1.31

# Use the tangnet alias for quick inference
tangnet "What is the meaning of life?"
```

### Running the Chat API
```bash
cd tanchat
pip install -r requirements.txt
python chatapi.py
```

The API will be available at `http://localhost:8000` with WebSocket support at `/ws/{session_id}`.

## 📋 Requirements

### Hardware (Current)
- Raspberry Pi 5 (8GB RAM)
- 32GB+ microSD card
- USB-C power supply (27W)
- Gigabit Ethernet connection

### Software
- Raspberry Pi OS Lite or Ubuntu Server ARM
- Python 3.10+
- llama.cpp (compiled for ARM)
- FastAPI, Uvicorn, WebSockets

## 🔧 Build Commands

### On the Pi
```bash
# Check temperature
vcgencmd measure_temp

# Navigate to llama.cpp
cd ~/tangnet/llama.cpp/build

# Run inference
./bin/llama-run ../tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf "Your prompt"
```

### Model Management
```bash
# Download new models
huggingface-cli download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF \
  tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
  --local-dir . \
  --local-dir-use-symlinks False
```

## 🗺️ Roadmap

1. **Phase 2**: 5-Node Mini Cluster
   - Multi-node coordination
   - Basic job distribution
   - HTML monitoring dashboard

2. **Phase 3**: 10-Node AI Stack
   - Distributed services (ChromaDB, FastAPI)
   - Job queue management
   - Persistent logging

3. **Phase 4**: 25-Node Regional Cluster
   - Zone-based architecture
   - Redundancy and failover
   - Memory integration

4. **Phase 5**: 100-Node TANGNET GRIDCORE
   - Full AI mesh deployment
   - Cluster-wide message bus
   - Voice command layer
   - Complete offline operation

## 🤝 Contributing

This is currently a personal project, but contributions and ideas are welcome. Feel free to open issues or submit PRs.

## 📜 License

This project is open source. Specific license to be determined.

## 🧪 Creator

Created by Brandon. Powered by curiosity, caffeine, and cold solder joints.

---

*"TANGNET isn't just a build — it's a bunker-grade synthetic brain."*