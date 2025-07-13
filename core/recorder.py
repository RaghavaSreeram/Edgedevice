import subprocess, os, time

def start_ffmpeg_record(rtsp_url, output_path, duration=3600):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-i", rtsp_url,
        "-t", str(duration), "-vcodec", "copy", output_path
    ]
    print(f"Starting recording: {cmd}")
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg recording failed: {e}")
        return False
