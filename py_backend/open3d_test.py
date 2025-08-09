import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

prev_x, prev_y = None, None
THRESHOLD = 40
COOLDOWN_TIME = 0.5  # seconds
last_action_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks and results.multi_handedness:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            hand_type = results.multi_handedness[i].classification[0].label  # 'Right' or 'Left'

            if hand_type != "Right":  # Track only the right hand
                continue

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger_tip = hand_landmarks.landmark[8]
            h, w, _ = frame.shape
            x, y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            if prev_x is not None and prev_y is not None:
                dx = x - prev_x
                dy = y - prev_y

                if time.time() - last_action_time > COOLDOWN_TIME:
                    dir_x = ""
                    dir_y = ""

                    if abs(dx) > THRESHOLD:
                        dir_x = "Right" if dx > 0 else "Left"

                    if abs(dy) > THRESHOLD:
                        dir_y = "Down" if dy > 0 else "Up"

                    if dir_x and dir_y:
                        print(f"Move {dir_y}-{dir_x}")
                    elif dir_x:
                        print(f"Move {dir_x}")
                    elif dir_y:
                        print(f"Move {dir_y}")

                    if dir_x or dir_y:
                        last_action_time = time.time()

            prev_x, prev_y = x, y
            break  # Only process the first matching right hand

    cv2.imshow('Hand Movement Control', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
