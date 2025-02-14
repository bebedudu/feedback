# terminal based update
import os
import sys
import requests
import subprocess
import time
from pystray import MenuItem as item, Menu, Icon
from PIL import Image
from tqdm import tqdm  # Progress bar

# Global constants
CURRENT_VERSION = "1.0.0"  # Define your program's current version
VERSION_URL = "https://raw.githubusercontent.com/bebedudu/autoupdate/refs/heads/main/latest_version.tx"  # URL to check the latest version
BASE_DOWNLOAD_URL = "https://github.com/bebedudu/autoupdate/releases/download"  # Base GitHub Releases URL
APP_NAME = "Keylogger.exe"  # Name of the executable

def check_for_update():
    try:
        # Step 1: Check for updates
        response = requests.get(VERSION_URL)
        response.raise_for_status()  # Raise an error if the request fails
        latest_version = response.text.strip()

        if latest_version > CURRENT_VERSION:
            print(f"Update available! Latest version: {latest_version}")
            result = input("Do you want to update now? (yes/no): ").lower()
            if result == "yes":
                download_update(latest_version)
        else:
            print("You are already using the latest version!")
    except Exception as e:
        print(f"Error checking for updates: {e}")

def download_update(latest_version):
    try:
        # Step 2: Dynamically construct the download URL
        download_url = f"{BASE_DOWNLOAD_URL}/v{latest_version}/{APP_NAME}"
        print(f"Downloading update from: {download_url}")

        # Step 3: Download the updated file with progress tracking
        response = requests.get(download_url, stream=True)
        response.raise_for_status()  # Raise an error if the download fails

        # Get the total file size from the headers
        total_size = int(response.headers.get("Content-Length", 0))

        start_time = time.time()
        with open("update_temp.exe", "wb") as f, tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc="Downloading",
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive chunks
                    f.write(chunk)
                    progress_bar.update(len(chunk))

        # Calculate and display download time
        elapsed_time = time.time() - start_time
        print(f"\nDownload completed in {elapsed_time:.2f} seconds!")

        # Step 4: Replace the old executable
        update_path = os.path.join(os.getcwd(), "update_temp.exe")
        current_path = os.path.join(os.getcwd(), APP_NAME)

        os.rename(current_path, f"{current_path}.old")  # Backup old version
        os.rename(update_path, current_path)

        print("Update completed successfully!")
        restart_program()
    except Exception as e:
        print(f"Error updating program: {e}")

def restart_program():
    subprocess.Popen([sys.executable, APP_NAME])  # Restart the updated program
    sys.exit()

def quit_app(icon, item):
    icon.stop()

def main():
    # System tray icon setup
    image = Image.new("RGB", (64, 64), "blue")
    menu = Menu(
        item("Update Program", lambda: check_for_update()),
        item("Quit", quit_app)
    )
    icon = Icon("MyApp", image, "My Application", menu)
    icon.run()

if __name__ == "__main__":
    main()



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------



# without system tray 
import os
import sys
import requests
import time
import threading
import tkinter as tk
from plyer import notification
from tkinter import ttk, messagebox

CURRENT_VERSION = "1.1.0"
VERSION_URL = "https://raw.githubusercontent.com/bebedudu/autoupdate/refs/heads/main/latest_version.tx"
BASE_DOWNLOAD_URL = "https://github.com/bebedudu/autoupdate/releases/download"
APP_NAME = "Keylogger.exe"


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
    print(f"icon is at {ICON_PATH}")
except Exception as e:
    print(f"Error creating image folder: {e}")
    raise SystemExit(f"Error: Unable to create image folder. {e}")


# Determine the application directory for log files
# ----------------------------------------------------------------------------------
if getattr(sys, 'frozen', False):  # Bundled as .exe
    app_dir = os.path.dirname(sys.executable)
else:  # Running as a script
    app_dir = os.path.dirname(os.path.abspath(__file__))

# Define the logs folder and log file path
logs_folder = os.path.join(app_dir, "v110")
# Ensure the logs folder exists
try:
    os.makedirs(logs_folder, exist_ok=True)  # Create logs folder if it doesn't exist
    print(f"v110 folder is at {logs_folder}")
except Exception as e:
    print(f"Error creating v110 folder: {e}")
    raise SystemExit(f"Error: Unable to create v110 folder. {e}")


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
        print(f"Notification Error: {e}")

show_notification(APP_NAME, f"test app version v1.1.0")


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
        return f"{seconds / 60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds / 3600:.2f} hours"
    else:
        return f"{seconds / 86400:.2f} days"

class UpdaterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Updater")
        self.root.geometry("400x250")

        # self.label = ttk.Label(root, text="Initializing...")
        self.label = ttk.Label(root, text="Click 'Check for Updates' to start.")
        self.label.pack(pady=10)

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.status_label = ttk.Label(root, text="", font=("Arial", 10))
        self.status_label.pack(pady=5)

        self.time_label = ttk.Label(root, text="", font=("Arial", 10))
        self.time_label.pack(pady=5)

        self.check_button = ttk.Button(root, text="Check for Updates", command=self.check_for_update)
        self.check_button.pack(pady=5)

        self.quit_button = ttk.Button(root, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=5)
        
        # Automatically check for updates when the app starts
        # self.check_for_update()


    def check_for_update(self):
        self.label.config(text="Checking for updates...")
        threading.Thread(target=self._check_for_update_thread).start()

    def _check_for_update_thread(self):
        # try:
        #     response = requests.get(VERSION_URL)
        #     response.raise_for_status()
        #     latest_version = response.text.strip()

        #     if latest_version > CURRENT_VERSION:
        #         self.label.config(text=f"Update available: v{latest_version}")
        #         if messagebox.askyesno("Update Available", f"A new version (v{latest_version}) is available. Update now?"):
        #             self.download_update(latest_version)
        #     else:
        #         self.label.config(text="You are already using the latest version.")
        # except Exception as e:
        #     self.label.config(text="Error checking for updates.")
        #     messagebox.showerror("Error", f"Failed to check for updates: {e}")
        
        
        
        try:
            # Fetch the latest version
            response = requests.get(VERSION_URL, timeout=10)  # Timeout to avoid hanging
            response.raise_for_status()
            latest_version = response.text.strip()

            if latest_version > CURRENT_VERSION:
                self.label.config(text=f"Update available: v{latest_version}")
                show_notification("Update Available", f"New version v{latest_version} is available.")

                # Prompt user to update
                if messagebox.askyesno("Update Available", f"A new version (v{latest_version}) is available. Would you like to update now?"):
                    self.download_update(latest_version)
                else:
                    self.label.config(text="Update postponed by the user.")
            else:
                self.label.config(text="You are already using the latest version.")
                show_notification("No Update", "You are using the latest version.")
        except requests.exceptions.RequestException as e:
            self.label.config(text="Error checking for updates.")
            show_notification("Error", "Failed to check for updates. Please try again later.")
            messagebox.showerror("Error", f"Failed to check for updates: {e}")
        
        

    def download_update(self, latest_version):
        try:
            download_url = f"{BASE_DOWNLOAD_URL}/v{latest_version}/{APP_NAME}"
            self.label.config(text="Downloading update...")

            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            total_size = int(response.headers.get("Content-Length", 0))

            self.progress_bar["maximum"] = total_size
            downloaded_size = 0
            start_time = time.time()

            with open("update_temp.exe", "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        self.progress_bar["value"] = downloaded_size

                        # Calculate and update status
                        elapsed_time = time.time() - start_time
                        speed = downloaded_size / elapsed_time  # Bytes per second
                        remaining_time = (total_size - downloaded_size) / speed if speed > 0 else 0

                        self.status_label.config(
                            text=f"Downloaded: {format_size(downloaded_size)} of {format_size(total_size)}"
                        )
                        self.time_label.config(
                            text=f"Speed: {format_size(speed)}/s | Remaining Time: {format_time(remaining_time)}"
                        )
                        self.root.update()

            self.label.config(text="Download completed successfully!")
            self.replace_executable()
        except Exception as e:
            self.label.config(text="Error during download.")
            messagebox.showerror("Error", f"Failed to download update: {e}")

    def replace_executable(self):
        try:
            current_path = os.path.join(os.getcwd(), APP_NAME)
            backup_path = f"{current_path}.old"
            update_path = os.path.join(os.getcwd(), "update_temp.exe")

            # Check if the backup file exists and delete it
            if os.path.exists(backup_path):
                os.remove(backup_path)

            # Rename current executable to backup
            if os.path.exists(current_path):
                os.rename(current_path, backup_path)

            # Rename the new file to the current executable name
            os.rename(update_path, current_path)
            messagebox.showinfo("Update Complete", "The program has been updated successfully!")
            self.restart_program()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to replace the executable: {e}")

    def restart_program(self):
        os.execv(sys.executable, [sys.executable] + sys.argv)

if __name__ == "__main__":
    root = tk.Tk()
    app = UpdaterApp(root)
    root.mainloop()


# ---------------------------------------------------------------------------------------------------------------------------------------------------


# with system tray 
import os
import sys
import requests
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
from plyer import notification

CURRENT_VERSION = "1.1.0"
VERSION_URL = "https://raw.githubusercontent.com/bebedudu/autoupdate/refs/heads/main/latest_version.tx"
BASE_DOWNLOAD_URL = "https://github.com/bebedudu/autoupdate/releases/download"
APP_NAME = "Keylogger.exe"

if getattr(sys, 'frozen', False):  # Bundled as .exe
    app_dir = os.path.dirname(sys.executable)
else:  # Running as a script
    app_dir = os.path.dirname(os.path.abspath(__file__))

image_folders = os.path.join(app_dir, "image")
ICON_PATH = os.path.join(image_folders, "icon.ico")

def create_icon_image(size=64, color1="blue", color2="white"):
    image = Image.new("RGB", (size, size), color1)
    draw = ImageDraw.Draw(image)
    draw.ellipse((10, 10, size - 10, size - 10), fill=color2)
    return image

def show_notification(title, message):
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Keylogger",
            app_icon=ICON_PATH if os.path.exists(ICON_PATH) else None,
            timeout=3
        )
    except Exception as e:
        print(f"Notification Error: {e}")
        
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
        return f"{seconds / 60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds / 3600:.2f} hours"
    else:
        return f"{seconds / 86400:.2f} days"

