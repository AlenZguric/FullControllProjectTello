import pygame
import time
from djitellopy import Tello
from components.display import Display
from utils.telemetry import get_telemetry_data

# Inicijalizacija pygame-a
pygame.init()

# Pygame postavke
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Tello Display")

# Poveži se sa Tello dronom
tello = Tello()
try:
    tello.connect()
    time.sleep(4)
    # Pokreni video stream
    print("Pokušavam da pokrenem video stream...")
    if tello.streamon():
        print("Stream pokrenut, spreman za poletanje.")
        tello.takeoff()
    else:

        print("Stream nije uspeo da se pokrene. Proveri konekciju.")
        raise RuntimeError("Nije moguće pokrenuti video stream.")

    # Kreiraj instancu za prikaz
    display = Display(screen, 1200, 800)

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

        # Proveri da li je prošlo 1000 ms
        if current_time - last_telemetry_time >= 1000:
            telemetry = get_telemetry_data(tello)  # Ažuriraj telemetriju
            last_telemetry_time = current_time  # Postavi poslednje vreme

        # Dobij video frame
        frame = tello.get_frame_read().frame

        # Ažuriraj prikaz
        display.update(telemetry, frame)
        pygame.display.flip()

finally:
    # Osiguraj zatvaranje resursa
    tello.streamoff()
    tello.end()
    pygame.quit()
