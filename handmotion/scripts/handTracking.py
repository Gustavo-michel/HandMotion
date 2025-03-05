"""
This script is responsible for providing the script for the Flask app that connects with the Google Chrome extension
"""
import cv2
import mediapipe as mp
from collections import deque
import tensorflow as tf
import numpy as np
import os
import pyautogui
import time
import sys

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class HandTracking:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        if not self.video.isOpened():
            raise RuntimeError("Error accessing the camera. Check the camera connection or index.")
        
        hand = mp.solutions.hands
        self.Hand = hand.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mpDraw = mp.solutions.drawing_utils
        self.frame = None 

        self.screen_width, self.screen_height = pyautogui.size()
        self.safe_margin = 5
        self.mouse_positions = deque(maxlen=5)
        self.last_click_time = time.time()
        # self.video.set(cv2.CAP_PROP_FPS, 30)
        # self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
        # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.model = None
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(script_dir, '../model/gesture_model.h5')

    def load_model(self):
        """
        Loading the predict model.
        """
        if self.model is None:
            try:
                self.model = tf.keras.models.load_model(self.model_path)
                print("Modelo carregado com sucesso!")
            except Exception as e:
                print(f"Erro ao carregar o modelo: {e}")
                sys.exit(1)

    def generate_frames(self):
        """
        Generates frames for display in a Flask route.
        """
        while True:
            try:
                check, frame = self.video.read()
                if not check:
                    print("Error capturing the frame.")
                    break

                imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.Hand.process(imgRGB)

                if results.multi_hand_landmarks:
                    for points in results.multi_hand_landmarks:
                        self.mpDraw.draw_landmarks(
                            frame, points, mp.solutions.hands.HAND_CONNECTIONS,
                            self.mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                            self.mpDraw.DrawingSpec(color=(0, 0, 255), thickness=2))
                frame = cv2.flip(frame, 1)
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                print(f"Error capturing the frame: {e}")
                break
    
    def actions(self, predicted_class):
        """Defines actions corresponding to detected gestures.

        Args:
            predicted_class (int): Last predicted class.

        Returns:
            Bool: return False if not action.
        """
        actions = {
            0: lambda: pyautogui.click(button='left'),  # Left click
            1: lambda: pyautogui.click(button='right'),  # Right click
            2: lambda: pyautogui.hotkey('ctrl', 'shift', 'tab'),  # Previous tab
            3: lambda: pyautogui.hotkey('ctrl', 'tab'),  # Next tab
            4: lambda: pyautogui.press('pgup'),  # Scroll up
            5: lambda: pyautogui.press('pgdn')   # Scroll down
        }

        if predicted_class in actions and (time.time() - self.last_click_time > 0.7):
            actions[predicted_class]()
            self.last_click_time = time.time()
        
        return False

    def tracking(self):
        """
        Method to process the video and return the detected gesture.
        """

        self.load_model()
        gesture_names = ["Left Click", "Right Click", "Previous Tab", "Next Tab","Roll page up", "Roll page down", "Move Mouse"]
        
        check, img = self.video.read()
        if not check:
            raise RuntimeError("Error accessing the camera. Check the camera connection or index.")
        
        try:
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

                    gesture_name_str = gesture_names[predicted_class] if predicted_class < len(gesture_names) else "Unknown"

                    return gesture_name_str

            return None
        except Exception as e:
            print(f"Error in tracking: {e}")
            return None
        