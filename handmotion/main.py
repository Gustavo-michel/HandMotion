from flask import Flask, jsonify, Response
import cv2
import mediapipe as mp
import pyautogui

app = Flask(__name__)

@app.route('/start-tracking', methods=['GET'])
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
        h, w, _ = img.shape 

        if handsPoints:
            for points in handsPoints:
                mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)
                for id, cord in enumerate(points.landmark):
                    cx, cy = int(cord.x * w), int(cord.y * h)

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

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        return jsonify({"status": "tracking started"})


def generate_frames():
    video = cv2.VideoCapture(0)
    
    while True:
        success, frame = video.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)