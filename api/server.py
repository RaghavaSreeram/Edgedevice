from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "Edge API running"})

@app.route("/record", methods=["POST"])
def record():
    data = request.get_json()
    camera_url = data.get("camera_url")
    output_path = data.get("output_path", "/recordings/default.mp4")
    if not os.path.isdir("/recordings"):
        os.makedirs("/recordings")
    from core import recorder
    proc = recorder.start_recording(camera_url, output_path)
    return jsonify({"recording_pid": proc.pid})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
