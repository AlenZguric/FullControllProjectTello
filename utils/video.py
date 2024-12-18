import cv2

class TelloVideo:
    def __init__(self, tello):
        self.tello = tello

    def get_frame(self):
        frame_read = self.tello.get_frame_read()
        if frame_read and frame_read.frame is not None:
            # Konvertuj frame iz BGR (default Tello format) u RGB za dalju obradu
            return cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)
        return None
