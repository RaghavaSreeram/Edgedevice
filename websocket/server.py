import asyncio, websockets
async def handler(ws, path): await ws.send("WebSocket signaling active")
def run(): asyncio.get_event_loop().run_until_complete(websockets.serve(handler, "0.0.0.0", 8765)); asyncio.get_event_loop().run_forever()
if __name__ == "__main__": run()
