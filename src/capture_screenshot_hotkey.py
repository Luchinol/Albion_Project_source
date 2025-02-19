import os
import glob
from PIL import ImageGrab
import keyboard
import time

def capture_and_save(target_folder: str):
    """
    Captura la pantalla y guarda la imagen en target_folder con numeración secuencial.
    """
    # Crear la carpeta destino si no existe
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Buscar imágenes existentes que sigan el patrón "image*.jpg"
    pattern = os.path.join(target_folder, "image*.jpg")
    files = glob.glob(pattern)

    # Determinar el número máximo actual a partir de los nombres de fichero existentes
    max_index = 0
    for f in files:
        basename = os.path.basename(f)
        try:
            # Se espera un formato "image<number>.jpg"
            number = int(basename.replace("image", "").replace(".jpg", ""))
            max_index = max(max_index, number)
        except ValueError:
            continue

    next_index = max_index + 1
    filename = os.path.join(target_folder, f"image{next_index}.jpg")

    try:
        # Capturar la pantalla y guardar la imagen
        screenshot = ImageGrab.grab()
        screenshot.save(filename, "JPEG")
        print(f"Screenshot captured and saved as: {filename}")
    except Exception as e:
        print(f"Error capturing screen: {e}")

def main():
    # Definir la carpeta de destino. Desde src/ la ruta relativa es "../data/sample_images"
    target_folder = os.path.join("..", "data", "sample_images")
    print("Iniciando el capturador de pantalla.")
    print("Presiona '.' para capturar un screenshot y 'q' para salir.")

    # Definir la acción para la tecla punto, usando un pequeño retardo para evitar detecciones duplicadas
    keyboard.add_hotkey(".", lambda: (capture_and_save(target_folder), time.sleep(0.2)))
    # Espera hasta que se presione la tecla 'q' para salir
    keyboard.wait("q")
    print("Saliendo del programa.")

if __name__ == '__main__':
    main()