from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import threading
from handmotion.scripts.handTracking import HandTracking
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["chrome-extension://mahcmoailbbfjannahinbdkkibkajbcf", "*"]}})

hand_tracker = HandTracking()
gesture = None

tracking_active = False
tracking_thread = None

def trackGestures():
    """
    initialize tracking
    """
    global gesture
    
    while tracking_active:
        gesture = hand_tracker.tracking()
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
            tracking_thread = threading.Thread(target=trackGestures, daemon=True)
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

@app.route('/video_feed')
def video_feed():
    """Collects the video transmission passing to the client side
    Returns:
        jpeg: video frames
    """
    return Response(hand_tracker.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status', methods=['GET'])
def status_check():
    """Check server status

    Returns:
        json(dict): server status and current gesture
    """
    return jsonify({"status": "Active server", "gesture": gesture or "No gestures detected"}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)