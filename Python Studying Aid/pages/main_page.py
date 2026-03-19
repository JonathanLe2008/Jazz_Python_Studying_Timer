from pages.base_page import BasePage
import tkinter as tk

class MainPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        body = tk.Frame(self.card, bg="#ffffff", padx=20, pady=16)
        body.pack(fill="both", expand=True)

        tk.Label(body, text="Welcome", font=("Segoe UI", 24, "bold"), bg="#ffffff").pack(pady=(20, 8))

        info = (    
            "Application will be in taskbar when X out, right click to open and close"
        )
        tk.Label(body, text=info, justify="center", anchor = 'center', font=("Segoe UI", 11), bg="#ffffff").pack()
        
        tk.Label(body, text="KEEP GOING!", justify="center", anchor = 'center', font=("Segoe UI", 20), bg="#ffffff").pack(pady=(20, 0))
        