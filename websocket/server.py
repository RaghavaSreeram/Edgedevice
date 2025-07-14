
import asyncio, websockets, json, logging

clients = set()
logging.basicConfig(level=logging.INFO)

async def client_handler(websocket, path):
    clients.add(websocket)
    try:
        async for msg in websocket:
            data = json.loads(msg)
            await asyncio.gather(*[c.send(msg) for c in clients if c != websocket])
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
    finally:
        clients.discard(websocket)

async def main():
    async with websockets.serve(client_handler, "0.0.0.0", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
