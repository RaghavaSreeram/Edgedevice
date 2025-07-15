# recorder.py – FFmpeg recording management for each camera

import asyncio
import os
import subprocess
import logging
from datetime import datetime

logger = logging.getLogger("recorder")

class RecorderManager:
    def __init__(self, cameras, config):
        self.cameras = cameras
        self.config = config
        self.recording_duration = config.get("recording", {}).get("duration", 3600)  # in seconds
        self.output_dir = config.get("recording", {}).get("output_dir", "./recordings")
        self.processes = {}

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    async def start_all(self):
        logger.info("🎬 Starting recording for all cameras...")
        for cam in self.cameras:
            asyncio.create_task(self.record(cam))

    async def record(self, cam):
        cam_id = cam.get("ip")
        while True:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{cam_id.replace('.', '_')}_{timestamp}.mp4"
            filepath = os.path.join(self.output_dir, filename)

            rtsp_url = cam.get("rtsp_url")
            cmd = [
                "ffmpeg", "-rtsp_transport", "tcp", "-i", rtsp_url,
                "-t", str(self.recording_duration),
                "-c:v", "copy", "-c:a", "aac", filepath
            ]

            try:
                logger.info(f"📹 Recording started for {cam_id} to {filename}")
                proc = await asyncio.create_subprocess_exec(*cmd)
                self.processes[cam_id] = proc
                await proc.communicate()
                logger.info(f"✅ Recording finished for {cam_id}")
            except Exception as e:
                logger.error(f"❌ Failed to record {cam_id}: {e}")
            await asyncio.sleep(2)  # buffer before restarting

    def stop(self, cam_id):
        proc = self.processes.get(cam_id)
        if proc:
            proc.terminate()
            logger.info(f"🛑 Recording manually stopped for {cam_id}")
