import cv2
from time import time
from Application.Albion.detection import AlbionDetection
from Application.Interaction.interaction import Interaction

def main():
    model_path = "C:/Users/Lenovo/PycharmProjects/CNN_Project/src/runs/detect/train2/weights/best.pt"
    detector = AlbionDetection(model_path=model_path, debug=True, confidence=0.5, window_name="Albion Online Client")
    interaction = Interaction(detector)  # Se pasa el detector para la interacción

    while True:
        start_time = time()
        center_x, center_y, resource, annotated_img = detector.predict()

        if center_x is not None and center_y is not None:
            interaction.click_at(int(center_x), int(center_y))

        cv2.imshow("Detection", annotated_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        print(f"FPS: {1 / (time() - start_time):.2f}")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()