import asyncio, websockets
async def handler(ws): await ws.send("WebSocket ready")
async def main(): await websockets.serve(handler, "0.0.0.0", 8765)
asyncio.run(main())
