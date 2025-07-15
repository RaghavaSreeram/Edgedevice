# Re-Play Edge Device Software v14

## Overview
This is the edge software for capturing, previewing, and uploading sports videos from local Raspberry Pi-based setups.

## Setup
1. Run `bash scripts/install.sh`
2. Place your configuration in `/config/config.yaml` and `/config/qr_config.json`
3. Enable systemd services:
   ```bash
   sudo systemctl enable replay-api
   sudo systemctl enable replay-ws
   ```

## License
MIT
