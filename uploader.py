# uploader.py – Upload videos to backend with retry and logging

import os
import time
import json
import logging
import requests
import asyncio
from hashlib import sha256
from pathlib import Path

logger = logging.getLogger("uploader")

class UploaderManager:
    def __init__(self, config):
        self.backend_url = config.get("backend_url")
        self.auth_token = config.get("auth_token", "")
        self.upload_dir = config.get("recording", {}).get("output_dir", "./recordings")
        self.uploaded_db = "uploaded_hashes.json"
        self.retry_interval = 180
        self.max_retries = 5
        self.load_uploaded_hashes()

    def load_uploaded_hashes(self):
        if os.path.exists(self.uploaded_db):
            with open(self.uploaded_db, 'r') as f:
                self.uploaded_hashes = json.load(f)
        else:
            self.uploaded_hashes = {}

    def save_uploaded_hashes(self):
        with open(self.uploaded_db, 'w') as f:
            json.dump(self.uploaded_hashes, f)

    def hash_file(self, file_path):
        h = sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    async def start(self):
        while True:
            files = sorted(Path(self.upload_dir).glob("*.mp4"))
            for f in files:
                file_hash = self.hash_file(f)
                if file_hash in self.uploaded_hashes:
                    continue
                success = await self.upload_file(f, file_hash)
                if success:
                    self.uploaded_hashes[file_hash] = f.name
                    self.save_uploaded_hashes()
            await asyncio.sleep(self.retry_interval)

    async def upload_file(self, filepath, file_hash):
        tries = 0
        while tries < self.max_retries:
            try:
                logger.info(f"📤 Uploading {filepath.name} to backend...")
                files = {"file": open(filepath, 'rb')}
                headers = {"Authorization": f"Bearer {self.auth_token}"}
                resp = requests.post(f"{self.backend_url}/api/upload", files=files, headers=headers)
                if resp.status_code == 200:
                    logger.info(f"✅ Uploaded {filepath.name} successfully.")
                    return True
                else:
                    logger.warning(f"⚠️ Upload failed: {resp.status_code} - {resp.text}")
            except Exception as e:
                logger.error(f"❌ Upload error: {e}")
            tries += 1
            await asyncio.sleep(self.retry_interval)
        logger.error(f"⛔ Max retries exceeded for {filepath.name}")
        return False
