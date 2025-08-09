import cv2
import mediapipe as mp
import pyautogui
import util
from pynput.mouse import Button, Controller
import time

mouse = Controller()
screen_width, screen_height = pyautogui.size()
left_clicking = False

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None

def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height)
        pyautogui.moveTo(x, y)

def is_left_click(landmark_list, thumb_index_dist):
    return (util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
            thumb_index_dist > 50)

def is_right_click(landmark_list, thumb_index_dist):
    return (util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90 and
            thumb_index_dist > 50)

def is_double_click(landmark_list, thumb_index_dist):
    return (util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
            thumb_index_dist > 50)

def is_index_bent(landmark_list):
    return util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50

def is_middle_bent(landmark_list):
    return util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50

def is_ring_bent(landmark_list):
    return util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) < 60

def is_palm_open(landmark_list):
    index_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])
    middle_angle = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12])
    ring_angle = util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16])
    pinky_angle = util.get_angle(landmark_list[17], landmark_list[18], landmark_list[20])
    thumb_angle = util.get_angle(landmark_list[1], landmark_list[2], landmark_list[4])
    return (index_angle > 160 and
            middle_angle > 160 and
            ring_angle > 160 and
            pinky_angle > 160 and
            thumb_angle > 150)

def is_hand_spread(landmark_list):
    if len(landmark_list) < 21:
        return False
    index_tip = landmark_list[8]
    pinky_tip = landmark_list[20]
    spread = util.get_distance([index_tip, pinky_tip])
    return spread > 100

def is_palm_open_and_spread(landmark_list):
    return is_palm_open(landmark_list) and is_hand_spread(landmark_list)

def detect_gestures(frame, landmark_list, processed):
    global left_clicking

    if len(landmark_list) < 21:
        return

    index_finger_tip = find_finger_tip(processed)
    thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])
    pinch_distance = util.get_distance([landmark_list[4], landmark_list[8]])
    check_angle = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])

    index_bent = is_index_bent(landmark_list)
    middle_bent = is_middle_bent(landmark_list)
    ring_bent = is_ring_bent(landmark_list)
    pinky_angle = util.get_angle(landmark_list[17], landmark_list[18], landmark_list[20])

    # Priority 1: Palm open and spread = hold left click + move
    if is_palm_open_and_spread(landmark_list):
        if not left_clicking:
            mouse.press(Button.left)
            left_clicking = True
            print("[GESTURE] Palm spread - Holding left click")
        move_mouse(index_finger_tip)
        print("[MOVE] Mouse moving while holding left click")
        return

    # Release left click if previously held
    if left_clicking:
        mouse.release(Button.left)
        left_clicking = False
        print("[GESTURE] Palm closed - Released left click")

    # Priority 2: Mouse movement (no palm spread)
    if thumb_index_dist < 50 and check_angle > 90:
        move_mouse(index_finger_tip)
        print("[MOVE] Mouse moving")
        return

    # Priority 3: Zoom in
    if pinch_distance < 30:
        mouse.scroll(0, 2)
        print("[GESTURE] Zoom In (Pinch detected)")
        return

    # Priority 4: Zoom out
    if (pinky_angle > 150 and index_bent and middle_bent and ring_bent):
        mouse.scroll(0, -2)
        print("[GESTURE] Zoom Out (Only pinky raised)")
        return

    # Other clicks (low priority)
    if index_bent and not middle_bent:
        mouse.press(Button.left)
        mouse.release(Button.left)
        print("[CLICK] Quick left click")

    elif index_bent and middle_bent:
        if not left_clicking:
            mouse.press(Button.left)
            left_clicking = True
            print("[CLICK] Hold left click down")
    else:
        if left_clicking:
            mouse.release(Button.left)
            left_clicking = False
            print("[CLICK] Hold left click released")

    if is_right_click(landmark_list, thumb_index_dist):
        mouse.press(Button.right)
        mouse.release(Button.right)
        print("[CLICK] Right click")

    elif is_double_click(landmark_list, thumb_index_dist):
        mouse.scroll(0, 2)
        print("[CLICK] Middle click (scrolling up)")

def run_virtual_mouse():
    cap = cv2.VideoCapture(0)
    draw = mp.solutions.drawing_utils

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmarks_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmarks_list.append((lm.x, lm.y))

            detect_gestures(frame, landmarks_list, processed)

            # cv2.imshow('frame', frame)  # Uncomment to debug with camera feed
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
    finally:
        cap.release()
        # cv2.destroyAllWindows()

if __name__ == "__main__":
    run_virtual_mouse()
