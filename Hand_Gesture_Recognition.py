import cv2
import mediapipe as mp
import pyautogui
import time


mp_hands = mp.solutions.hands     
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6, 
    min_tracking_confidence=0.4 
)
mp_drawing = mp.solutions.drawing_utils


def all_fingers_open(landmarks):
    return all([landmarks[i].y < landmarks[i - 2].y for i in [8, 12, 16, 20]])


def index_finger_only(landmarks):
    return landmarks[8].y < landmarks[6].y and all([landmarks[i].y > landmarks[i - 2].y for i in [12, 16, 20]])


def check_camera(cap):
    if not cap.isOpened():
        print("awoakwowa error bangke.")
        return False
    else:
        print("cihuyyy berhasil bruakakakaka.")
        return True


jump_cooldown = 0.4 
duck_cooldown = 0.4
last_jump_time = 0
last_duck_time = 0


cap = cv2.VideoCapture(0)


if not check_camera(cap):
    exit()

frame_count = 0 

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("kebaca cuyh kameranya.")
        break

    
    frame_count += 1
    if frame_count % 2 == 0:
        continue


    image = cv2.flip(image, 1)

    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)

    current_time = time.time()

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark
            
            
            if all_fingers_open(landmarks): 
                if current_time - last_jump_time > jump_cooldown:
                    pyautogui.press('space')  
                    print("Jump")
                    last_jump_time = current_time

            
            elif index_finger_only(landmarks):
                if current_time - last_duck_time > duck_cooldown:
                    pyautogui.keyDown('down')  
                    print("Duck")
                    last_duck_time = current_time
            else:
                pyautogui.keyUp('down')  

        
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Hand Tracking Dino Control', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()