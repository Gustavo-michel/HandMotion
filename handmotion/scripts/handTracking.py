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
import threading
from queue import Empty

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class HandTracking:
    def __init__(self, frame_queue):
        self.frame_queue = frame_queue
        self.gesture = None
        self.tracking_active = False
        self.tracking_thread = None
        
        hand = mp.solutions.hands
        self.Hand = hand.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mpDraw = mp.solutions.drawing_utils

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
        
        try:    
            img = self.frame_queue.get(timeout=2)

            imgRGB = cv2.resize(img, (160, 120))
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

        except Empty:
            print(f"empty frame queue")
            return "Aguardando Video..."
        except Exception as e:
            print(f"Error in tracking: {e}")
            return None
        
    def track_gestures(self):
        """Starts a tracking thread"""
        while self.tracking_active:
            self.gesture = self.tracking()
            time.sleep(0.1)

    def start_tracking(self):
        """Start tracking from control endpoint"""
        if self.tracking_active:
            return "Tracking already started."
        try:
            self.tracking_active = True
            self.tracking_thread = threading.Thread(target=self.track_gestures, daemon=True)
            self.tracking_thread.start()
            return "Success started"
        except Exception as e:
            return f"Error when starting the app: {str(e)}"

    def stop_tracking(self):
        """Stop tracking in control endpoint"""
        if not self.tracking_active:
            return "Tracking already stopped."
        try:
            self.tracking_active = False
            self.tracking_thread = None
            return "Success stopped"
        except Exception as e:
            return f"Error stopping the app: {str(e)}"