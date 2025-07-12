import subprocess
import threading
import os

def start_recording(input_url, output_file):
    cmd = [
        "ffmpeg", "-y", "-i", input_url,
        "-t", "3600", "-vcodec", "h264_v4l2m2m",
        output_file
    ]
    return subprocess.Popen(cmd)
