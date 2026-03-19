import tkinter as tk
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk
import requests
from io import BytesIO

class BasePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#eef2f7")
        
        # persistent background layer
        self.bg_label = tk.Label(self)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.lower()

        
        self.controller = controller
        self.card = tk.Frame(self, bg="#ffffff", bd=1, relief="solid")
        self.card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.75, relheight=0.75)
        self.create_navbar()
        
        #time and date in top right corner
        self.datetime_label = tk.Label(self, font=("Consolas", 8), fg="#1f4e79")
        self.datetime_label.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)
        self.update_datetime()
        
        #spotify
        self.build_spotify_controls()

        #unplash/jazz background
        self.auto_update_vibe()


    #change vibe every hour by fetching a new background from unsplash and changing the color scheme
    def auto_update_vibe(self):
        # Wait until window has a real size
        if self.winfo_width() < 200 or self.winfo_height() < 200:
            self.after(200, self.auto_update_vibe)
            return

        self.set_background()
        self.apply_theme()
        self.after(3600000, self.auto_update_vibe)

    def apply_theme(self):
        THEMES = {
            "morning": {
                "bg": "#FFF3D6",
                "accent": "#FFD28F",
                "text": "#3A2E2A"
            },
            "afternoon": {
                "bg": "#F2E9D8",
                "accent": "#C9A66B",
                "text": "#2B2B2B"
            },
            "night": {
                "bg": "#1A1A2E",
                "accent": "#16213E",
                "text": "#E0E0E0"
            }
        }

        period = self.get_time_period()
        theme = THEMES[period]

        self.configure(bg=theme["bg"])
        self.spotify_frame.configure(bg=theme["accent"])
        self.track_label.configure(bg=theme["accent"], fg=theme["text"])
        self.datetime_label.configure(bg=theme["bg"], fg=theme["text"])

    def set_background(self):
        BACKGROUND_QUERIES = {
            "morning": "warm morning cafe",
            "afternoon": "jazz afternoon cafe",
            "night": "cozy evening cafe"
        }

        period = self.get_time_period()
        query = BACKGROUND_QUERIES[period]

        img = self.get_unsplash_image(query)

        # Ensure window has a size
        w = max(self.winfo_width(), 300)
        h = max(self.winfo_height(), 300)

        img = img.resize((w, h), Image.LANCZOS)

        self.bg_image = ImageTk.PhotoImage(img)
        self.bg_label.config(image=self.bg_image)

        # keep background behind everything
        self.bg_label.lower()

    def get_unsplash_image(self, query):
        url = (
            f"https://api.unsplash.com/photos/random?"
            f"query={query}&orientation=landscape&client_id=YOUR UNPLASH CLIENT ID"
        )

        response = requests.get(url).json()

        # If Unsplash fails, return a fallback background
        if "urls" not in response:
            print("Unsplash failed:", response)
            # fallback: warm dark café color
            return Image.new("RGB", (800, 600), "#2b2b2b")

        img_url = response["urls"]["regular"]
        img_data = requests.get(img_url).content
        return Image.open(BytesIO(img_data))

    def get_time_period(self):
        hour = datetime.now().hour
        if 6 <= hour < 11:
            return "morning"
        elif 11 <= hour < 17:
            return "afternoon"
        else:
            return "night"


    #SPOTIFY CONTROLS (currently only on main page, but can be added to other pages if desired)
    def build_spotify_controls(self):

        
        # Small square widget in top-left
        self.spotify_frame = tk.Frame(self, bg="white", bd=1, relief="solid", width=200, height=80)
        self.spotify_frame.place(x=50, y=40, anchor="nw")

        # Album art placeholder
        self.album_art_label = tk.Label(self.spotify_frame, bg="white")
        self.album_art_label.grid(row=0, column=0, padx=3, pady=3)

        # Shortened track name
        self.track_label = tk.Label(
            self.spotify_frame,
            text="Loading…",
            font=("Segoe UI", 8, "bold"), 
            bg="white",
            justify="center"
        )
        self.track_label.grid(row=1, column=0, padx=3, pady=3)

        # Reverse / Play-Pause / Forward buttons
        controls = tk.Frame(self.spotify_frame, bg="white")
        controls.grid(row=2, column=0, padx=2, pady=3)

        tk.Button(controls, text="⏮", width=1,
                command=self.controller.spotify.previous).grid(row=0, column=0)

        tk.Button(controls, text="⏯", width=1,
                command=self.toggle_play_pause).grid(row=0, column=1)

        tk.Button(controls, text="⏭", width=1,
                command=self.controller.spotify.next).grid(row=0, column=2)


        #volume slider

        self.volume_slider = ttk.Scale(
            self.spotify_frame,
            from_=0,
            to=100,
            length=100,
            # value=75,
            style="info.Horizontal.TScale",
            command=self.set_volume
        )
        self.volume_slider.grid(row=3, column=0, pady=(0, 5))

        self.update_spotify_display()

    def set_volume(self, value):
        try:
            self.controller.spotify.sp.volume(int(float(value)))
        except:
            pass
        
    def toggle_play_pause(self):
        track = self.controller.spotify.sp.current_playback()
        if track and track["is_playing"]:
            self.controller.spotify.pause()
        else:
            self.controller.spotify.play()

    def update_spotify_display(self):
        track = self.controller.spotify.get_current_track()

        # Update volume slider to match Spotify
        playback = self.controller.spotify.sp.current_playback()
        if playback and "device" in playback:
            current_volume = playback["device"]["volume_percent"]
            self.volume_slider.set(current_volume)

        if track:
            # shorten title to ~20 chars
            short_title = track["name"][:20] + ("…" if len(track["name"]) > 20 else "")
            self.track_label.config(text=short_title)

            # load album art
            try:
                response = requests.get(track["album_art"])
                img = Image.open(BytesIO(response.content))
                img = img.resize((40, 40), Image.LANCZOS)
                self.album_art = ImageTk.PhotoImage(img)
                self.album_art_label.config(image=self.album_art)
            except:
                self.album_art_label.config(image="", text="No Art")

        else:
            self.track_label.config(text="No music")
            self.album_art_label.config(image="", text="")

        self.after(3000, self.update_spotify_display)

    #timer feature in top right corner
    def update_datetime(self):
        now = datetime.now().astimezone()  # gets local timezone automatically
        formatted = now.strftime("%m/%d/%Y | %I:%M %p")
        self.datetime_label.config(text=formatted)

        # update every 1000 ms (1 second)
        self.after(1000, self.update_datetime)

    def create_navbar(self):
        nav = tk.Frame(self.card, bg="#ffffff", padx=8, pady=10)
        # nav = tk.Frame(self, bg="#ffffff", padx=8, pady=10)
        nav.pack(pady=(10, 4))

        tk.Button(
            nav,
            text="Main Page",
            width=12,
            bg="#f1f4f8",
            command=lambda: self.controller.show_frame("MainPage"),
        ).pack(side="left", padx=4)

        tk.Button(
            nav,
            text="Timer",
            width=12,
            bg="#f1f4f8",
            command=lambda: self.controller.show_frame("TimerPage"),
        ).pack(side="left", padx=4)

