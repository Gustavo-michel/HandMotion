from flask import Flask, Response, render_template
from flask_socketio import SocketIO
import cv2
import mediapipe as mp
import pyautogui

app = Flask(__name__)
socketio = SocketIO(app)

video = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('handmotion.html')

@socketio.on('start_tracking')
def start_tracking():
    hand = mp.solutions.hands
    Hand = hand.Hands(max_num_hands=1)
    mpDraw = mp.solutions.drawing_utils

    screen_width, screen_height = pyautogui.size()
    safe_margin = 2

    points_to_check = {
        8: 5,
        12: 9,
        16: 13,
        20: 17
    }
    click_triggered = False

    while True:
        check, img = video.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = Hand.process(imgRGB)
        handsPoints = results.multi_hand_landmarks

        if handsPoints:
            for points in handsPoints:
                mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)
                for id, cord in enumerate(points.landmark):
                    screen_x = screen_width - int(cord.x * (screen_width - 2 * safe_margin)) + safe_margin
                    screen_y = int(cord.y * (screen_height - 2 * safe_margin)) + safe_margin

                    if id == 9:
                        pyautogui.moveTo(screen_x, screen_y, duration=0.1)

                    click_condition = all(points.landmark[d].y > points.landmark[b].y for d, b in points_to_check.items())
                    if click_condition and not click_triggered:
                        pyautogui.click()
                        click_triggered = True
                    elif not click_condition:
                        click_triggered = False

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        socketio.emit('video_frame', frame)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
