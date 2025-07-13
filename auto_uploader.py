import requests, os

def upload_video(file_path, backend_url, token):
    if not os.path.exists(file_path):
        return {"status": "error", "message": "file not found"}
    try:
        with open(file_path, 'rb') as f:
            files = {'video': f}
            headers = {'Authorization': f"Bearer {token}"}
            resp = requests.post(backend_url, files=files, headers=headers)
            return resp.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}
