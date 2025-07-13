<<<<<<< HEAD

#!/usr/bin/env python3
"""WebSocket signaling server for WebRTC"""

import asyncio
import websockets
import json
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store connected clients
clients = set()

async def handle_client(websocket, path):
    """Handle WebSocket client connections"""
    clients.add(websocket)
    logger.info(f"Client connected. Total clients: {len(clients)}")
    
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                logger.info(f"Received message: {data.get('type', 'unknown')}")
                
                # Broadcast message to all other clients
                if clients:
                    await asyncio.gather(
                        *[client.send(message) for client in clients if client != websocket],
                        return_exceptions=True
                    )
                    
            except json.JSONDecodeError:
                logger.error("Invalid JSON received")
            except Exception as e:
                logger.error(f"Error handling message: {e}")
                
    except websockets.exceptions.ConnectionClosed:
        logger.info("Client disconnected")
    finally:
        clients.discard(websocket)
        logger.info(f"Client removed. Total clients: {len(clients)}")

async def main():
    """Start the WebSocket server"""
    host = "0.0.0.0"
    port = 5000
    
    logger.info(f"Starting WebSocket server on {host}:{port}")
    
    async with websockets.serve(handle_client, host, port):
        logger.info("WebSocket server started successfully")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
=======
import asyncio
import websockets
import json
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store connected clients
clients = set()

async def handle_client(websocket, path):
    """Handle WebSocket client connections"""
    clients.add(websocket)
    logger.info(f"Client connected. Total clients: {len(clients)}")
    
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                logger.info(f"Received message: {data.get('type', 'unknown')}")
                
                # Broadcast message to all other clients
                if clients:
                    await asyncio.gather(
                        *[client.send(message) for client in clients if client != websocket],
                        return_exceptions=True
                    )
                    
            except json.JSONDecodeError:
                logger.error("Invalid JSON received")
            except Exception as e:
                logger.error(f"Error handling message: {e}")
                
    except websockets.exceptions.ConnectionClosed:
        logger.info("Client disconnected")
    finally:
        clients.discard(websocket)
        logger.info(f"Client removed. Total clients: {len(clients)}")

async def main():
    """Start the WebSocket server"""
    host = "0.0.0.0"
    port = 5000
    
    logger.info(f"Starting WebSocket server on {host}:{port}")
    
    async with websockets.serve(handle_client, host, port):
        logger.info("WebSocket server started successfully")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
>>>>>>> b809c20241ae6ba5106e22b967c2f935abc7f776
