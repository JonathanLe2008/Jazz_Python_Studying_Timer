import tkinter as tk

from pages.main_page import MainPage
from pages.timer_page import TimerPage

from utils.tray import hide_window
from utils.hotkeys import start_hotkey_listener
from utils.spotify_controller import SpotifyController


class StudyingAidApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        #spotify controller instance
        self.spotify = SpotifyController()

        self.title("Python Studying Aid")
        self.resizable(False, False)
        self.configure(bg="#eef2f7")
        center_window(self, width=700, height=500)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page in (MainPage, TimerPage):
            frame = page(parent=self.container, controller=self)
            self.frames[page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")
        
        #when exit out of the app, minimize to system tray instead of closing
        self.protocol("WM_DELETE_WINDOW", lambda: hide_window(self))
        
        #listens for hotkeys 
        start_hotkey_listener(self)
        

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    #hotkey buttons:

    def start_timer_global(self):
        self.frames["TimerPage"].start_timer()

    def pause_timer_global(self):
        self.frames["TimerPage"].pause_timer()

    def reset_timer_global(self):
        self.frames["TimerPage"].reset_timer()

def center_window(window, width=700, height=500):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_pos = (screen_width - width) // 2
    y_pos = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
