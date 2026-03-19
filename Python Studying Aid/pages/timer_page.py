import threading
import time
from pages.base_page import BasePage
import tkinter as tk
import winsound

class TimerPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.sound_loop_active = False
        self.flashing = False
        
        self.is_running = False
        self.remaining_seconds = 25 * 60
        self.timer_job_id = None

        body = tk.Frame(self.card, bg="#ffffff", padx=20, pady=16)
        body.pack(fill="both", expand=True) 

        self.hotkey_instructions = tk.Label(body, text="Hotkeys: Alt+S (Start), Alt+P (Pause), Alt+R (Reset)", font=("Segoe UI", 8), fg="#555555", bg="#ffffff")
        self.hotkey_instructions.pack()

        tk.Label(body, text="Study Timer", font=("Segoe UI", 22, "bold"), bg="#ffffff").pack(pady=(8, 6))

        self.status_label = tk.Label(body, text="Ready", font=("Segoe UI", 10), fg="#555555", bg="#ffffff")
        self.status_label.pack()

        controls = tk.Frame(body, bg="#ffffff", pady=10)
        controls.pack()
    
        self.start_button = tk.Button(controls, text="Start", width=10, command=self.start_timer)
        self.start_button.pack(side="left", padx=5)

        self.pause_button = tk.Button(controls, text="Pause", width=10, command=self.pause_timer, state="disabled")
        self.pause_button.pack(side="left", padx=5)

        tk.Button(controls, text="Reset", width=10, command=self.reset_timer).pack(side="left", padx=5)

        duration_row = tk.Frame(body, bg="#ffffff")
        duration_row.pack()
        
        tk.Label(duration_row, text="Minutes:", font=("Segoe UI", 11), bg="#ffffff").pack(side="left", padx=(0, 8), pady=4)
        self.minutes_entry = tk.Entry(duration_row, width=8, justify="center", font=("Segoe UI", 10))
        self.minutes_entry.insert(0, "25")
        self.minutes_entry.pack(side="left")

        #toggle timer on and off
        self.timer_hidden = False
        # --- TIMER LABEL ---
        self.time_label = tk.Label(body, text="25:00", font=("Consolas", 75, "bold"), fg="#1f4e79")
        self.time_label.pack(pady=(10, 5))
        self.time_label.bind("<Button-1>", lambda _e: self.toggle_timer_display())
        
        # load GIF frames
        self.gif_frames = []
        i = 0
        while True:
            try:
                frame = tk.PhotoImage(file="assets/kirby-running.gif", format=f"gif -index {i}")
                self.gif_frames.append(frame)
                i += 1
            except:
                break
        
        # print("Loaded frames:", len(self.gif_frames))   

        # GIF label (initially hidden)
        self.gif_label = tk.Label(body)
        self.gif_label.pack_forget()
        self.gif_label.bind("<Button-1>", lambda _e: self.toggle_timer_display())
        
        self.animate(0)

        
    def animate(self, i):
        if self.timer_hidden:  # only update when visible
            self.gif_label.configure(image=self.gif_frames[i])

        self.after(50, self.animate, (i+1) % len(self.gif_frames))

    def toggle_timer_display(self):
        self.timer_hidden = not self.timer_hidden

        if self.timer_hidden:
            # Hide timer, show GIF
            self.time_label.pack_forget()
            self.gif_label.pack(pady=(15, 10))
        else:
            # Hide GIF, show timer
            self.gif_label.pack_forget()
            self.time_label.pack(pady=(15, 10))
    
    def flash_text(self):
        if not self.flashing:
            return  # stop flashing when flag is turned off

        current_color = self.time_label.cget("fg")
        new_color = "red" if current_color != "red" else "#1f4e79"  # your normal blue
        self.time_label.config(fg=new_color)

        # repeat every 500ms
        self.after(500, self.flash_text)

    def start_timer(self):
        self.stop_sound_loop()
        self.flashing = False
        self.time_label.config(fg="#1f4e79")  # reset color
        
        if not self.is_running:
            if self.minutes_entry.cget("state") == "normal":
                self.remaining_seconds = self.get_minutes_from_input() * 60
            
            self.is_running = True
            self.start_button.config(state="disabled")
            self.pause_button.config(state="normal")
            self.minutes_entry.config(state="disabled")
            self.status_label.config(text="Running")
            self.tick()

    def pause_timer(self):
        self.is_running = False
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")
        self.status_label.config(text="Paused")

        if self.timer_job_id is not None:
            self.after_cancel(self.timer_job_id)
            self.timer_job_id = None

    def reset_timer(self):
        self.stop_sound_loop()
        self.flashing = False
        self.time_label.config(fg="#1f4e79")  # reset color
        
        self.is_running = False
        if self.timer_job_id is not None:
            self.after_cancel(self.timer_job_id)
            self.timer_job_id = None

        self.remaining_seconds = self.get_minutes_from_input() * 60
        self.update_time_display()
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")
        self.minutes_entry.config(state="normal")
        self.status_label.config(text="Reset")


    def play_sound(self, sound_alias="SystemAsterisk"):
        def _play():
            winsound.PlaySound(sound_alias, winsound.SND_ALIAS)
        threading.Thread(target=_play, daemon=True).start()
        
    def start_sound_loop(self, sound="SystemAsterisk"):
        self.sound_loop_active = True

        def loop():
            while self.sound_loop_active:
                winsound.PlaySound(sound, winsound.SND_ALIAS)
                time.sleep(0.5)  # small delay between repeats

        threading.Thread(target=loop, daemon=True).start()
        
    def stop_sound_loop(self):
        self.sound_loop_active = False 

    def tick(self):
        if not self.is_running:
            return

        if self.remaining_seconds <= 0:
            self.start_sound_loop("SystemAsterisk")
            
            self.status_label.config(text="Completed")
            self.is_running = False
            self.start_button.config(state="normal")
            self.pause_button.config(state="disabled")
            self.minutes_entry.config(state="normal")
            self.timer_job_id = None
            
            self.flashing = True
            self.flash_text()
            return

        
        self.remaining_seconds -= 1
        self.update_time_display()
        self.timer_job_id = self.after(1000, self.tick)

    def update_time_display(self):
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")

    def get_minutes_from_input(self):
        try:
            minutes = int(self.minutes_entry.get())
            return max(0, minutes)
        except ValueError:
            return 25
    