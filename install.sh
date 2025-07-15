#!/bin/bash
# install.sh – Setup EdgeDevice environment with dependencies and cleanup service

set -e

# Logging
echo "🚀 Installing EdgeDevice dependencies..."

# Update & install base packages
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-pip python3-opencv ffmpeg libyaml-dev nmap git curl

# Optional: Install Docker & Docker Compose
if ! command -v docker &> /dev/null; then
  echo "🐳 Installing Docker..."
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo usermod -aG docker $USER
fi

if ! command -v docker-compose &> /dev/null; then
  echo "📦 Installing docker-compose..."
  sudo apt-get install -y docker-compose
fi

# Install Python dependencies
pip3 install -r requirements.txt

# Create necessary folders
mkdir -p recordings config logs tmp backup

# Copy sample config
cp -n config/config.example.yaml config/config.yaml

# Create systemd service for cleanup daemon
cat <<EOF | sudo tee /etc/systemd/system/edge-cleanup.service
[Unit]
Description=EdgeDevice Storage Cleanup Daemon
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/edge_device/core/modules/storage_cleanup.py
WorkingDirectory=/home/pi/edge_device
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOF

# Enable the cleanup daemon
sudo systemctl daemon-reexec
sudo systemctl enable edge-cleanup.service
sudo systemctl start edge-cleanup.service

echo "✅ Install complete. Reboot may be required to finalize Docker setup."
