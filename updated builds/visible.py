from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading
import keyboard

# Global variables
tray_icon = None
icon_visible = False  # Initially hidden

def create_image():
    """Create an icon image."""
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), fill=(0, 0, 255))
    draw.ellipse((16, 16, 48, 48), fill=(255, 0, 0))
    return image

def create_tray_icon():
    """Create a new tray icon."""
    menu = Menu(MenuItem("Quit", lambda: on_quit()))
    return Icon("TestIcon", create_image(), "My Tray Icon", menu)

def toggle_tray_icon():
    """Toggle the visibility of the tray icon."""
    global tray_icon, icon_visible

    if icon_visible:
        tray_icon.stop()
        tray_icon = None
    else:
        tray_icon = create_tray_icon()
        threading.Thread(target=tray_icon.run, daemon=True).start()
    icon_visible = not icon_visible

def on_quit():
    """Quit the application."""
    global tray_icon
    if tray_icon:
        tray_icon.stop()
    exit(0)

def main():
    global tray_icon

    # Initially, the tray icon is hidden (not created)

    # Listen for a shortcut (e.g., Ctrl+Shift+T)
    keyboard.add_hotkey("ctrl+shift+t", toggle_tray_icon)

    print("Press Ctrl+Shift+T to toggle the tray icon visibility.")
    print("Press Ctrl+C to exit.")
    try:
        keyboard.wait("ctrl+c")  # Keep the script running
    except KeyboardInterrupt:
        print("\nExiting...")
        on_quit()

if __name__ == "__main__":
    main()
