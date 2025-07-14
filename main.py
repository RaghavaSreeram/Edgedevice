import time
import logging
from threading import Thread
import subprocess

def start_websocket_server():
    subprocess.run(["python", "websocket/server.py"])

def start_api_server():
    subprocess.run(["python", "api/server.py"])

def start_watchdog():
    while True:
        logging.info("Watchdog: monitoring system health...")
        time.sleep(300)

def main():
    retries = 0
    while retries < 5:
        try:
            logging.info("Starting edge device components...")

            Thread(target=start_websocket_server, daemon=True).start()
            Thread(target=start_api_server, daemon=True).start()
            Thread(target=start_watchdog, daemon=True).start()

            while True:
                time.sleep(10)

        except Exception as e:
            logging.error(f"Main loop failed: {e}")
            retries += 1
            time.sleep(10)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
