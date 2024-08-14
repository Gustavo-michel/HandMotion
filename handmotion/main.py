import cv2
import mediapipe as mp
import pyautogui

video = cv2.VideoCapture(0)

hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()
safe_margin = 10

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
                screen_y = screen_height - int(cord.y * (screen_height - 2 * safe_margin)) + safe_margin

                if id == 9:
                    pyautogui.moveTo(screen_x, screen_y, duration=0.001)

                click_condition = all(points.landmark[d].y > points.landmark[b].y for d, b in points_to_check.items())
                if click_condition and not click_triggered:
                    pyautogui.click()
                    click_triggered = True

                if not click_condition:
                    click_triggered = False

    cv2.imshow("Imagem", img)
    cv2.waitKey(1)
