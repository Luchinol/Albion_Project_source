import cv2 as cv
import pyautogui
from time import sleep

from Application.Albion.detection import AlbionDetection

class Gathering:
    def __init__(self, x, y, resource):
        self.x = x
        self.y = y
        self.resource = resource

class Interaction:
    def __init__(self, model: AlbionDetection):
        self.model = model
        self.current_gathering: Gathering | None = None
        self.debug = self.model.debug
        # Si no deseas utilizar un archivo local, elimina o comenta la siguiente línea:
        # self.img_border_resource = cv.imread("images/cropped_bar_resource.png", cv.IMREAD_UNCHANGED)
        self.img_border_resource = None  # Opcional: asigna None para evitar errores

    # Si usabas esta imagen para detectar cierta área por template matching,
    # deberás eliminar o modificar los métodos que dependan de ella, por ejemplo:
    def __crop_image_resource(self):
        # Aquí podrías devolver una parte de la imagen capturada o ajustar la lógica
        top_x, top_y = 265, 365
        bottom_x, bottom_y = 293, 410
        img = self.model._process_image(self.model.window_capture.screenshot())
        return cv.cvtColor(img, cv.COLOR_BGR2GRAY)[top_y:bottom_y, top_x:bottom_x]

    def __is_mining(self):
        # Si dejas template matching, verifica que self.img_border_resource no es None
        cropped_img = self.__crop_image_resource()
        if self.img_border_resource is None:
            # Regresa False o implementa otra lógica en ausencia de la imagen de recurso
            return False
        result = cv.matchTemplate(cropped_img, self.img_border_resource, cv.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv.minMaxLoc(result)
        if self.debug:
            print("Template match value:", max_val)
        return max_val >= 0.8

    def __mining(self):
        if self.debug:
            print("Inicio de minería...")
        while self.__is_mining():
            sleep(2)
        if self.debug:
            print("Minería completada.")

    def __moving(self):
        if self.debug:
            print("Moviéndose a un nuevo objetivo...")
        count = 0
        while not self.__is_mining() and count < 10:
            sleep(1)
            count += 1
        if self.debug:
            print("Movimiento completado.")

    def click_at(self, x, y):
        pyautogui.moveTo(x, y)
        pyautogui.click()

    def gathering(self, x, y, resource):
        self.toggle_ath()
        self.current_gathering = Gathering(x, y, resource)
        pyautogui.click(self.current_gathering.x, self.current_gathering.y)
        pyautogui.moveTo(10, 10)
        self.__moving()
        self.__mining()
        self.toggle_ath()

    def toggle_ath(self):
        pyautogui.hotkey('alt', 'h')