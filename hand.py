import mediapipe as mp
import cv2
import numpy as np
import uuid
import os
from pynput.keyboard import Key, Controller

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
joint_list =[[8,5,0]]

def draw_finger_angles(image, results, joint_list):
    # Loop through hands
    for hand in results.multi_hand_landmarks:
        # Loop through joint sets
        for joint in joint_list:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])  # Index tip
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])  # Index root
            c = np.array([hand.landmark[joint[2]].x, hand.landmark[joint[2]].y])  # Root of palm

            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            angle = np.abs(radians * 180.0 / np.pi)


            cv2.putText(image, str(round(angle, 2)), tuple(np.multiply(b, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    return image, angle

def get_label(index, hand, results):
    output = None
    for idx, classification in enumerate(results.multi_handedness):
        if classification.classification[0].index == index:
            # Process results
            label = classification.classification[0].label
            score = classification.classification[0].score
            text = '{} {}'.format(label, round(score, 2))

            # Extract Coordinates
            coords = tuple(np.multiply(
                np.array((hand.landmark[mp_hands.HandLandmark.WRIST].x, hand.landmark[mp_hands.HandLandmark.WRIST].y)),
                [640, 480]).astype(int))

            output = text, coords

    return output


cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()

        # BGR 2 RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Flip on horizontal
        image = cv2.flip(image, 1)

        # Set flag
        image.flags.writeable = False

        # Detections
        results = hands.process(image)

        # Set flag to true
        image.flags.writeable = True

        # RGB 2 BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Rendering results
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                          )

            # Draw angles and enter keyboard events
            image, angle = draw_finger_angles(image, results, joint_list)
            keyboard = Controller()
            if angle<=168:
                keyboard.press(Key.right)
                keyboard.release(Key.right)
            if angle>=173 and angle<=180:
                keyboard.press(Key.up)
                keyboard.release(Key.up)
            if angle>= 184 :
                keyboard.press(Key.left)
                keyboard.release(Key.left)
            if angle<=25:
                keyboard.press(Key.down)
                keyboard.release(Key.down)
                
        cv2.imshow('Hand Tracking', image)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

for i in range (1,5):
    cv2.waitKey(1)
