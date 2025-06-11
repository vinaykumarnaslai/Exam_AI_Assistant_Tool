# main.py
import keyboard
import threading
from gui import open_floating_window

def listen_shortcut():
    print("Listening for Ctrl + Alt + V...")
    keyboard.add_hotkey('ctrl+alt+v', open_floating_window)
    keyboard.wait()  # Keeps the script running

if __name__ == "__main__":
    threading.Thread(target=listen_shortcut).start()