def check_for_update_async():
    show_notification("Checking", "Checking for updates.....")
    threading.Thread(target=check_for_update, daemon=True).start()

def check_for_update():
    try:
        response = requests.get(VERSION_URL, timeout=10)
        response.raise_for_status()
        latest_version = response.text.strip()

        if latest_version > CURRENT_VERSION:
            # show_notification("Update Available", f"New version v{latest_version} is available.")
            if messagebox.askyesno("Update Available", f"A new version (v{latest_version}) is available. Update now?"):
                # Open the tkinter window and start downloading the update
                threading.Thread(target=lambda: run_tkinter_window(latest_version), daemon=True).start()

        else:
            show_notification("No Update", "You are using the latest version.")
            messagebox.showinfo("No Update", "You are using the latest version.")
    except requests.exceptions.RequestException as e:
        show_notification("Error", "Failed to check for updates. Please try again later.")
        messagebox.showerror("Error", f"Failed to check for updates: {e}")

def download_update(latest_version):  
        
    try:
        download_url = f"{BASE_DOWNLOAD_URL}/v{latest_version}/{APP_NAME}"
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
        messagebox.showerror("Error", f"Failed to download update: {e}")

def replace_executable():
    try:
        current_path = os.path.join(os.getcwd(), APP_NAME)
        backup_path = f"{current_path}.old"
        update_path = os.path.join(os.getcwd(), "update_temp.exe")

        if os.path.exists(backup_path):
            os.remove(backup_path)

        if os.path.exists(current_path):
            os.rename(current_path, backup_path)

        os.rename(update_path, current_path)
        messagebox.showinfo("Update Complete", "The program has been updated successfully!")
        restart_program()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to replace the executable: {e}")
        
def clean_partial_files():
    try:
        update_path = os.path.join(os.getcwd(), "update_temp.exe")
        if os.path.exists(update_path):
            os.remove(update_path)
    except Exception as e:
        print(f"Error during cleanup: {e}")


def restart_program():
    os.execv(sys.executable, [sys.executable] + sys.argv)

def quit_application(icon, item):
    icon.stop()

def run_tkinter_window(latest_version=None):
    
    global root, progress_label, progress_bar, time_label

    root = tk.Tk()
    root.title("Updater")
    root.geometry("400x250")

    progress_label = ttk.Label(root, text="Click 'Check for Updates' to start.")
    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)

    time_label = ttk.Label(root, text="", font=("Arial", 10))
    time_label.pack(pady=5)
    
    if latest_version:
        progress_label.config(text="Starting download...")
        threading.Thread(target=download_update, args=(latest_version,), daemon=True).start()
                         

    quit_button = ttk.Button(root, text="Quit", command=root.destroy)
    quit_button.pack(pady=5)

    root.mainloop()   
        
        
if __name__ == "__main__":
    clean_partial_files()
    check_for_update_async()
    # Create a system tray icon
    icon_image = create_icon_image()
    menu = Menu(
        MenuItem("Check for Updates", lambda icon, item: check_for_update_async()),
        MenuItem("Quit", quit_application)
    )
    tray_icon = Icon("Updater", icon_image, "Updater", menu)
    tray_icon.run()
