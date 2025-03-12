from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import threading
from handmotion.scripts.handTracking import HandTracking
import time
import queue
import cv2
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["chrome-extension://mahcmoailbbfjannahinbdkkibkajbcf", "http://localhost:5000", "*"]}})

frame_queue = queue.Queue(maxsize=10)
hand_tracker = HandTracking(frame_queue)
gesture = None

tracking_active = False
tracking_thread = None

def trackGestures():
    """
    initialize tracking
    """
    global tracking_active
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



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)