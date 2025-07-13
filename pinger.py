# Send heartbeat to backend
import requests, time

def send_heartbeat(device_id, backend_url, token, interval=60):
    url = f"{backend_url}/device/ping"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"device_id": device_id}
    while True:
        try:
            r = requests.post(url, json=payload, headers=headers)
            print(f"Heartbeat sent: {r.status_code}")
        except Exception as e:
            print(f"Heartbeat error: {e}")
        time.sleep(interval)
