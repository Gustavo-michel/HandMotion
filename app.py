from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
from handmotion.scripts.handTracking import HandTracking
from flask_socketio import SocketIO
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins=["chrome-extension://mahcmoailbbfjannahinbdkkibkajbcf", "*"])

hand_tracker = HandTracking()
gesture = None

tracking_active = False
tracking_thread = None

def track_gestures():
    global gesture
    
    while tracking_active:
        gesture = hand_tracker.run()
        time.sleep(0.1) 

@app.route('/control', methods=['POST'])
def control():
    global tracking_thread, tracking_active
    data = request.json
    action = data.get('action')

    if action == "start":
        if tracking_active:
            return jsonify({"status": "Tracking already started."}), 200
        try:
            tracking_active = True
            tracking_thread = threading.Thread(target=track_gestures, daemon=True)
            tracking_thread.start()
            return jsonify({"status": "Success started"}), 200
        except Exception as e:
            return jsonify({"status": "Error when starting the app", "error": str(e)}), 500

    elif action == "stop":
        if not tracking_active:
            return jsonify({"status": "Tracking already stopped."}), 200
        try:
            tracking_active = False
            tracking_thread.join()
            tracking_thread = None
            return jsonify({"status": "Success stopped"}), 200
        except Exception as e:
            return jsonify({"status": "Error stopping the app", "error": str(e)}), 500

    return jsonify({"status": "Invalid action"}), 400

@socketio.on('connect')
def handle_connect():
    print("Cliente conectado via Socket.IO")

@socketio.on('disconnect')
def handle_disconnect():
    print("Cliente desconectado via Socket.IO")

@socketio.on('video')
def handle_video(data):
    if tracking_active:
        hand_tracker.receive_frame(data)

@app.route('/status', methods=['GET'])
def status_check():
    return jsonify({"status": "Active server", "gesture": gesture or "No gestures detected"}), 200


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)