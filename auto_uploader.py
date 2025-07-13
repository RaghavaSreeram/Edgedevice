import os
import requests

def upload_file(file_path, backend_url, token):
    if not os.path.exists(file_path):
        return {"status": "error", "reason": "file not found"}
    with open(file_path, 'rb') as f:
        files = {'video': f}
        headers = {'Authorization': f"Bearer {token}"}
        try:
            response = requests.post(backend_url, files=files, headers=headers)
            return response.json()
        except Exception as e:
            return {"status": "error", "reason": str(e)}
