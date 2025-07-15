import socket
import threading
import time
from queue import Queue
from onvif import ONVIFCamera
import requests

# Configuration
SUBNET = "192.168.1."
PORT = 554
TIMEOUT = 1
MAX_THREADS = 50

def is_port_open(ip, port=PORT, timeout=TIMEOUT):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except:
        return False

def rtsp_options_check(ip, port=PORT):
    try:
        url = f"rtsp://{ip}:{port}/"
        response = requests.options(url, timeout=TIMEOUT)
        return response.status_code == 200
    except:
        return False

def get_onvif_info(ip):
    try:
        camera = ONVIFCamera(ip, 80, 'admin', 'admin')  # Default credentials, can be changed
        device_info = camera.devicemgmt.GetDeviceInformation()
        return device_info.Model
    except:
        return "Unknown"

def get_camera_info(ip):
    model = get_onvif_info(ip)
    rtsp_valid = rtsp_options_check(ip)
    return {
        "ip": ip,
        "model": model,
        "rtsp_valid": rtsp_valid,
        "status": "active" if rtsp_valid else "inactive"
    }

def worker(queue, results):
    while not queue.empty():
        ip = queue.get()
        if is_port_open(ip):
            results.append(get_camera_info(ip))
        queue.task_done()

def scan_subnet(subnet_prefix=SUBNET, port=PORT):
    ip_queue = Queue()
    results = []

    for i in range(1, 255):
        ip_queue.put(f"{subnet_prefix}{i}")

    threads = []
    for _ in range(min(MAX_THREADS, ip_queue.qsize())):
        thread = threading.Thread(target=worker, args=(ip_queue, results))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return results

if __name__ == "__main__":
    print("Scanning for RTSP-enabled devices with ONVIF model info...")
    camera_list = scan_subnet()
    for camera in camera_list:
        print(f"Discovered camera: {camera['ip']} - {camera['model']} (RTSP valid: {camera['rtsp_valid']})")
