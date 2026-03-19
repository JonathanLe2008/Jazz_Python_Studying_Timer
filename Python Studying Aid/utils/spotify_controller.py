import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyController:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="YOUR CLIENT ID",
            client_secret="YOUR CLIENT SECRET ID",
            redirect_uri="http://127.0.0.1:8000/callback",
            scope="user-read-playback-state user-modify-playback-state user-read-currently-playing"
        ))

    # --- Playback Controls ---
    def play(self):
        self.sp.start_playback()

    def pause(self):
        self.sp.pause_playback()

    def next(self):
        self.sp.next_track()

    def previous(self):
        self.sp.previous_track()

    def play_playlist(self, playlist_uri):
        self.sp.start_playback(context_uri=playlist_uri)

    # --- Track Info ---
    def get_current_track(self):
        data = self.sp.current_user_playing_track()
        if not data or not data.get("item"):
            return None

        item = data["item"]
        return {
            "name": item["name"],
            "artist": item["artists"][0]["name"],
            "album_art": item["album"]["images"][2]["url"]  # 64x64 image 
        }

