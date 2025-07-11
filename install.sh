#!/bin/bash
sudo apt update
sudo apt install -y python3-pip ffmpeg libv4l-dev libavcodec-extra
pip3 install flask requests onvif-zeep websockets aiortc prometheus_client pyyaml ffmpeg-python psutil
