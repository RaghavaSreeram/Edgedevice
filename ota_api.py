# ota_api.py – Trigger OTA update from HTTP REST request

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ota_updater import ota_update
import uvicorn

app = FastAPI()

class UpdateRequest(BaseModel):
    token: str

VALID_TOKEN = "secure_token_here"  # Replace with your actual token

@app.post("/api/ota/update")
def trigger_ota(request: UpdateRequest):
    if request.token != VALID_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

    try:
        ota_update()
        return {"status": "success", "message": "OTA update triggered"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {e}")

if __name__ == "__main__":
    uvicorn.run("ota_api:app", host="0.0.0.0", port=8600)
