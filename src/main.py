import cv2 as cv
import time

from Albion.detection import AlbionDetection
from Application.Interaction.interaction import Interaction
from Capture.Windows import WindowsCapture

def run_detection():
    # Inicializar el detector sobre la ventana completa
    model = AlbionDetection(debug=True, confidence=0.9)
    window_name = "Detección en pantalla completa"
    cv.namedWindow(window_name, cv.WINDOW_NORMAL)
    cv.resizeWindow(window_name, 800, 600)

    while True:
        # Se obtiene la predicción y se visualiza la imagen anotada
        x, y, resource, annotated_img = model.predict()
        cv.imshow(window_name, annotated_img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()

def run_interaction():
    # Flujo de interacción con detección e interacción
    model = AlbionDetection(debug=True, confidence=0.8)
    interaction = Interaction(model)

    # Se obtiene la posición central detectada y el recurso asociado
    x, y, resource, _ = model.predict()
    interaction.gathering(x, y, resource)

    # Mantener abierto para visualizar hasta presionar 'q'
    while True:
        if cv.waitKey(1) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            break

if __name__ == "__main__":
    # Seleccionar el flujo deseado:
    run_detection()
    # O bien:
    # run_interaction()