# TANGNET Mesh Network Inventory

## 🌐 Network Overview

The TANGNET mesh network consists of AI nodes, sensors, and orchestration servers working together to create a decentralized AI infrastructure.

## 📊 Node Status

| Node Name | Type | IP Address | Role | Status | Specs |
|-----------|------|------------|------|--------|-------|
| tangent-brain | Desktop | 192.168.1.30 | Central AI / Storage / Orchestration | 🔴 Offline | Intel i7, RTX 3070 Ti, 64GB RAM |
| tangent-node-01 | Raspberry Pi 5 | 192.168.1.31 | TinyLlama 1.1B Chat Server | 🟢 Online | 8GB RAM, SSH: brand@192.168.1.31 |
| tangent-node-02 | Raspberry Pi 5 | 192.168.1.43 | Llama 2 7B Deep Inference | 🔴 Offline | 16GB RAM, SSH: brand@192.168.1.43 |

## 🎛️ Devices

| Device Name | Type | IP Address | Role | Status |
|-------------|------|------------|------|--------|
| cam-01 | Camera | 192.168.1.40 | Video stream / Security | 🔴 Offline |
| mic-01 | Microphone | 192.168.1.41 | Audio sensing | 🔴 Offline |
| neutrino-01 | Neutrino Detector | 192.168.1.42 | Data collection | 🔴 Offline |

## 🚀 Future Expansion

| Node Name | Type | IP Address | Role | Notes |
|-----------|------|------------|------|-------|
| future-node-03 | Raspberry Pi | 192.168.1.33 | Expansion slot | Plug and play new node! |

## 📡 Access Commands

```bash
# Access TinyLlama node
ssh brand@192.168.1.31
asktiny "Your question here"

# Access Llama 2 7B node
ssh brand@192.168.1.43
ask7b "Complex query here"
```

## 🔧 Maintenance Notes

- **Last Manual Update**: 2025-01-06
- **Tailscale Integration**: Pending setup
- **Network Type**: Local LAN (future: Tailscale VPN mesh)

---

*This inventory will be automatically updated once Tailscale is configured. For now, it's maintained manually.*