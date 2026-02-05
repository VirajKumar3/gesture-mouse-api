import cv2
import mediapipe as mp
import pyautogui
import math
import time

pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

prev_y = None
dragging = False
last_click = 0

def fingers_up(lm):
    fingers = []

    # Thumb
    fingers.append(lm[4].x > lm[3].x)

    # Other fingers
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    for tip, pip in zip(tips, pips):
        fingers.append(lm[tip].y < lm[pip].y)

    return fingers  # [thumb, index, middle, ring, pinky]

def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        lm = hand.landmark
        fingers = fingers_up(lm)

        index = lm[8]
        x = int(index.x * screen_w)
        y = int(index.y * screen_h)

        # ☝️ MOVE
        if fingers == [0,1,0,0,0]:
            pyautogui.moveTo(x, y, duration=0.01)

        # 🤏 LEFT CLICK
        if distance(lm[4], lm[8]) < 0.03 and time.time() - last_click > 0.5:
            pyautogui.click()
            last_click = time.time()

        # ✌️ RIGHT CLICK
        if fingers == [0,1,1,0,0] and time.time() - last_click > 0.6:
            pyautogui.rightClick()
            last_click = time.time()

        # ✊ DRAG
        if fingers == [0,0,0,0,0]:
            if not dragging:
                pyautogui.mouseDown()
                dragging = True
            pyautogui.moveTo(x, y, duration=0.01)
        else:
            if dragging:
                pyautogui.mouseUp()
                dragging = False

        # 🖐️ SCROLL
        if fingers == [1,1,1,1,1]:
            if prev_y is not None:
                if y < prev_y - 15:
                    pyautogui.scroll(40)
                elif y > prev_y + 15:
                    pyautogui.scroll(-40)
            prev_y = y
        else:
            prev_y = None

        mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

        cv2.putText(
            img,
            f"Gesture: {fingers}",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow("Gesture Virtual Mouse", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
