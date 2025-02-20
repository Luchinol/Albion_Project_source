from ultralytics import YOLO
import torch

def main():
    data_path = "C:/Users/Lenovo/PycharmProjects/CNN_Project/data/dataset_roboflow/dataset_1/data.yaml"
    model = YOLO("yolov8s.pt")  # Moodelos yolov8n.pt,  yolov8s.pt (x3 tiempo)

    # Seleccionar GPU si está disponible y tiene memoria suficiente, de lo contrario usar CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model.train(
        data=data_path,
        epochs=50,
        imgsz=640,
        batch=4,          # Ajustado para hardware limitado
        workers=2,
        device=device,
        amp=False,        # Desactivar precisión mixta si se usa CPU
        optimizer="AdamW",
        augment=True,
        cache="ram",      # Prueba a usar RAM si tienes suficiente (consumo depende del dataset), si notas que el uso de RAM es excesivo, prueba cache=False.
        visualize=False   # Se puede activar después con model.val()
    )

    print(f"Entrenamiento completado en {device.upper()}.")

if __name__ == "__main__":
    main()
