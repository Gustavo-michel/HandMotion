from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import threading
from handmotion.scripts.handTracking import HandTracking

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5000/*"]}})

hand_tracker = HandTracking()
process = False
gesture = None

def track_gestures():
    global gesture
    
    while process:
        gesture = hand_tracker.run()

@app.route('/control', methods=['POST'])
def control():
    global process
    tracking_thread = None
    data = request.json
    action = data.get('action')

    if action == "start":
        if process:
            return jsonify({"status": "App is already running"}), 200
        try:
            process = True
            tracking_thread = threading.Thread(target=track_gestures, daemon=True)
            tracking_thread.start()
            return jsonify({"status": "Started"}), 200
        except Exception as e:
            return jsonify({"status": "Error when starting the app", "error": str(e)}), 500
            

    elif action == "stop":
        if process is False:
            return jsonify({"status": "App is already stopped"}), 200
        try:
            process = False
            tracking_thread = None
            return jsonify({"status": "Stopped"}), 200
        except Exception as e:
            return jsonify({"status": "Error stopping the app", "error": str(e)}), 500
            
    return jsonify({"status": "Invalid action"}), 400

@app.route('/video_feed')
def video_feed():
    return Response(hand_tracker.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/status', methods=['GET'])
def status_check():
    return jsonify({"status": "Active server", "gesture": gesture or "No gestures detected"}), 200


if __name__ == '__main__':
    app.run(port=5000)
