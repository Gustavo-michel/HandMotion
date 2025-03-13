from flask import Flask, jsonify, request
from flask_cors import CORS
from handmotion.scripts.handTracking import HandTracking
import queue
import cv2
from flask_socketio import SocketIO, emit
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["chrome-extension://mahcmoailbbfjannahinbdkkibkajbcf", "http://localhost:5000", "*"]}})
socketio = SocketIO(app, cors_allowed_origins="*")

frame_queue = queue.Queue(maxsize=30)
hand_tracker = HandTracking(frame_queue)
gesture_thread = None

@socketio.on('connect')
def on_connect():
    print("Client connected.")

@socketio.on('disconnect')
def on_disconnect():
    print("Client disconnected.")

def process_frame(frame_bytes):
    nparr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if frame is not None:
        frame = cv2.resize(frame, (640, 480))
        frame_queue.put(frame)
        return True
    return False

@socketio.on('frame')
def handle_frame(data):
    """Receive the binary data from the frame

    Args:
        data (Blob, ArrayBuffer): frames in Array via WebSocket.
    """
    if process_frame(data):
        emit("frame_ack", {"message": "Frame received"})
    else:
        emit("frame_error", {"message": "Could not decode image"})

@app.route('/control', methods=['POST'])
def control():
    data = request.json
    action = data.get('action')
    if action == "start":
        result = hand_tracker.start_tracking()
        print(result)
        return jsonify({"status": "Success started"}), 200
    elif action == "stop":
        print("Parando o rastreamento...")
        result = hand_tracker.stop_tracking()
        print(result)
        return jsonify({"status": "Success stopped"}), 200
    return jsonify({"status": "Invalid action"}), 400

@app.route('/status', methods=['GET'])
def status_check():
    """Returns the server status and current gesture."""
    return jsonify({"status": "Active server", "gesture": hand_tracker.gesture or "No gestures detected"}), 200

"""
@app.route('/upload', methods=['POST'])
def upload_frame():
    if request.content_type == "image/jpeg":
        nparr = np.frombuffer(request.data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is not None:
            frame = cv2.resize(frame, (640, 480))
            frame_queue.put(frame)
            return "Frame received and processed.", 200
        else:
            return "Could not decode image", 400
        
    elif 'frame' in request.files:
        file = request.files['frame']
        file_bytes = file.read()
        nparr = np.frombuffer(file_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is not None:
            frame = cv2.resize(frame, (640, 480))
            frame_queue.put(frame)
            return "Frame received and processed.", 200
        else:
            return "Could not decode image", 400
    else:
        return "No frame sent!", 400
"""

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)