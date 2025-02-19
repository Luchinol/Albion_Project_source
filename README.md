yolo8_detection_project/
│
├── config/
│   └── custom_model.yaml    # (Opcional) Configuración para entrenamiento de un modelo personalizado
│
├── data/
│   └── sample_images/       # Carpeta para imágenes de prueba
│       └── image1.jpg       # Imagen ejemplo para realizar detección
│
├── src/
│   ├── detect.py            # Código para realizar detecciones (inferencia) usando YOLOv8
│   ├── train.py             # Script para entrenar un modelo personalizado (si es necesario)
│   └── utils.py             # Funciones de ayuda, por ejemplo, para procesamiento, post-procesado, etc.
│
├── requirements.txt         # Archivo con las dependencias necesarias, incluyendo Ultralytics y OpenCV
└── README.md                # Documentación del proyecto