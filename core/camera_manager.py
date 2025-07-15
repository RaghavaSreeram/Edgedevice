# camera_manager.py – Discover cameras using subnet scan + ONVIF

import socket
import logging
from onvif import ONVIFCamera
import ipaddress
import subprocess
import xml.etree.ElementTree as ET

logger = logging.getLogger("camera_manager")

def ping_ip(ip):
    try:
        output = subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output.returncode == 0
    except Exception as e:
        logger.warning(f"Ping failed for {ip}: {e}")
        return False

def discover_rtsp_streams(network_cfg):
    discovered = []
    subnet = network_cfg.get("subnet", "192.168.1.0/24")
    ports = network_cfg.get("ports", [554])

    logger.info(f"🔍 Scanning subnet {subnet} for cameras on ports {ports}...")
    
    for ip in ipaddress.IPv4Network(subnet):
        ip = str(ip)
        if not ping_ip(ip):
            continue
        for port in ports:
            if check_rtsp_port(ip, port):
                rtsp_url = f"rtsp://{ip}:{port}/"
                logger.info(f"📸 RTSP camera found: {rtsp_url}")
                discovered.append({
                    "ip": ip,
                    "port": port,
                    "rtsp_url": rtsp_url,
                })
    return discovered

def check_rtsp_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception as e:
        logger.warning(f"Error checking RTSP port {ip}:{port} - {e}")
        return False

# Optional ONVIF expansion (if needed later)
def get_onvif_profiles(ip, port=80, user='admin', password='admin'):
    try:
        cam = ONVIFCamera(ip, port, user, password)
        media = cam.create_media_service()
        profiles = media.GetProfiles()
        return [p.token for p in profiles]
    except Exception as e:
        logger.warning(f"ONVIF failed for {ip}: {e}")
        return []
