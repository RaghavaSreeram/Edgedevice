import subprocess
def start_recording(rtsp_url, output_file):
    cmd = ["ffmpeg", "-i", rtsp_url, "-t", "3600", "-vcodec", "copy", output_file]
    return subprocess.Popen(cmd)
