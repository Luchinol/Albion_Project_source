from ultralytics import YOLO

def main():
    # Ruta al archivo YAML; ajústala según tu estructura de carpetas.
    data_path = "C:/Users/Lenovo/PycharmProjects/CNN_Project/data/dataset_roboflow/dataset_1/data.yaml"
    # Carga el modelo pre-entrenado, puedes variar a un modelo diferente (por ejemplo, yolov8s.pt)
    model = YOLO("yolov8n.pt")

    # Inicia el entrenamiento configurando los parámetros: epochs, tamaño de imagen, etc.
    model.train(data=data_path, epochs=50, imgsz=640)
    print("Entrenamiento completado.")

if __name__ == "__main__":
    main()

