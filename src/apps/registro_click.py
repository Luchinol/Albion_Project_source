from pynput.mouse import Listener

def on_click(x, y, button, pressed):
    if button == button.left and pressed:
        print(f"Clic izquierdo en posición ({x}, {y})")

print("Registrando clics izquierdos. Presiona 'Ctrl + C' para detener.")

with Listener(on_click=on_click) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        print("Se detuvo el registro de clics.")