import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import pygame
import random
import time

# Inisialisasi MediaPipe hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Fungsi untuk mendeteksi apakah jari tertentu terangkat
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

# Inisialisasi game dengan Pygame
pygame.init()  # Pastikan pygame diinisialisasi
pygame.font.init()  # Inisialisasi modul font

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tangkap Bola dengan Gestur Tangan")
clock = pygame.time.Clock()

# Warna dan font
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
font = pygame.font.Font(None, 36)  # Pastikan font dibuat setelah pygame.font.init()

# Variabel permainan
player_width, player_height = 100, 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
ball_radius = 15
ball_x = random.randint(ball_radius, WIDTH - ball_radius)
ball_y = 0
ball_speed = 5
score = 0
running = True

# Faktor skala untuk meningkatkan sensitivitas pergerakan kursor
FAKTOR_SKALA_KURSOR = 1.5

# Inisialisasi Kamera
cap = cv2.VideoCapture(0)

# Gunakan MediaPipe untuk mendeteksi tangan
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5) as hands:
    while cap.isOpened() and running:
        # === Bagian Game ===
        screen.fill(WHITE)

        # Pergerakan bola
        ball_y += ball_speed
        if ball_y > HEIGHT:
            ball_y = 0
            ball_x = random.randint(ball_radius, WIDTH - ball_radius)

        # Deteksi jika bola ditangkap
        if player_x < ball_x < player_x + player_width and ball_y + ball_radius >= player_y:
            score += 1
            ball_y = 0
            ball_x = random.randint(ball_radius, WIDTH - ball_radius)

        # Gambar bola dan pemain
        pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

        # Tampilkan skor
        score_text = font.render(f"Skor: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Perbarui layar
        pygame.display.flip()

        # === Bagian Kamera dan Gestur ===
        success, image = cap.read()
        if not success:
            print("Tidak bisa mengakses kamera")
            break

        # Konversi warna dari BGR ke RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Deteksi gestur tangan
        results = hands.process(image)

        # Konversi kembali ke BGR untuk OpenCV
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Ambil landmark dari jari
                landmarks = hand_landmarks.landmark

                # Deteksi apakah hanya telunjuk yang terangkat untuk menggerakkan pemain
                if jari_terangkat(landmarks, 'telunjuk') and not jari_terangkat(landmarks, 'jari tengah') and not jari_terangkat(landmarks, 'jari manis') and not jari_terangkat(landmarks, 'kelingking'):
                    x_pos = int(landmarks[9].x * WIDTH * FAKTOR_SKALA_KURSOR)
                    player_x = max(0, min(WIDTH - player_width, x_pos))

        # Tampilkan kamera
        cv2.imshow('Gestur Tangan', image)

        # Keluar jika tekan tombol 'q'
        for event in pygame.event.get():
            if event.type == pygame.QUIT or cv2.waitKey(5) & 0xFF == ord('q'):
                running = False

        # Batasi FPS game
        clock.tick(30)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
