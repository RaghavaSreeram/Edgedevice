# storage_cleanup.py – Periodic cleanup of old recordings based on disk usage

import os
import shutil
import logging
import time

RECORDINGS_DIR = "./recordings"
MAX_DISK_USAGE_PERCENT = 80
SLEEP_INTERVAL = 600  # seconds (10 mins)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def get_disk_usage_percent(path):
    total, used, free = shutil.disk_usage(path)
    return (used / total) * 100

def cleanup_oldest_files(path):
    files = sorted(
        [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".mp4")],
        key=lambda x: os.path.getctime(x)
    )
    while get_disk_usage_percent(path) > MAX_DISK_USAGE_PERCENT and files:
        file_to_delete = files.pop(0)
        try:
            os.remove(file_to_delete)
            logging.info(f"🗑 Deleted: {file_to_delete}")
        except Exception as e:
            logging.error(f"❌ Error deleting {file_to_delete}: {e}")

def run_cleanup_loop():
    logging.info("🧹 Starting storage cleanup daemon...")
    while True:
        try:
            usage = get_disk_usage_percent(RECORDINGS_DIR)
            logging.info(f"💾 Disk usage: {usage:.2f}%")
            if usage > MAX_DISK_USAGE_PERCENT:
                cleanup_oldest_files(RECORDINGS_DIR)
        except Exception as e:
            logging.error(f"❌ Cleanup loop error: {e}")
        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    run_cleanup_loop()
