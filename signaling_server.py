# signaling_server.py – WebSocket signaling server for WebRTC peer connection

import asyncio
import websockets
import json
import logging

logger = logging.getLogger("signaling")
clients = set()

async def handle_client(websocket, path):
    clients.add(websocket)
    logger.info(f"🔌 Client connected. Total clients: {len(clients)}")

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                logger.info(f"📨 Message received: {data.get('type', 'unknown')}")

                # Broadcast to all others
                await asyncio.gather(
                    *[client.send(message) for client in clients if client != websocket],
                    return_exceptions=True
                )
            except json.JSONDecodeError:
                logger.warning("⚠️ Invalid JSON message")
    except websockets.exceptions.ConnectionClosed:
        logger.info("🔌 Client disconnected")
    finally:
        clients.discard(websocket)
        logger.info(f"Remaining clients: {len(clients)}")

async def start_signaling_server(config):
    host = config.get("signaling", {}).get("host", "0.0.0.0")
    port = config.get("signaling", {}).get("port", 5000)
    logger.info(f"📡 Starting signaling server on ws://{host}:{port}")

    async with websockets.serve(handle_client, host, port):
        await asyncio.Future()  # Run forever
