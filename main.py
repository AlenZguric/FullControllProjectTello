import pygame
from components.display import Display
from utils.telemetry import get_telemetry_data
from utils.video import TelloVideo
from djitellopy import tello

def main():
    # Inicijalizacija pygame-a
    pygame.init()
    pygame.display.set_caption("Tello Drone Interface")

    # Kreiranje prozora
    screen_width, screen_height = 1200, 800
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Povezivanje sa Tello dronom
    myDrone = tello.Tello()
    myDrone.connect()
    myDrone.streamon()

    # Kreiranje instanci za GUI i video stream
    display = Display(screen, screen_width, screen_height)
    video = TelloVideo(myDrone)

    # Glavna petlja aplikacije
    running = True
    while running:
        # Obrada događaja
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dobijanje telemetrijskih podataka
        telemetry = get_telemetry_data(myDrone)

        # Dobijanje trenutnog frejma sa kamere
        frame = video.get_frame()

        # Prikaz podataka i videa
        display.update(telemetry, frame)

        # Osvježavanje ekrana
        pygame.display.flip()

    # Zatvaranje aplikacije
    myDrone.streamoff()
    myDrone.end()
    pygame.quit()

if __name__ == "__main__":
    main()
