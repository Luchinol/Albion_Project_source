import cv2
import numpy as np
import mss
from ultralytics import YOLO

def main():
    # Carga el modelo entrenado (.pt) con YOLOv8
    model_path = "C:/Users/Lenovo/PycharmProjects/CNN_Project/src/runs/detect/train3/weights/best.pt"
    model = YOLO(model_path)

    # Configuración de la ventana para mostrar el resultado (600x400 píxeles)
    window_name = "Detección en tiempo real"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 600, 400)

    # Configurar mss para capturar la pantalla completa
    with mss.mss() as sct:
        # Seleccionamos el monitor principal (según mss, index 1 suele ser la pantalla principal)
        monitor = sct.monitors[1]
        while True:
            # Captura la imagen de la pantalla
            screenshot = sct.grab(monitor)
            # Convierte la imagen a un array de numpy y ajusta el formato de color
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # Realiza la detección en el frame actual
            # Se añade show=False para evitar que el método predict abra otra ventana.
            results = model.predict(frame, conf=0.25, verbose=False, show=False)

            # Obtén el frame anotado con las detecciones (si no hay detecciones, se usa el frame original)
            annotated_frame = results[0].plot() if results and len(results) > 0 else frame

            # Redimensiona el frame anotado a 600x400 para que se muestre en la ventana deseada
            display_frame = cv2.resize(annotated_frame, (600, 400))

            # Muestra el resultado en la ventana redimensionada
            cv2.imshow(window_name, display_frame)

            # Salir del loop si se presiona la tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()