import threading
import keyboard

#you use app bc the self you pass in is the Tkinter window object (tk.Tk), NOT your tray module.

def start_hotkey_listener(app):
    def listen():
        keyboard.add_hotkey("alt+s", app.start_timer_global) 
        keyboard.add_hotkey("alt+p", app.pause_timer_global)
        keyboard.add_hotkey("alt+r", app.reset_timer_global)
        keyboard.wait()

    thread = threading.Thread(target=listen, daemon=True)
    thread.start()
