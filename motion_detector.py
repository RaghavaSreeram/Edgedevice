# motion_detector.py – Simple motion detection using frame differencing

import cv2
import asyncio
import logging

logger = logging.getLogger("motion")

class MotionDetector:
    def __init__(self):
        self.running = True

    async def start(self, cameras):
        for cam in cameras:
            asyncio.create_task(self.detect_motion(cam))

    async def detect_motion(self, cam):
        cam_id = cam.get("ip")
        rtsp_url = cam.get("rtsp_url")

        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            logger.warning(f"⚠️ Unable to open camera: {cam_id}")
            return

        _, prev_frame = cap.read()
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY) if prev_frame is not None else None

        while self.running:
            ret, frame = cap.read()
            if not ret or frame is None:
                await asyncio.sleep(1)
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if prev_gray is not None:
                diff = cv2.absdiff(prev_gray, gray)
                _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
                motion = cv2.countNonZero(thresh)
                if motion > 50000:
                    logger.info(f"🚨 Motion detected on {cam_id} ({motion} pixels)")

            prev_gray = gray
            await asyncio.sleep(1)

        cap.release()
        logger.info(f"🔻 Stopped motion detection on {cam_id}")
