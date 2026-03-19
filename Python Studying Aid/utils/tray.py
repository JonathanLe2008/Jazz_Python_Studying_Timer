import threading
import pystray
from PIL import Image

#you use app bc The self you pass in is the Tkinter window object (tk.Tk), NOT your tray module.

def hide_window(app):
    app.withdraw()
    create_tray_icon(app)

def show_window(app, icon, item):
    icon.stop()
    app.after(0, app.deiconify)

def quit_app(app, icon, item):
    icon.stop()
    app.after(0, app.destroy)

def create_tray_icon(app):
    image = Image.open("assets/cafe_taskbar_icon.jpg")

    menu = pystray.Menu(
        pystray.MenuItem(
            "Open",
            lambda icon, item: show_window(app, icon, item),
            default=True  # THIS ENABLES LEFT-CLICK
        ),
        pystray.MenuItem(
            "Quit",
            lambda icon, item: quit_app(app, icon, item)
        )
    )

    icon = pystray.Icon("cafe-image", image, "Studying Aid", menu)

    def run_icon():
        icon.run()

    threading.Thread(target=run_icon, daemon=True).start()


