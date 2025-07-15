# Re-Play EdgeDevice

⚙️ **Version**: v13+ (Production Ready)
📅 **Updated**: July 2025

---

## 🔥 Overview
Re-Play EdgeDevice is an AI-ready, camera-aware smart edge solution for sports venues. It captures, processes, and uploads video data with live preview capabilities, OTA updates, and full configuration via QR or backend provisioning.

---

## 📦 Key Features

| Feature                    | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| 🎥 RTSP Camera Discovery   | Auto-detects cameras via ONVIF + Nmap + manual port check                   |
| 📡 WebRTC Live Preview     | P2P live stream via WebRTC using WebSocket signaling server                 |
| 🧠 Motion Detection        | Simple motion detection on frames using OpenCV                              |
| ⏺ Video Recording         | FFmpeg-based video capture with watchdog process                            |
| ☁️ Upload to Backend       | Background uploader with retries + hash verification                        |
| 🧹 Storage Management      | Auto cleanup when disk > threshold                                          |
| 🔐 QR/YAML Config Merge    | Load config via YAML + override with QR JSON config                         |
| 🌐 REST API + WS Control   | FastAPI HTTP control and WebSocket signaling server                         |
| 🚀 OTA Updates             | Trigger git pull + restart remotely via secure token                        |
| 🐳 Docker Ready            | Docker Compose-based deployment with persistent storage                     |

---

## 📁 Folder Structure

```
/recordings              → Saved video clips
/config                  → YAML config and QR config
/core/modules            → All services: recorder, uploader, motion, cleanup, API
/install.sh              → Bootstrap setup on Raspberry Pi
/docker-compose.yaml     → Multi-service orchestration
/storage_cleanup.py      → Systemd-monitored disk cleanup script
/ota_updater.py          → Git pull + systemctl restart logic
/ota_api.py              → REST endpoint to trigger OTA remotely
```

---

## 🛠 Setup Instructions

### 📌 Requirements
- Raspberry Pi OS (Lite preferred)
- Python 3.12+
- FFmpeg
- OpenCV
- Docker + docker-compose

### 🔧 Install
```bash
git clone https://github.com/RaghavaSreeram/Edgedevice.git
cd Edgedevice
chmod +x install.sh
./install.sh
```

---

## 🚀 Running

### 🔁 Systemd
```bash
sudo systemctl enable edge-core.service
sudo systemctl start edge-core.service
```

### 🐳 Docker Compose
```bash
docker-compose up -d
```

### 🌐 REST API
```bash
curl -X POST http://localhost:8600/api/ota/update -H "Content-Type: application/json" -d '{"token": "your-token"}'
```

---

## ✅ Requirements.txt
```
aiortc==1.4.0
opencv-python
fastapi
uvicorn
websockets
PyYAML
requests
nmap
python-multipart
```

---

## 🔒 Security & Logging
- Token-secured OTA
- JSON logging format (stdout and `logs/`)
- All modules log errors, warnings, and operational state

---

## 📍 Versioning
- `device_id`, `camera_id` and `version` are stored in persistent config
- OTA tracks Git version and restart logs

---

## 🤖 Roadmap
- [ ] AI analytics pipeline (e.g., player tracking)
- [ ] Video annotation tools
- [ ] Real-time scoreboard overlays
- [ ] Integration with Re-Play React Native app

---

## 👥 Contributors
- @RaghavaSreeram (Founder, Architect)
- @OpenAI + geerlingguy/pi-nvr (base architecture inspiration)

---

## 📜 License
MIT (to be added in `LICENSE` file)
