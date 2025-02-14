import os
import pyautogui
import time
import threading
from pynput import keyboard
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox

# Global variables
is_running = True  # To control screenshot taking
listener_running = True  # To control keylogging
screenshot_interval = 60  # Default interval in seconds
screenshot_folder = "screenshots"

# Ensure the screenshots folder exists
os.makedirs(screenshot_folder, exist_ok=True)

# Function to take a screenshot
def take_screenshot():
    while True:
        if is_running:
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            filename = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
            pyautogui.screenshot(filename)
            print(f"Screenshot saved: {filename}")
        time.sleep(screenshot_interval)

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

# Function to set screenshot interval
def set_interval(icon, item):
    global screenshot_interval
    screenshot_interval = int(item.text.split()[0])  # Parse interval from menu item text
    icon.notify(f"Screenshot interval set to {screenshot_interval} seconds.")

# Function to set custom interval using a tkinter slider
def set_custom_interval(icon, item):
    global screenshot_interval

    def apply_custom_interval():
        custom_value = int(slider.get())
        screenshot_interval = custom_value * 60  # Convert minutes to seconds
        icon.notify(f"Custom interval set to {custom_value} minute(s).")
        root.destroy()

    # Create tkinter root window
    root = tk.Tk()
    root.title("Set Custom Interval")
    root.geometry("400x200")
    root.resizable(False, False)

    # Slider Label
    tk.Label(root, text="Select interval (in minutes):", font=("Arial", 12)).pack(pady=10)

    # Slider widget
    slider = tk.Scale(
        root, from_=1, to=180, orient="horizontal", length=300, tickinterval=30, resolution=1
    )
    slider.set(screenshot_interval // 60)  # Default to current interval in minutes
    slider.pack(pady=10)

    # Apply button
    apply_button = tk.Button(root, text="Apply", command=apply_custom_interval)
    apply_button.pack(pady=10)

    root.mainloop()

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

    # Define menu items
    interval_menu = Menu(
        MenuItem("30 seconds", set_interval),
        MenuItem("60 seconds", set_interval),
        MenuItem("120 seconds", set_interval),
        MenuItem("300 seconds", set_interval),
        MenuItem("Custom", set_custom_interval),
    )
    menu = Menu(
        MenuItem("Pause/Resume Screenshots", toggle_screenshots, checked=is_screenshot_running),
        MenuItem("Pause/Resume Keylogging", toggle_keylogging, checked=is_keylogging_running),
        MenuItem("Set Screenshot Interval", interval_menu),
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
