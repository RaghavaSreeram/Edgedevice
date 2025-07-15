# ota_updater.py – Remote-controlled Git pull + restart mechanism

import subprocess
import logging
import os
import sys

REPO_DIR = os.path.abspath(os.path.dirname(__file__) + "/../../")
LOG = logging.getLogger("ota")
logging.basicConfig(level=logging.INFO)

def pull_latest():
    LOG.info("📥 Pulling latest code from Git...")
    try:
        subprocess.check_call(["git", "pull"], cwd=REPO_DIR)
        LOG.info("✅ Git pull successful")
        return True
    except subprocess.CalledProcessError as e:
        LOG.error(f"❌ Git pull failed: {e}")
        return False

def restart_service():
    LOG.info("🔁 Restarting EdgeDevice service...")
    try:
        subprocess.check_call(["sudo", "systemctl", "restart", "edge-core.service"])
    except Exception as e:
        LOG.error(f"❌ Restart failed: {e}")

def ota_update():
    if pull_latest():
        restart_service()

if __name__ == '__main__':
    ota_update()
