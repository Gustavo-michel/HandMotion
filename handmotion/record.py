import os
import cv2
import mediapipe as mp
import csv
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

video = cv2.VideoCapture(0)
hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

gesture_data = []

def save_gest(gestures):
    try:
        gesture_label = int(input("Insira o rótulo para este gesto (ex.: '1' para gesto 1, '2' para gesto 2): "))
        gesture_data.append((gestures, gesture_label))
        same_label_count = sum(1 for _, label in gesture_data if label == gesture_label)
        print(f"Gesto {gesture_label} salvo com sucesso! Total de gestos com esta label: {same_label_count}")
    except ValueError:
        print("Por favor, insira um número inteiro válido.")



print("Pressione 's' para salvar o gesto atual ou 'q' para sair.")

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
                save_gest(gestures)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

with open("gestures.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    for data, label in gesture_data:
        writer.writerow(data + [label])

print("Dados dos gestos salvos com sucesso em 'gestures.csv'.")

with open('gestures.csv', 'r') as file:
    num_gestos = sum(1 for i in file)
print("Número de gestos salvos:", num_gestos)
