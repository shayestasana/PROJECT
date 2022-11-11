import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def distanceCalculate(p1, p2):
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return dis
font = cv2.FONT_HERSHEY_SIMPLEX
red = (0, 0, 255)
green = (0, 255, 0)
blue= (255, 0, 0)
white=(255, 255, 255)
screen_height = 480*2
screen_width = 640*2
# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
       
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        h, w, _ = image.shape
        image = cv2.resize(image, (screen_width, screen_height))
        image = cv2.flip(image, 1)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                coords_1 = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                coords_2 = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                try:
                    # normalize the coordinates
                    x1, y1 = int(coords_1.x * w), int(coords_1.y * h)
                    x2, y2 = int(coords_2.x * w), int(coords_2.y * h)
                    cv2.circle(image, (x1, y1), 5, (255, 0, 0), -1)
                    cv2.circle(image, (x2, y2), 5, (0, 255, 0), -1)
                    # calculate the distance
                    dis = distanceCalculate((x1, y1), (x2, y2))
                    # draw the distance at the bottom of the image
                    cv2.putText(image, str(int(dis)), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    # logic 
                    if dis < 30:
                        # display joined
                        cv2.putText(image, "Selector", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    else:
                        # display not joined
                        cv2.putText(image, "Pointer", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                except Exception as e:
                    print(e)
        # display quiz ui
        q ="Is this a hand?"
        cv2.putText(image, q, (30, h - 50), font, 1, white, 2, cv2.LINE_AA)
        cv2.rectangle(image, (20, 90), (200,170), blue, 2)
        cv2.putText(image, "category", (50, 130), font, 1, blue, 2, cv2.LINE_AA)
        cv2.rectangle(image, (230, 20), (410,100), red, 2)
        #cv2.putText(frame, "A", (w - 70, 30), font, 1, red, 2, cv2.LINE_AA)
        cv2.rectangle(image, (440, 20), (620,100), red, 2)
     # cv2.putText(frame, "B", (w - 70, 30), font, 1, red, 2, cv2.LINE_AA)
        cv2.rectangle(image, (20, 200), (200,240), blue, 2)
     # cv2.putText(frame, "score", (w - 70, 30), font, 1, red, 2, cv2.LINE_AA)
        cv2.rectangle(image, (230,130), (410,210), red, 2)
     # cv2.putText(frame, "B", (w - 70, 30), font, 1, red, 2, cv2.LINE_AA)
        cv2.rectangle(image, (440, 130), (620,210), red, 2)
     # cv2.putText(frame, "B", (w - 70, 30), font, 1, red, 2, cv2.LINE_AA)
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
        
cap.release()