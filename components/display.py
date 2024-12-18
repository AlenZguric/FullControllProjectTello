import pygame
import cv2
import numpy as np

class Display:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 36)

    def update(self, telemetry, frame):
        # Prikaz telemetrije
        self._draw_telemetry(telemetry)

        # Prikaz video streama
        self._draw_video(frame)

    def _draw_telemetry(self, telemetry):
        y_offset = 20
        for key, value in telemetry.items():
            text = f"{key}: {value}"
            label = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(label, (20, y_offset))
            y_offset += 40

    def _draw_video(self, frame):
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (self.width // 2, 0))
