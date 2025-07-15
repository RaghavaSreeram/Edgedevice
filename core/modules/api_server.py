
#!/usr/bin/env python3
"""Main API server module"""

import asyncio
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

logger = logging.getLogger(__name__)

app = FastAPI(title="EdgeNVR API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "EdgeNVR API"}

@app.get("/api/status")
async def get_status():
    return {"status": "running", "cameras": 0, "recordings": 0}

def run_server(host="0.0.0.0", port=8080):
    """Run the API server"""
    uvicorn.run(app, host=host, port=port, log_level="info")

if __name__ == "__main__":
    run_server()
