# watchdog.py – Simple system watchdog for core services

import asyncio
import logging
import psutil
import os

logger = logging.getLogger("watchdog")

class Watchdog:
    def __init__(self):
        self.interval = 60  # seconds

    async def monitor(self):
        while True:
            logger.info("🔍 Watchdog check: system health OK")
            self.check_disk()
            self.check_cpu()
            await asyncio.sleep(self.interval)

    def check_disk(self):
        usage = psutil.disk_usage('/')
        percent = usage.percent
        logger.info(f"💽 Disk usage: {percent}%")
        if percent > 90:
            logger.warning("🚨 Disk usage critical (>90%)")

    def check_cpu(self):
        cpu = psutil.cpu_percent(interval=1)
        logger.info(f"🔥 CPU usage: {cpu}%")
        if cpu > 85:
            logger.warning("⚠️ High CPU usage (>85%)")
