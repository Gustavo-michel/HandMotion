import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf

video = cv2.VideoCapture(0)
hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()
safe_margin = 5
click_triggered = False
previous_class = None

model_path = 'gesture_model.h5'
try:
    model = tf.keras.models.load_model(model_path)
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    exit()

def actions(predicted_class, click_triggered, previous_class):
    actions = {
        0: lambda: pyautogui.click(button='left'),  # Clique esquerdo
        1: lambda: pyautogui.click(button='right'),  # Clique direito
        2: lambda: pyautogui.hotkey('ctrl', 'shift', 'tab'),  # Aba anterior
        3: lambda: pyautogui.hotkey('ctrl', 'tab'),  # Próxima aba
    }

    if predicted_class in actions and not click_triggered and predicted_class != previous_class:
        actions[predicted_class]()
        return True, predicted_class
    
    return False, previous_class


while True:
    check, img = video.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Hand.process(imgRGB)
    handsPoints = results.multi_hand_landmarks
    h, w, _ = img.shape
    prev_screen_x, prev_screen_y = None, None 

    if handsPoints:
        for points in handsPoints:
            mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)

            gesture = []
            for id, cord in enumerate(points.landmark):
                gesture.extend([cord.x, cord.y, cord.z])

            gesture_array = np.array([gesture])
            prediction = model.predict(gesture_array)
            predicted_class = np.argmax(prediction)

            if predicted_class == 4:  # Mão aberta -> Movimento do mouse
                screen_x = screen_width - int(cord.x * (screen_width - 2 * safe_margin)) + safe_margin
                screen_y = int(cord.y * (screen_height - 2 * safe_margin)) + safe_margin

                pyautogui.moveTo(screen_x, screen_y, duration=0.0, _pause=False)
                previous_class = None
            else:
                click_triggered, previous_class = actions(predicted_class, click_triggered, previous_class)


            gesture_names = ["Left Click", "Right Click", "Previous Tab", "Next Tab", "Move Mouse"]
            gesture_name = gesture_names[predicted_class] if predicted_class < len(gesture_names) else "Unknown"
            cv2.putText(img, f"Gesture: {gesture_name}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Tracking", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
