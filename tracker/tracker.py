import time
import pygetwindow as gw
import psutil
from pynput import mouse, keyboard
import threading

class ActivityMonitor:
    def __init__(self):
        self.last_input_time = time.time()
        self.keyboard_activity = False
        self.mouse_activity = False
        self.start_listeners()

    def start_listeners(self):
        def on_press(key):
            self.keyboard_activity = True
            self.last_input_time = time.time()

        def on_move(x, y):
            self.mouse_activity = True
            self.last_input_time = time.time()

        mouse.Listener(on_move=on_move).start()
        keyboard.Listener(on_press=on_press).start()

    def get_active_window(self):
        try:
            window = gw.getActiveWindow()
            return window.title if window else "Unknown"
        except:
            return "Unknown"

    def get_idle_time(self):
        return int(time.time() - self.last_input_time)

    def reset_activity_flags(self):
        self.mouse_activity = False
        self.keyboard_activity = False
