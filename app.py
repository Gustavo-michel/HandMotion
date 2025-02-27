from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
from handmotion.scripts.handTracking import HandTracking
from flask_socketio import SocketIO
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins=["chrome-extension://mahcmoailbbfjannahinbdkkibkajbcf"])

hand_tracker = HandTracking()
gesture = None

def track_gestures():
    global gesture
    
    while True:
        gesture = hand_tracker.run()
        time.sleep(0.1) 

@app.route('/control', methods=['POST'])
def control():
    tracking_thread = None
    data = request.json
    action = data.get('action')

    if action == "start":
        if tracking_thread and tracking_thread.is_alive():
            return jsonify({"status": "Tracking already started."}), 200
        try:
            tracking_thread = threading.Thread(target=track_gestures, daemon=True)
            tracking_thread.start()
            return jsonify({"status": "Sucess started"}), 200
        except Exception as e:
            return jsonify({"status": "Error when starting the app", "error": str(e)}), 500

    elif action == "stop":
        if not tracking_thread or not tracking_thread.is_alive():
            return jsonify({"status": "Tracking already stopped."}), 200
        try:
            tracking_thread.join()
            tracking_thread = None
            return jsonify({"status": "Sucess stopped"}), 200
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
    hand_tracker.receive_frame(data)

@app.route('/status', methods=['GET'])
def status_check():
    return jsonify({"status": "Active server", "gesture": gesture or "No gestures detected"}), 200


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)