from flask import Flask, jsonify, request
from flask_cors import CORS
from handmotion.scripts.handTracking import HandTracking
from flask_socketio import SocketIO, emit
import cv2
import base64
import os

port = int(os.getenv("PORT", 5000))

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["chrome-extension://bgmanlokleejebndadmkkfibihjddpaf", "http://localhost:5000", "*"]}})
socketio = SocketIO(app, cors_allowed_origins="*")

hand_tracker = HandTracking()

@app.route('/control', methods=['POST'])
def control():
    """control start/stop of tracking.

    Returns:
        Json: _status of process
    """
    data = request.json
    action = data.get('action')
    if action == "start":
        result = hand_tracker.start_tracking()
        print(result)
        return jsonify({"status": "Success started"}), 200
    elif action == "stop":
        result = hand_tracker.stop_tracking()
        print(result)
        return jsonify({"status": "Success stopped"}), 200
    return jsonify({"status": "Invalid action"}), 400

@socketio.on('connect')
def on_connect():
    print("Client connected.")

@socketio.on('disconnect')
def on_disconnect():
    print("Client disconnected.")

@socketio.on('frame')
def handle_frame(data):
    """
    Receives the frame in binary format, inserts it into the queue and sends the processed frame.
    """
    if hand_tracker:
        hand_tracker.add_frame(data)
        if hand_tracker.processed_frame is not None:
            flipped_frame = cv2.flip(hand_tracker.processed_frame, 1)
            _, buffer = cv2.imencode('.jpg', flipped_frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            emit("processed_frame", {"frame": jpg_as_text}, broadcast=True)
        else:
            emit("frame_error", {"message": "No processed frames available"})
    else:
        emit("frame_error", {"message": "Hand Tracker not initialized"})


@app.route('/status', methods=['GET'])
def status_check():
    """
    Returns the server status and current gesture.
    """
    return jsonify({"status": "Active server", "gesture": hand_tracker.gesture or "No gestures detected"}), 200


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=port, allow_unsafe_werkzeug=True)