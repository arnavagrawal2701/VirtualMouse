import cv2
import mediapipe as mp
import pyautogui
import math

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Mediapipe hand detector
hand_detector = mp.solutions.hands.Hands(
    max_num_hands=1,
    model_complexity=0,               # faster model
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
drawing_utils = mp.solutions.drawing_utils

# Screen size for mapping
screen_width, screen_height = pyautogui.size()

# Cursor smoothing variables
index_x, index_y = 0, 0
smooth_x, smooth_y = 0, 0
alpha = 0.2   # smoothing factor (0–1)

# Gesture state flags
left_click_down = False
right_click_down = False

# Distance threshold (tune if needed)
click_threshold = 20  # pixels in camera space

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("Failed to grab frame")
        continue

    # Mirror the frame so movement feels natural
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    # Convert to RGB for Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            thumb, index, middle = None, None, None

            # Collect fingertip positions
            for id, lm in enumerate(landmarks):
                x = int(lm.x * frame_width)
                y = int(lm.y * frame_height)

                if id == 4:   # thumb tip
                    thumb = (x, y)
                    cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)

                elif id == 8:  # index tip
                    index = (x, y)
                    cv2.circle(frame, (x, y), 8, (255, 0, 0), -1)

                elif id == 12:  # middle tip
                    middle = (x, y)
                    cv2.circle(frame, (x, y), 8, (0, 0, 255), -1)

            # =========================
            # 1) CURSOR MOVEMENT
            # =========================
            if index is not None:
                ix, iy = index

                # Map to screen space
                raw_x = screen_width / frame_width * ix
                raw_y = screen_height / frame_height * iy

                # Smooth the cursor movement
                smooth_x = alpha * raw_x + (1 - alpha) * smooth_x
                smooth_y = alpha * raw_y + (1 - alpha) * smooth_y

                index_x, index_y = smooth_x, smooth_y
                pyautogui.moveTo(index_x, index_y)

            # =========================
            # 2) LEFT CLICK: thumb + index pinch
            # =========================
            if thumb is not None and index is not None:
                dist_thumb_index = math.hypot(
                    thumb[0] - index[0], thumb[1] - index[1]
                )

                if dist_thumb_index < click_threshold and not left_click_down:
                    pyautogui.click()
                    left_click_down = True
                elif dist_thumb_index >= click_threshold:
                    left_click_down = False

            # =========================
            # 3) RIGHT CLICK: thumb + middle pinch
            # =========================
            if thumb is not None and middle is not None:
                dist_thumb_middle = math.hypot(
                    thumb[0] - middle[0], thumb[1] - middle[1]
                )

                if dist_thumb_middle < click_threshold and not right_click_down:
                    pyautogui.rightClick()
                    right_click_down = True
                elif dist_thumb_middle >= click_threshold:
                    right_click_down = False

    cv2.imshow("Virtual Mouse", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
