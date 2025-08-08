# 🧠 TANGNET - Decentralized AI Cluster

<div align="center">
  <img src="docs/assets/images/picluster.png" alt="TANGNET Architecture" width="600">
  
  [![Phase](https://img.shields.io/badge/Phase-1%20of%205-blue)](https://github.com/bneidlinger/tangent)
  [![Model](https://img.shields.io/badge/Model-TinyLlama%201.1B-green)](https://github.com/bneidlinger/tangent)
  [![Nodes](https://img.shields.io/badge/Current%20Nodes-1-orange)](https://github.com/bneidlinger/tangent)
  [![Target](https://img.shields.io/badge/Target%20Nodes-100-red)](https://github.com/bneidlinger/tangent)
  
  ![Mesh Status](docs/mesh-status.svg)
  
  **Building a 100-node Raspberry Pi cluster for distributed AI inference**
  
  ### 🌐 [View Live Project Site](https://bneidlinger.github.io/tangent/)
</div>

## 🌟 Overview

TANGNET (Tangential Network) is an ambitious project to create a fully offline-capable AI infrastructure combining edge computing with powerful GPU acceleration. No cloud dependencies, complete autonomy.

### 🎯 Project Goals

- **100 Raspberry Pi 5 units** (8GB) for distributed edge computing
- **10 RTX 5090 GPU rigs** for heavy inference tasks  
- Voice transcription, document retrieval, and AI inference
- Completely self-contained synthetic intelligence ecosystem
- Zero reliance on external APIs or cloud services

## 🚀 Quick Start

### Access the Current Node

```bash
# SSH into the primary Pi (replace with your Pi's IP)
ssh user@<pi-ip-address>

# Run inference using the tangnet alias
tangnet "What is the meaning of life?"
```

### AI Interface

The project includes:
- FastAPI-based chat server with WebSocket support
- Legacy tanchat system (archived in `/archive/`)
- Direct llama.cpp command-line interface

## 🌐 Live Mesh Network Status

View the [Live Mesh Inventory](docs/mesh-inventory-auto.md) for real-time node status.

### Network Architecture
- **Control Node** - Central orchestration with GPU acceleration
- **Edge Nodes** - Raspberry Pi 5 units for distributed inference
- **Mesh Network** - Tailscale VPN for secure node communication

## 📊 Current Progress

### ✅ Phase 1: Single Node (Complete)
- Raspberry Pi 5 (8GB) operational
- TinyLlama 1.1B model deployed (Q4_K_M quantization)
- ~10-15 tokens/second inference
- Custom chat API with WebSocket support
- Remote access configured via SSH/VNC

### 🔄 Phase 2: Mini Cluster (In Progress)
- Adding 4 additional Pi nodes
- Implementing job distribution
- Building monitoring dashboard
- Integrating RTX 3080 GPU server

## 🏗️ Architecture

```
TANGNET Infrastructure
├── Edge Nodes (Raspberry Pi 5)
│   ├── Inference Engine (llama.cpp)
│   ├── Local Model Storage
│   └── Mesh Networking (Tailscale)
├── GPU Acceleration Layer
│   ├── RTX 3080 Server (Phase 2)
│   └── RTX 5090 Rigs (Phase 5)
└── Control Plane
    ├── FastAPI Chat Server
    ├── WebSocket Real-time Streaming
    └── Distributed Job Queue
```

## 🛠️ Technical Stack

### Hardware
- **Current**: 1x Raspberry Pi 5 (8GB RAM)
- **Phase 5**: 100x Pi 5 + 10x RTX 5090 rigs
- **Networking**: Gigabit Ethernet mesh
- **Storage**: Distributed across nodes

### Software
- **Inference**: llama.cpp (ARM-optimized)
- **API**: FastAPI + WebSockets
- **Models**: TinyLlama 1.1B (expanding to Llama 3, Mixtral)
- **Mesh**: Tailscale VPN
- **OS**: Raspberry Pi OS Lite

## 📈 Performance Metrics

| Metric | Current | Target (Phase 5) |
|--------|---------|------------------|
| Nodes | 1 | 100 |
| Models | TinyLlama 1.1B | Multiple 70B+ |
| Inference Speed | 10-15 tok/s | 1000+ tok/s |
| Availability | Single node | 99.9% uptime |
| Power Draw | ~10W | ~5kW total |

## 🗺️ Roadmap

<details>
<summary><b>Phase 2: 5-Node Mini Cluster</b></summary>

- [ ] Deploy 4 additional Pi nodes
- [ ] Implement basic load balancing
- [ ] Add RTX 3080 GPU server
- [ ] Create monitoring dashboard
- [ ] Test multi-node inference

</details>

<details>
<summary><b>Phase 3: 10-Node AI Stack</b></summary>

- [ ] Distributed vector database (ChromaDB)
- [ ] Job queue management system
- [ ] Persistent conversation memory
- [ ] API gateway with auth
- [ ] Automated model deployment

</details>

<details>
<summary><b>Phase 4: 25-Node Regional Cluster</b></summary>

- [ ] Zone-based architecture
- [ ] Redundancy and auto-failover
- [ ] Advanced load distribution
- [ ] Real-time performance monitoring
- [ ] Voice command integration

</details>

<details>
<summary><b>Phase 5: 100-Node TANGNET GRIDCORE</b></summary>

- [ ] Full 100 Pi deployment
- [ ] 10x RTX 5090 GPU rigs
- [ ] Cluster-wide message bus
- [ ] Complete offline operation
- [ ] Multi-modal AI capabilities

</details>

## 📚 Documentation

### Core Documentation
- [Project Overview](docs/index.html) - Vision and goals
- [Setup Guide](docs/guide.html) - Step-by-step Pi configuration
- [Hardware Specs](docs/materials.html) - Complete parts list
- [Mesh Network](docs/architecture/mesh/mesh_network.md) - Node inventory and topology

### Additional Resources
- **Setup Guides**: Model setup, Tailscale configuration, hardware integration
- **Architecture Docs**: 2-Pi setup, future cluster designs, mesh networking
- **API Documentation**: Chat server, WebSocket interfaces, inference endpoints

### Project Structure
- `llama.cpp/` - Core inference engine (gitignored submodule)
- `docs/` - All project documentation
- `archive/` - Legacy systems and deprecated code
- `inventory/` - Hardware inventory and network configurations
- `UFOglintdetector/` - Experimental modules

## 🤝 Contributing

While this is currently a personal project, contributions are welcome! Areas of interest:

- Distributed inference algorithms
- Web UI improvements
- Performance optimizations
- Documentation and tutorials
- Hardware recommendations

## 📜 License

This project is open source. License TBD.

## 👨‍💻 Creator

Built by **Brandon** - Powered by curiosity, caffeine, and the relentless pursuit of decentralized AI.

---

<div align="center">
  <i>"TANGNET isn't just a cluster — it's a bunker-grade synthetic brain."</i>
  
  ⭐ Star this repo to follow the journey from 1 to 100 nodes!
</div>