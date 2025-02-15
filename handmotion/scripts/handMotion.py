import cv2
import mediapipe as mp
import tensorflow as tf
import pyautogui
import numpy as np
from collections import deque
import threading
import time
import sys
import json
import base64
import os
import signal

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class HandTracking:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        if not self.video.isOpened():
            raise RuntimeError("Error accessing the camera. Check the camera connection or index.")

        hand = mp.solutions.hands
        self.Hand = hand.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mpDraw = mp.solutions.drawing_utils
	
        self.screen_width, self.screen_height = pyautogui.size()
        self.safe_margin = 5
        self.mouse_positions = deque(maxlen=5)
        self.last_click_time = time.time()

        self.model = None
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(base_path, "model", "gesture_model.h5")

        self.model_loading_thread = threading.Thread(target=self.load_model, daemon=True)
        self.model_loading_thread.start()

    def load_model(self):
        """
        Load model.
        """
        if self.model is None:
            try:
                self.model = tf.keras.models.load_model(self.model_path)
                print("Modelo carregado com sucesso!")
            except Exception as e:
                print(f"Erro ao carregar o modelo: {e}")
                sys.exit(1)

    def actions(self, predicted_class):
        """
        Defines actions corresponding to detected gestures.
        """
        actions = {
            0: lambda: pyautogui.click(button='left'),  # Left click
            1: lambda: pyautogui.click(button='right'),  # Right click
            2: lambda: pyautogui.hotkey('ctrl', 'shift', 'tab'),  # Previous tab
            3: lambda: pyautogui.hotkey('ctrl', 'tab'),  # Next tab
            4: lambda: pyautogui.press('pgup'),  # Scroll up
            5: lambda: pyautogui.press('pgdn')   # Scroll down
        }

        if predicted_class in actions and (time.time() - self.last_click_time > 0.5):
            actions[predicted_class]()
            self.last_click_time = time.time()
        
        return False
    
    def tracking(self):
        """Method to process the video and return the detected gesture.

        Returns:
            Str: Gestures Names
        """
        check, img = self.video.read()
        if not check:
            raise RuntimeError("Error accessing the camera. Check the camera connection or index.")
        
        imgRGB = cv2.resize(img, (320, 240))
        imgRGB = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2RGB)
        results = self.Hand.process(imgRGB)
        handsPoints = results.multi_hand_landmarks

        if handsPoints:
            for points in handsPoints:
                self.mpDraw.draw_landmarks(img, points, mp.solutions.hands.HAND_CONNECTIONS)

                gesture = []
                for _, cord in enumerate(points.landmark):
                    gesture.extend([cord.x, cord.y, cord.z])

                gesture_array = np.array([gesture])
                prediction = self.model.predict(gesture_array, verbose=0)
                predicted_class = np.argmax(prediction)

                if predicted_class == 6:  # Mouse movement
                        hand_center = points.landmark[9]
                        screen_x = self.screen_width - int(hand_center.x * (self.screen_width - 2 * self.safe_margin)) + self.safe_margin
                        screen_y = int(hand_center.y * (self.screen_height - 2 * self.safe_margin)) + self.safe_margin

                        self.mouse_positions.append((screen_x, screen_y))

                        avg_x = int(sum(pos[0] for pos in self.mouse_positions) / len(self.mouse_positions))
                        avg_y = int(sum(pos[1] for pos in self.mouse_positions) / len(self.mouse_positions))

                        pyautogui.moveTo(avg_x, avg_y, duration=0.0, _pause=False)
                else:
                    self.actions(predicted_class)

                gesture_names = ["Left Click", "Right Click", "Previous Tab", "Next Tab","Roll page up", "Roll page down", "Move Mouse"]
                gesture_name_str = gesture_names[predicted_class] if predicted_class < len(gesture_names) else "Unknown"

                return gesture_name_str

        return None
    
def read_message():
    try:
        length_bytes = sys.stdin.buffer.read(4)
        if not length_bytes:
            return None
        length = int.from_bytes(length_bytes, byteorder='little')
        return json.loads(sys.stdin.buffer.read(length).decode('utf-8'))
    except Exception as e:
        print(f"Erro lendo mensagem: {e}", file=sys.stderr)
        return None

def send_message(message):
    try:
        encoded = json.dumps(message).encode('utf-8')
        sys.stdout.buffer.write(len(encoded).to_bytes(4, byteorder='little'))
        sys.stdout.buffer.write(encoded)
        sys.stdout.buffer.flush()
    except Exception as e:
        print(f"Erro enviando mensagem: {e}", file=sys.stderr)

def camera(hand_tracking):
    while True:
        try:
            check, frame = hand_tracking.video.read()
            if not check:
                print("Error capturing the frame.")
                break

            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hand_tracking.Hand.process(imgRGB)

            if results.multi_hand_landmarks:
                for points in results.multi_hand_landmarks:
                    hand_tracking.mpDraw.draw_landmarks(
                        frame, points, mp.solutions.hands.HAND_CONNECTIONS,
                        hand_tracking.mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                        hand_tracking.mpDraw.DrawingSpec(color=(0, 0, 255), thickness=2))
            frame = cv2.flip(frame, 1)
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield base64.b64encode(frame_bytes).decode('utf-8')
        except Exception as e:
            print(f"Error capturing the frame: {e}")
            break

def track_gestures():
    while process:
        gesture_text = tracker.tracking()
        send_message({"gesture": gesture_text})
        time.sleep(0.03)


if __name__ == "__main__":
    tracker = HandTracking()
    process = False

    while tracker.model is None:
        time.sleep(0.1)

    while True:
        message = read_message()
        if message:
            action = message.get("action")

            if action == "start":
                process = True
                tracking_thread = threading.Thread(target=track_gestures, daemon=True)
                tracking_thread.start()

            elif action == "stop":
                process = False
                if tracking_thread:
                    tracking_thread.join()
                    tracking_thread = None
                cv2.destroyAllWindows()
                sys.exit(0)

