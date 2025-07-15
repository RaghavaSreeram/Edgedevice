# main.py – Entry point for EdgeDevice v13

import asyncio
import logging
from core.modules.config_loader import load_config
from core.modules.camera_manager import discover_rtsp_streams
from core.modules.api_server import start_api_server
from core.modules.signaling_server import start_signaling_server
from core.modules.recorder import RecorderManager
from core.modules.uploader import UploaderManager
from core.modules.watchdog import Watchdog
from core.modules.motion_detector import MotionDetector
from core.modules.storage_cleanup import cleanup_old_videos
from core.modules.logger import init_logger


def main():
    # Setup logging
    logger = init_logger("main")
    logger.info("🚀 Starting EdgeDevice v13...")

    # Load configuration
    config = load_config("config/config.example.yaml", "config/qr_config.json")

    # Discover cameras (RTSP)
    discovered_cameras = discover_rtsp_streams(config.get("network", {}))
    logger.info(f"Discovered {len(discovered_cameras)} RTSP streams")

    # Initialize core services
    recorder_mgr = RecorderManager(discovered_cameras, config)
    uploader_mgr = UploaderManager(config)
    watchdog = Watchdog()
    motion_detector = MotionDetector()

    # Create event loop
    loop = asyncio.get_event_loop()
    loop.create_task(start_api_server(config, recorder_mgr, uploader_mgr))
    loop.create_task(start_signaling_server(config))
    loop.create_task(recorder_mgr.start_all())
    loop.create_task(uploader_mgr.start())
    loop.create_task(motion_detector.start(discovered_cameras))
    loop.create_task(watchdog.monitor())
    loop.create_task(cleanup_old_videos(config))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("🛑 EdgeDevice shutting down...")
    finally:
        loop.stop()


if __name__ == "__main__":
    main()
