import time
import requests

def send_heartbeat(
    device_id: str,
    backend_url: str,
    token: str = None,
    endpoint: str = "/device/ping",
    interval: int = 60,
    timeout: int = 5,
):
    """
    Send a periodic heartbeat to the backend.

    Args:
      device_id:    Unique identifier for this device.
      backend_url:  Base URL (e.g. https://api.example.com).
      token:        Optional Bearer token for auth.
      endpoint:     Path to hit (default '/device/ping').
      interval:     Seconds between pings.
      timeout:      Request timeout in seconds.
    """
    url = backend_url.rstrip("/") + endpoint
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    payload = {"device_id": device_id}

    while True:
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=timeout)
            if r.ok:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Heartbeat OK ({r.status_code})")
            else:
                print(
                    f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Heartbeat failed: "
                    f"{r.status_code} – {r.text}"
                )
        except requests.RequestException as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Heartbeat error:", e)
        time.sleep(interval)
