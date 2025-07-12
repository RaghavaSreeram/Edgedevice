import time, requests
def send_heartbeat(device_id, backend_url):
    while True:
        try:
            requests.post(f"{backend_url}/api/heartbeat", json={"device_id": device_id})
        except Exception as e:
            print("Ping failed:", e)
        time.sleep(10)
