#!/bin/bash
sudo apt update
sudo apt install -y python3-pip ffmpeg libv4l-dev libavcodec-extra
pip3 install -r requirements.txt
