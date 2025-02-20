import cv2 as cv
import numpy as np
import mss
from ultralytics import YOLO
from time import time
from math import sqrt


class MSSCapture:
    """
    Captura de pantalla utilizando mss.
    Se encarga de capturar el monitor principal y provee:
      - screenshot(): devuelve la imagen en formato RGB.
      - window: un objeto simple con las propiedades left, top, width y height.
    """

    def __init__(self, monitor_number=1):
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[monitor_number]

        class Window:
            pass

        self.window = Window()
        self.window.left = self.monitor['left']
        self.window.top = self.monitor['top']
        self.window.width = self.monitor['width']
        self.window.height = self.monitor['height']

    def screenshot(self):
        sct_img = self.sct.grab(self.monitor)
        img = np.array(sct_img)
        # Convertir de BGRA a RGB
        return cv.cvtColor(img, cv.COLOR_BGRA2RGB)


class AlbionDetection:
    IMG_SIZE = 640
    CONFIDENCE = 0.5

    def __init__(self,
                 model_path="C:/Users/Lenovo/PycharmProjects/CNN_Project/src/runs/detect/train2/weights/best.pt",
                 debug=False,
                 confidence=CONFIDENCE,
                 window_name="Albion Online Client"):
        """
        Inicializa el objeto AlbionDetection usando YOLOv8 y mss para la captura.

        :param model_path: Ruta al modelo YOLOv8 (.pt).
        :param debug: Activa el modo debug para mostrar la imagen anotada.
        :param confidence: Umbral de confianza para las detecciones.
        :param window_name: (No se utiliza aquí pero se deja como parámetro para compatibilidad).
        """
        self.model_name = model_path
        self.model = self._load_model()
        self.classes = self._load_classes()
        self.window_capture = MSSCapture()
        self.debug = debug
        self.confidence = confidence
        self.character_position_X = self.IMG_SIZE / 2
        self.character_position_Y = self.IMG_SIZE / 2 - 60

    def _process_image(self, img):
        """
        Preprocesa la imagen capturada.

        :param img: Imagen en RGB.
        :return: Imagen en BGR redimensionada a IMG_SIZE x IMG_SIZE.
        """
        # Convertir de RGB a BGR (OpenCV trabaja en BGR)
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        return cv.resize(img, (self.IMG_SIZE, self.IMG_SIZE))

    def _load_classes(self):
        """
        Carga los nombres de clases a partir del modelo YOLOv8 entrenado.
        Se accede a los nombres de las clases a través de model.model.names.

        :return: Diccionario con id --> { "label": nombre, "color": color (RGB) }.
        """
        classes = {}
        names = self.model.model.names if hasattr(self.model, "model") and hasattr(self.model.model, "names") else {}
        for k, v in names.items():
            # Se asigna un color basado en el id (mod 256 para que esté en rango válido)
            classes[k] = {"label": v, "color": (0, 255, (int(k) * 10) % 256)}
        return classes

    def draw_boxes(self, img, coordinates):
        """
        Dibuja las cajas detectadas sobre la imagen y marca la detección más cercana.

        :param img: Imagen sobre la que se dibuja.
        :param coordinates: Lista de detecciones con el formato [x1, y1, x2, y2, confidence, class].
        """
        for coord in coordinates:
            x1, y1, x2, y2 = int(coord[0]), int(coord[1]), int(coord[2]), int(coord[3])
            confidence = coord[4]
            class_id = int(coord[5])
            class_info = self.classes.get(class_id, {"label": "Unknown", "color": (0, 255, 0)})
            cv.rectangle(img, (x1, y1), (x2, y2), class_info["color"], 2)
            label = f"{class_info['label']} {confidence:.2f}"
            cv.putText(img, label, (x1, y1 - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, class_info["color"], 2)
        self.__cross_line(img)
        cv.drawMarker(img, (int(self.character_position_X), int(self.character_position_Y)),
                      (255, 255, 255), cv.MARKER_DIAMOND, 10, 2)
        self.__marker_closest(img, coordinates)

    def __cross_line(self, img):
        """
        Dibuja líneas de referencia (una horizontal y una vertical) según la posición base.
        """
        cv.line(img, (0, int(self.character_position_Y)), (self.IMG_SIZE, int(self.character_position_Y)),
                (255, 255, 255), 2)
        cv.line(img, (int(self.character_position_X), 0), (int(self.character_position_X), self.IMG_SIZE),
                (255, 255, 255), 2)

    def __marker_closest(self, img, coordinates):
        """
        Marca la detección cuyo centro está más cerca del punto de referencia.
        """
        closest = self.closest_point(coordinates)
        if closest is not None:
            cv.drawMarker(img, (int(closest[0]), int(closest[1])), (37, 150, 190),
                          cv.MARKER_CROSS, 10, 2)
            cv.putText(img, "Closest", (int(closest[0]), int(closest[1]) + 50),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    def closest_point(self, coordinates):
        """
        Calcula la detección cuya caja (centro) se encuentra más cerca del punto base.

        :param coordinates: Lista de detecciones.
        :return: Tuple (center_x, center_y, class_id) o None si no hay detecciones.
        """
        if len(coordinates) == 0:
            return None

        min_distance = float("inf")
        selected = None
        for coord in coordinates:
            x1, y1, x2, y2 = int(coord[0]), int(coord[1]), int(coord[2]), int(coord[3])
            center_x = x1 + (x2 - x1) / 2
            center_y = y1 + (y2 - y1) / 2
            distance = sqrt((self.character_position_X - center_x) ** 2 +
                            (self.character_position_Y - center_y) ** 2)
            if distance < min_distance:
                min_distance = distance
                selected = (center_x, center_y, int(coord[5]))
        return selected

    def __convert_coordinates_to_screen_position(self, center_x, center_y):
        """
        Convierte las coordenadas de la imagen procesada a las coordenadas reales de la pantalla.
        """
        screen_x = ((center_x * self.window_capture.window.width) / self.IMG_SIZE) + self.window_capture.window.left
        screen_y = ((center_y * self.window_capture.window.height) / self.IMG_SIZE) + self.window_capture.window.top
        return screen_x, screen_y

    def _load_model(self):
        """
        Carga el modelo YOLOv8 entrenado usando la librería ultralytics.

        :return: Modelo YOLOv8 cargado.
        """
        try:
            model = YOLO(self.model_name)
        except Exception as e:
            raise Exception(f"Failed to load the model: {e}")
        return model

    def predict(self):
        """
        Realiza la detección sobre la imagen capturada.

        :return: Tuple (screen_center_x, screen_center_y, class_id, imagen)
        """
        loop_time = time()
        img = self._process_image(self.window_capture.screenshot())
        results = self.model.predict(img, conf=self.confidence, verbose=False, show=False)
        coordinates = []
        if results and results[0].boxes is not None:
            # Cada detección es una lista: [x1, y1, x2, y2, confidence, class]
            coordinates = [coord for coord in results[0].boxes.data.tolist() if coord[4] >= self.confidence]

        if self.debug:
            annotated_img = results[0].plot() if results and results[0].boxes is not None else img
            cv.putText(annotated_img, f'FPS {1 / (time() - loop_time):.2f}', (10, 20),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv.imshow("Founded", annotated_img)

        if not coordinates:
            return None, None, None, img

        closest = self.closest_point(coordinates)
        if closest is None:
            return None, None, None, img

        center_x, center_y, class_id = closest
        screen_x, screen_y = self.__convert_coordinates_to_screen_position(center_x, center_y)
        return screen_x, screen_y, class_id, img