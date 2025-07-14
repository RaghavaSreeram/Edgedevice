
import subprocess
import os

def start_ffmpeg_record(rtsp_url, output_path, duration=3600):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cmd = [
            "ffmpeg", "-rtsp_transport", "tcp", "-i", rtsp_url,
            "-t", str(duration), "-vcodec", "copy", output_path
        ]
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Recording failed: {e}")
        return False

