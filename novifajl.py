import pygame
import time
import cv2
import numpy as np
from djitellopy import Tello

# Inicijalizacija pygame-a
pygame.init()

# Pygame postavke
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tello EDU Display")

# Poveži se sa Tello dronom
tello = Tello()
try:
    tello.connect()
    tello.streamon()
    tello.takeoff()

    # Postavi početnu visinu kao referentnu tačku
    base_height = tello.get_height()

    # Font za prikaz telemetrije
    font = pygame.font.Font(None, 36)

    # Vremenska kontrola
    last_telemetry_time = 0  # Početno vreme za telemetriju
    telemetry = {}  # Prazan dict za telemetriju

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dobij trenutno vreme
        current_time = time.time() * 1000  # Trenutno vreme u milisekundama

        # Proveri da li je prošlo 1000 ms za telemetriju
        if current_time - last_telemetry_time >= 1000:
            try:
                current_height = tello.get_height()
                adjusted_height = current_height - base_height
                telemetry = {
                    "Battery": f"{tello.get_battery()}%",
                    "Height": f"{adjusted_height} cm",
                    "Speed X": f"{tello.get_speed_x()} cm/s",
                    "Speed Y": f"{tello.get_speed_y()} cm/s",
                    "Speed Z": f"{tello.get_speed_z()} cm/s",
                    "WiFi Signal": f"{tello.query_wifi_signal_noise_ratio()}%",
                }
            except Exception as e:
                print(f"Greška pri dohvaćanju telemetrije: {e}")
            last_telemetry_time = current_time

        # Dobij video frame
        frame_read = tello.get_frame_read()
        frame = frame_read.frame if frame_read else None
        
        if frame is not None:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  # Rotiraj sliku horizontalno
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Konvertuj u RGB format
            frame_surface = pygame.surfarray.make_surface(np.flipud(frame))  # Flip za ispravno prikazivanje
            screen.blit(frame_surface, (0, 0))

        # Prikaz telemetrije
        screen.fill((0, 0, 0), (0, 0, SCREEN_WIDTH, 100))  # Očisti prostor za tekst
        y_offset = 20
        for key, value in telemetry.items():
            text = f"{key}: {value}"
            label = font.render(text, True, (255, 255, 255))
            screen.blit(label, (20, y_offset))
            y_offset += 40

        pygame.display.flip()

finally:
    # Osiguraj zatvaranje resursa
    try:
        tello.streamoff()
        tello.land()
    except Exception as e:
        print(f"Greška pri zatvaranju resursa: {e}")
    tello.end()
    pygame.quit()
