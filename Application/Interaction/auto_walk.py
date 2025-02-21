import keyboard
import pyautogui
import time
import winsound
from threading import Thread, Event


class AutoWalk:
    def __init__(self):
        self.running = False
        self.program_running = True
        self.stop_event = Event()

        # Frecuencias para los diferentes sonidos
        self.SOUND_START = 1000  # 1000 Hz - Tono más alto para inicio
        self.SOUND_PAUSE = 500  # 500 Hz - Tono medio para pausa
        self.SOUND_EXIT = 250  # 250 Hz - Tono bajo para salida
        self.SOUND_DURATION = 150  # Duración en millisegundos

    def play_sound(self, frequency):
        """Reproduce un sonido con la frecuencia especificada"""
        winsound.Beep(frequency, self.SOUND_DURATION)

    def hold_click(self):
        while not self.stop_event.is_set():
            if self.running:
                pyautogui.mouseDown(button='left')
            time.sleep(0.1)

    def release_click(self):
        pyautogui.mouseUp(button='left')

    def start(self):
        # Asegurar que el mouse esté liberado al inicio
        self.release_click()

        click_thread = Thread(target=self.hold_click)
        click_thread.start()

        print("Programa iniciado")
        print("Presiona '.' para activar")
        print("Presiona ',' para pausar")
        print("Presiona '-' para cerrar")

        while self.program_running:
            if keyboard.is_pressed('.'):  # Iniciar
                if not self.running:  # Solo reproduce el sonido si no estaba activo
                    self.running = True
                    self.play_sound(self.SOUND_START)
                    print("Auto-walk activado")
                    time.sleep(0.3)

            elif keyboard.is_pressed(','):  # Pausar
                if self.running:  # Solo reproduce el sonido si estaba activo
                    self.running = False
                    self.release_click()
                    self.play_sound(self.SOUND_PAUSE)
                    print("Auto-walk pausado")
                    time.sleep(0.3)

            elif keyboard.is_pressed('-'):  # Cerrar
                self.running = False
                self.program_running = False
                self.stop_event.set()
                self.release_click()
                self.play_sound(self.SOUND_EXIT)
                print("Programa finalizado")
                break

            time.sleep(0.1)

        click_thread.join()


if __name__ == "__main__":
    auto_walk = AutoWalk()
    auto_walk.start()