
import time
import logging
from threading import Thread
import subprocess
import sys
from pathlib import Path

def start_api_server():
    """Start the main WebSocket signaling server"""
    try:
        subprocess.run([sys.executable, "api/server.py"])
    except Exception as e:
        logging.error(f"Failed to start API server: {e}")

def start_watchdog():
    """Monitor system health"""
    while True:
        logging.info("Watchdog: monitoring system health...")
        # Add actual health checks here
        time.sleep(300)

def check_dependencies():
    """Verify required files exist"""
    required_files = [
        "api/server.py",
        "config.yaml", 
        "qr_config.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        logging.error(f"Missing required files: {missing_files}")
        return False
    return True

def main():
    """Main application entry point"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    if not check_dependencies():
        logging.error("Dependency check failed. Exiting.")
        sys.exit(1)
    
    retries = 0
    max_retries = 5
    
    while retries < max_retries:
        try:
            logging.info("Starting edge device components...")

            # Start main API server (handles WebSocket signaling)
            api_thread = Thread(target=start_api_server, daemon=True)
            api_thread.start()
            
            # Start system monitoring
            watchdog_thread = Thread(target=start_watchdog, daemon=True)
            watchdog_thread.start()

            logging.info("All components started successfully")
            
            # Keep main thread alive
            while True:
                time.sleep(10)
                
                # Check if critical threads are still alive
                if not api_thread.is_alive():
                    logging.error("API server thread died, restarting...")
                    raise Exception("API server failed")

        except KeyboardInterrupt:
            logging.info("Shutdown requested by user")
            break
        except Exception as e:
            logging.error(f"Main loop failed: {e}")
            retries += 1
            if retries < max_retries:
                logging.info(f"Retrying in 10 seconds... (attempt {retries}/{max_retries})")
                time.sleep(10)
            else:
                logging.error("Max retries exceeded. Exiting.")
                sys.exit(1)

if __name__ == "__main__":
    main()
