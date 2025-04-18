import os
import pyautogui
import time
import threading
from pynput import keyboard
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import sys

# Global variables
is_running = True  # To control screenshot taking
listener_running = True  # To control keylogging
screenshot_interval = 5  # Default interval in seconds
screenshot_folder = "screenshots"
lock = threading.Lock()  # For safely updating interval

# Ensure the screenshots folder exists
os.makedirs(screenshot_folder, exist_ok=True)

# Function to take a screenshot
def take_screenshot():
    global screenshot_interval
    while True:
        if is_running:
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            filename = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
            pyautogui.screenshot(filename)
            print(f"Screenshot saved: {filename}")
        with lock:
            current_interval = screenshot_interval
        time.sleep(current_interval)

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

# Function to update menu items based on the selected interval
def set_interval(icon, item):
    global screenshot_interval

    # Update the interval based on the selected item
    interval_text = item.text.split()[0]
    screenshot_interval = int(interval_text)

    # Update the menu with checkmarks
    update_checkmarks(icon)

    icon.notify(f"Screenshot interval set to {screenshot_interval} seconds.")

# Function to check if the interval should be checked in the menu
def interval_checked(interval_value):
    return lambda item: screenshot_interval == interval_value

# Function to update the checkmarks in the menu
def update_checkmarks(icon):
    # Define the interval menu with checkmarks
    interval_menu = Menu(
        MenuItem("30 seconds", set_interval, checked=interval_checked(30)),
        MenuItem("60 seconds", set_interval, checked=interval_checked(60)),
        MenuItem("120 seconds", set_interval, checked=interval_checked(120)),
        MenuItem("300 seconds", set_interval, checked=interval_checked(300)),
    )

    # Define the main menu
    menu = Menu(
        MenuItem("Pause/Resume Screenshots", toggle_screenshots, checked=is_screenshot_running),
        MenuItem("Pause/Resume Keylogging", toggle_keylogging, checked=is_keylogging_running),
        MenuItem("Set Screenshot Interval", interval_menu),
        MenuItem("Restart", restart_script),
        MenuItem("Exit", stop_script)
    )

    # Update the system tray icon menu with the updated interval menu
    icon.menu = menu  # Reassign updated menu to icon

# Function to stop the script
def stop_script(icon, item):
    global listener
    icon.stop()  # Stops the tray icon
    listener.stop()  # Stops the keylogger
    print("Script stopped.")
    exit(0)

# Function to restart the script
def restart_script(icon, item):
    global listener
    icon.stop()  # Stops the tray icon
    listener.stop()  # Stops the keylogger
    print("Restarting script...")
    os.execv(sys.executable, ['python'] + sys.argv)  # Restart the script

# Function to create the system tray icon
def create_tray_icon():
    # Create an icon image
    icon_image = Image.new("RGB", (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(icon_image)
    draw.ellipse((16, 16, 48, 48), fill=(0, 0, 255))

    # Define the initial interval menu
    interval_menu = Menu(
        MenuItem("30 seconds", set_interval, checked=interval_checked(30)),
        MenuItem("60 seconds", set_interval, checked=interval_checked(60)),
        MenuItem("120 seconds", set_interval, checked=interval_checked(120)),
        MenuItem("300 seconds", set_interval, checked=interval_checked(300)),
    )

    # Define the main menu
    menu = Menu(
        MenuItem("Pause/Resume Screenshots", toggle_screenshots, checked=is_screenshot_running),
        MenuItem("Pause/Resume Keylogging", toggle_keylogging, checked=is_keylogging_running),
        MenuItem("Set Screenshot Interval", interval_menu),
        MenuItem("Restart", restart_script),
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
