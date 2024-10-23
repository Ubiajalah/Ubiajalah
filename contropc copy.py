import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def jari_terangkat(landmarks, jari):
    if jari == 'jempol':
        return landmarks[4].x < landmarks[3].x
    if jari == 'telunjuk':
        return landmarks[8].y < landmarks[6].y
    if jari == 'jari tengah':
        return landmarks[12].y < landmarks[10].y
    if jari == 'jari manis':
        return landmarks[16].y < landmarks[14].y
    if jari == 'kelingking':
        return landmarks[20].y < landmarks[18].y


FAKTOR_SKALA_KURSOR = 1.5


cap = cv2.VideoCapture(0)


with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Tidak bisa mengakses kamera")
            break

      
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

       
        results = hands.process(image)

        
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                landmarks = hand_landmarks.landmark

                
                if jari_terangkat(landmarks, 'telunjuk') and not jari_terangkat(landmarks, 'jari tengah') and not jari_terangkat(landmarks, 'jari manis') and not jari_terangkat(landmarks, 'kelingking'):
                    x_pos = int(landmarks[9].x * pyautogui.size().width * FAKTOR_SKALA_KURSOR)
                    y_pos = int(landmarks[9].y * pyautogui.size().height * FAKTOR_SKALA_KURSOR)
                    pyautogui.moveTo(x_pos, y_pos)
                    print("Menggerakkan kursor ke", x_pos, y_pos)

                
                elif jari_terangkat(landmarks, 'telunjuk') and jari_terangkat(landmarks, 'jari tengah') and not jari_terangkat(landmarks, 'jari manis') and not jari_terangkat(landmarks, 'kelingking'):
                    print("Klik kiri")
                    pyautogui.click()

               
                elif jari_terangkat(landmarks, 'jempol') and jari_terangkat(landmarks, 'telunjuk') and jari_terangkat(landmarks, 'jari tengah') and jari_terangkat(landmarks, 'jari manis') and jari_terangkat(landmarks, 'kelingking'):
                    print("Scroll ke bawah")
                    pyautogui.scroll(-20) 

               
                elif jari_terangkat(landmarks, 'jempol') and not jari_terangkat(landmarks, 'telunjuk') and not jari_terangkat(landmarks, 'jari tengah') and not jari_terangkat(landmarks, 'jari manis') and not jari_terangkat(landmarks, 'kelingking'):
                    print("Scroll ke atas")
                    pyautogui.scroll(20) 

        
        cv2.imshow('Gestur Tangan', image)

        
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
