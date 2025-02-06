import os
import cv2
import mediapipe as mp
import csv

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

video = cv2.VideoCapture(0)
hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

gesture_data = []
current_label = None

def set_label():
    global current_label
    try:
        current_label = int(input("Insert the new label for the gestures (e.g.: '1', '2', etc.): "))
        print(f"Label changed to {current_label}. Now all gestures will be saved with this label.")
    except ValueError:
        print("Please enter a valid integer.")
set_label()

print("Press 's' to save the current gesture with the chosen label, 'l' to change the label, or 'q' to exit and save everything.")

while True:
    check, img = video.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Hand.process(imgRGB)
    handsPoints = results.multi_hand_landmarks
    h, w, _ = img.shape

    if handsPoints:
        for points in handsPoints:
            mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)

            gestures = []
            for id, cord in enumerate(points.landmark):
                cx, cy = int(cord.x * w), int(cord.y * h)
                cv2.putText(img, str(id), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                gestures.extend([cord.x, cord.y, cord.z])

            cv2.imshow("Hand tracking", img)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                if current_label is not None:
                    gesture_data.append((gestures, current_label))
                    same_label_count = sum(1 for _, label in gesture_data if label == current_label)
                    print(f"Gesture saved with label {current_label}. Total gestures with this label: {same_label_count}")
                else:
                    print("Define a label first using the 'l' key.")
    else:
        cv2.imshow("Hand tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('l'):
        set_label()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()


csv_path = "data/gestures.csv"
os.makedirs(os.path.dirname(csv_path), exist_ok=True)

with open(csv_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    for data, label in gesture_data:
        writer.writerow(data + [label])

print(f"Gesture data successfully saved to '{csv_path}'.")

with open(csv_path, 'r') as file:
    num_gestos = sum(1 for _ in file)
print("Total number of saved gestures:", num_gestos)
