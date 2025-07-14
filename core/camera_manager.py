import subprocess

def discover_rtsp_streams(subnet="192.168.1.0/24"):
    try:
        result = subprocess.check_output(f"nmap -p 554 --open {subnet}", shell=True).decode()
        return [line.split()[-1] for line in result.splitlines() if "Nmap scan report for" in line]
    except Exception as e:
        print(f"Camera discovery error: {e}")
        return []


from onvif import ONVIFCamera
from zeep.exceptions import Fault

def get_rtsp_url(ip, username="admin", password="admin"):
    try:
        cam = ONVIFCamera(ip, 80, username, password)
        media_service = cam.create_media_service()
        profiles = media_service.GetProfiles()
        token = profiles[0].token
        stream_uri = media_service.GetStreamUri({'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}, 'ProfileToken': token})
        return stream_uri.Uri
    except Fault as e:
        print(f"ONVIF error: {e}")
        return None
