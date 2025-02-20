import cv2 as cv
import numpy as np
import pyautogui
from time import sleep

from Application.Albion.detection import AlbionDetection

class Gathering:
    def __init__(self, x, y, resource):
        self.x = x
        self.y = y
        self.resource = resource

class Interaction:
    def __init__(self, model: AlbionDetection, green_threshold: float = 0.3):
        """
        Inicializa la clase Interaction usando la detección de color para identificar el modo gathering.

        :param model: Instancia de AlbionDetection que permite obtener capturas de pantalla.
        :param green_threshold: Porcentaje mínimo de píxeles verdes en la región de interés para considerar que
                                el modo gathering está activo.
        """
        self.model = model
        self.current_gathering: Gathering | None = None
        self.debug = self.model.debug
        self.green_threshold = green_threshold

    def __is_gathering(self) -> bool:
        """
        Determina si la interfaz del juego muestra el modo gathering basándose en la detección de una barra verde en una
        región fija (definida por coordenadas).

        :return: True si la proporción de píxeles verdes en la región supera el umbral, False en caso contrario.
        """
        # Se obtiene la imagen preprocesada (redimensionada a 640x640)
        img = self.model._process_image(self.model.window_capture.screenshot())

        # Definir la región de interés donde se espera la barra verde
        # En este ejemplo, se usa el rectángulo con esquina superior izquierda en (265, 365) y esquina inferior derecha en (293, 410)
        x1, y1, x2, y2 = 852, 669, 1109, 688
        region = img[y1:y2, x1:x2]

        # Convertir la región a espacio HSV para facilitar la segmentación de colores
        hsv = cv.cvtColor(region, cv.COLOR_BGR2HSV)
        lower_green = np.array([40, 100, 100])
        upper_green = np.array([80, 255, 255])
        mask = cv.inRange(hsv, lower_green, upper_green)
        count_green = cv.countNonZero(mask)
        total_pixels = region.shape[0] * region.shape[1]
        ratio = count_green / total_pixels

        if self.debug:
            print("Green ratio in region:", ratio)

        return ratio >= self.green_threshold

    def __mining(self):
        """
        Espera a que el modo gathering (indicador verde) finalice.
        """
        if self.debug:
            print("Inicio de gathering...")
        while self.__is_gathering():
            sleep(2)
        if self.debug:
            print("Gathering completado.")

    def __moving(self):
        """
        Espera a que se detecte el inicio del modo gathering (la barra verde aparezca) para proceder al siguiente paso.
        """
        if self.debug:
            print("Moviéndose a un nuevo objetivo...")
        count = 0
        while not self.__is_gathering() and count < 10:
            sleep(1)
            count += 1
        if self.debug:
            print("Movimiento completado.")

    def click_at(self, x, y):
        """
        Realiza un click en la posición dada.
        """
        pyautogui.moveTo(x, y)
        pyautogui.click()

    def gathering(self, x, y, resource):
        """
        Lanza el proceso para realizar una acción de gathering:
          - Abre la ventana de interacción (mediante toggle de hotkey).
          - Da click en la posición objetivo.
          - Espera a que inicie el modo gathering (se verifica la presencia de la barra verde).
          - Espera a que finalice el modo gathering antes de cerrar la ventana de interacción.

        :param x: Coordenada x donde se debe hacer click.
        :param y: Coordenada y donde se debe hacer click.
        :param resource: Identificador o dato adicional del recurso a recolectar.
        """
        self.toggle_ath()
        self.current_gathering = Gathering(x, y, resource)
        pyautogui.click(self.current_gathering.x, self.current_gathering.y)
        pyautogui.moveTo(10, 10)
        self.__moving()
        self.__mining()
        self.toggle_ath()

    def toggle_ath(self):
        """
        Envía la combinación de teclas para abrir o cerrar la ventana de interacción (por ejemplo, Alt+H).
        """
        pyautogui.hotkey('alt', 'h')

# Ejemplo de uso:
if __name__ == "__main__":
    detection = AlbionDetection(debug=True)
    # Se crea el objeto de interacción usando el método de análisis de color.
    interaction = Interaction(detection, green_threshold=0.3)

    # Ejemplo: simular una acción de gathering en coordenadas (x, y) y con recurso 'gold'
    interaction.gathering(500, 500, resource="gold")