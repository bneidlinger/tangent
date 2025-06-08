# Home Mesh Network Inventory

| Name             | Type         | IP            | Hostname           | Specs/Model           | Role                         | Notes                        |
|------------------|--------------|---------------|--------------------|-----------------------|------------------------------|------------------------------|
| tangent-brain    | Desktop      | 192.168.1.30  | tangent-brain      | 3070 Ti, 64GB, Ubuntu | Central AI/Storage           | LLMs, Docker, media server   |
| tangent-node-01  | Raspberry Pi | 192.168.1.31  | tangent-node-01    | Pi 5, 8GB             | Edge node/Sensors            | General lab Pi               |
| tangent-node-02  | Raspberry Pi | 192.168.1.32  | tangent-node-02    | Pi 5, 16GB            | Edge node/AI/Backup          | High-RAM Pi                  |

## Devices

| Name           | Type             | IP            | Role               | Notes                  |
|----------------|------------------|---------------|--------------------|------------------------|
| cam-01         | Camera           | 192.168.1.40  | Video/Security     | Direct or Pi-connected |
| mic-01         | Microphone       | 192.168.1.41  | Audio Sensing      | For sound/AI analysis  |
| neutrino-01    | Neutrino Detector| 192.168.1.42  | Data collection    | Experimental!          |

## Expansion Plan

- **future-node-03** (192.168.1.33): reserved for new Pi, NUC, or VM

---

_Last updated: 2025-06-06_
