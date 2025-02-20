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

    def __check_exit(self):
        """
        Verifica si se ha presionado la tecla ',' y, de ser así, finaliza el programa.
        """
        if cv.waitKey(1) & 0xFF == ord(','):
            if self.debug:
                print("Tecla ',' presionada. Finalizando el programa.")
            exit()


    # def gathering(self, x, y, resource):
    #     """
    #     Lanza el proceso para realizar una acción de gathering:
    #       - Abre la ventana de interacción (mediante toggle de hotkey).
    #       - Da click en la posición objetivo.
    #       - Espera a que inicie el modo gathering (se verifica la presencia de la barra verde).
    #       - Espera a que finalice el modo gathering antes de cerrar la ventana de interacción.
    #
    #     :param x: Coordenada x donde se debe hacer click.
    #     :param y: Coordenada y donde se debe hacer click.
    #     :param resource: Identificador o dato adicional del recurso a recolectar.
    #     """
    #     self.toggle_ath()
    #     self.current_gathering = Gathering(x, y, resource)
    #     pyautogui.click(self.current_gathering.x, self.current_gathering.y)
    #     pyautogui.moveTo(10, 10)
    #     self.__moving()
    #     self.__mining()
    #     self.toggle_ath()


    def __mining(self):
        """
        Espera a que el modo gathering (indicador verde) finalice.
        """
        if self.debug:
            print("Inicio de gathering...")
        while self.__is_gathering():
            self.__check_exit()  # Verifica si se presionó la tecla ',' para salir
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
            self.__check_exit()  # Verifica si se presionó la tecla ',' para salir
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

