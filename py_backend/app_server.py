import os
import subprocess
import signal
from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS
from flask_socketio import SocketIO
from nii_to_ply_converter import convert_single_nii

import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://10.1.5.50:3000"], supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000", "http://10.1.5.50:3000"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Track the virtual mouse subprocess globally
virtual_mouse_process = None

@app.route("/outputs/<path:filename>")
def serve_output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route("/start-virtual-mouse", methods=["POST"])
def start_virtual_mouse():
    global virtual_mouse_process
    try:
        if virtual_mouse_process is None or virtual_mouse_process.poll() is not None:
            virtual_mouse_process = subprocess.Popen(["python", "py_backend/virtual_mouse.py"])
            logging.info("Virtual mouse started.")
            return jsonify({"status": "Virtual mouse started"}), 200
        else:
            return jsonify({"status": "Already running"}), 200
    except Exception as e:
        logging.error(f"Failed to start virtual mouse: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/stop-virtual-mouse", methods=["POST"])
def stop_virtual_mouse():
    global virtual_mouse_process
    try:
        if virtual_mouse_process and virtual_mouse_process.poll() is None:
            virtual_mouse_process.terminate()
            virtual_mouse_process.wait()
            virtual_mouse_process = None
            logging.info("Virtual mouse stopped.")
            return jsonify({"status": "Virtual mouse stopped"}), 200
        else:
            return jsonify({"status": "Not running"}), 200
    except Exception as e:
        logging.error(f"Failed to stop virtual mouse: {e}")
        return jsonify({"error": str(e)}), 500

@socketio.on("connect")
def handle_connect():
    print("WebSocket client connected")

@app.route("/upload", methods=["POST"])
def upload_nii():
    file = request.files.get("file")
    if not file:
        print("UPLOAD ERROR: No file uploaded.")
        return make_response(jsonify({"error": "Please upload a NIfTI file"}), 400)

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    print(f"UPLOAD: Saving to {filepath}")
    file.save(filepath)

    try:
        convert_single_nii(filepath, OUTPUT_FOLDER, output_filename="brain_final.ply")
    except Exception as e:
        print("UPLOAD ERROR:", e)
        return make_response(jsonify({"error": f"Failed to convert: {str(e)}"}), 500)

    model_url = "/outputs/brain_final.ply"
    public_url = f"http://10.1.5.50:5000{model_url}"
    print("Emitting model update to clients:", public_url)
    socketio.emit("model_update", {"modelUrl": public_url})

    response = jsonify({"model_url": model_url})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    app.debug = True
    app.config['PROPAGATE_EXCEPTIONS'] = True
    socketio.run(app, debug=True, port=5000, host="0.0.0.0", allow_unsafe_werkzeug=True)
