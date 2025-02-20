import mss
import numpy as np
import cv2

class WindowsCapture:
    def __init__(self, window_name="Albion Online Client"):
        self.sct = mss.mss()
        # Para simplificar, se usa el monitor primario.
        self.window = self.sct.monitors[1]

    def screenshot(self):
        screenshot = self.sct.grab(self.window)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img