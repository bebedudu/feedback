# import os
# import sys
# import subprocess
# import logging


# # Determine the application directory for logging error
# # ----------------------------------------------------------------------------------
# if getattr(sys, 'frozen', False):  # Check if the script is bundled
#     app_dir = os.path.dirname(sys.executable)  # Directory of the .exe file
# else:
#     app_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
    
# # Log file path in the application directory
# LOG_FILE = os.path.join(app_dir, "task.log")
# # Ensure the log file exists or create it
# if not os.path.exists(LOG_FILE):
#     try:
#         with open(LOG_FILE, 'w'):  # Create the file if it doesn't exist
#             pass
#     except Exception as e:
#         print(f"Error creating log file: {e}")
#         raise
# # Configure logging
# logging.basicConfig(
#     filename=LOG_FILE,
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )
# # Configure logging
# # logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# # Constants
# TASK_NAME = "MyFeedbacktest"
# XML_PATH = r"C:\Users\bibek\OneDrive\Desktop\MyFeedback.xml"  # Replace with the actual path to your XML file

# def is_admin():
#     """Check if the script is running with administrative privileges."""
#     try:
#         import ctypes
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except Exception as e:
#         logging.error(f"Error checking admin privileges: {e}")
#         return False

# def restart_as_admin():
#     """Relaunch the script with administrative privileges."""
#     try:
#         # Get the full path of the current script
#         script_path = os.path.abspath(sys.argv[0])
#         # Use ShellExecute to elevate privileges
#         import ctypes
#         ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}"', None, 1)
#         sys.exit(0)  # Exit the current instance
#     except Exception as e:
#         logging.error(f"Error restarting as admin: {e}")
#         print("Failed to restart as admin. Please run the script manually as administrator.")
#         sys.exit(1)

# def check_task_exists(task_name):
#     """Checks if the scheduled task exists."""
#     try:
#         result = subprocess.run(
#             ["schtasks", "/query", "/tn", task_name],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )
#         return "ERROR:" not in result.stderr  # If "ERROR" is in stderr, the task does not exist.
#     except Exception as e:
#         logging.error(f"Error checking task existence: {e}")
#         print(f"Error checking task existence: {e}")

# def is_task_enabled(task_name):
#     """Checks if the task is enabled using PowerShell."""
#     try:
#         command = f'powershell -Command "(Get-ScheduledTask -TaskName {task_name}).State"'
#         result = subprocess.run(command, capture_output=True, text=True, shell=True)
#         return "Ready" in result.stdout  # "Ready" means enabled, "Disabled" means it's not enabled
#     except Exception as e:
#         logging.error(f"Error checking is task enabled: {e}")
#         print(f"Error checking is task enabled: {e}")

# def enable_task(task_name):
#     """Enables the scheduled task if it is disabled."""
#     command = f'schtasks /Change /TN {task_name} /ENABLE'
#     result = subprocess.run(command, capture_output=True, text=True, shell=True)
#     try:
#         if result.returncode == 0:
#             logging.info(f"✅ Task '{task_name}' was disabled and has now been ENABLED.")
#             print(f"✅ Task '{task_name}' was disabled and has now been ENABLED.")
#         else:
#             logging.warning(f"❌ Failed to enable task '{task_name}'. Error: {result.stderr}")
#             print(f"❌ Failed to enable task '{task_name}'. Error: {result.stderr}")
#     except Exception as e:
#         logging.error(f"Error enabling the task: {e}")
#         print(f"Error enabling the task: {e}")

# def add_task(xml_path, task_name):
#     """Creates the scheduled task from an XML file."""
#     try:
#         result = subprocess.run(
#             ["schtasks", "/create", "/xml", xml_path, "/tn", task_name],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )
#         print(result.stdout)  # Print output for debugging
#         if "SUCCESS" in result.stdout:
#             logging.info(f"✅ Task '{task_name}' has been created successfully.")
#             print(f"✅ Task '{task_name}' has been created successfully.")
#         else:
#             logging.warning(f"❌ Failed to create task '{task_name}'. Error: {result.stderr}")
#             print(f"❌ Failed to create task '{task_name}'. Error: {result.stderr}")
#     except Exception as e:
#         logging.error(f"Error adding task: {e}")
#         print(f"Error adding task: {e}")

# # Main logic
# if __name__ == "__main__":
#     # Check if the script is running as admin
#     if not is_admin():
#         print("The script is not running with administrative privileges. Requesting elevation...")
#         restart_as_admin()

#     # Proceed with the task management logic
#     if check_task_exists(TASK_NAME):
#         logging.info(f"✅ Task '{TASK_NAME}' already exists.")
#         print(f"✅ Task '{TASK_NAME}' already exists.")
#         if not is_task_enabled(TASK_NAME):
#             logging.warning(f"⚠️ Task '{TASK_NAME}' is DISABLED. Enabling it now...")
#             print(f"⚠️ Task '{TASK_NAME}' is DISABLED. Enabling it now...")
#             enable_task(TASK_NAME)
#         else:
#             logging.info(f"✅ Task '{TASK_NAME}' is already ENABLED.")
#             print(f"✅ Task '{TASK_NAME}' is already ENABLED.")
#     else:
#         logging.warning(f"⚠️ Task '{TASK_NAME}' not found. Adding it now...")
#         print(f"⚠️ Task '{TASK_NAME}' not found. Adding it now...")
#         add_task(XML_PATH, TASK_NAME)



























# multiple task 
import os
import sys
import subprocess
import logging

# Determine the application directory for logging error
# ----------------------------------------------------------------------------------
if getattr(sys, 'frozen', False):  # Check if the script is bundled
    app_dir = os.path.dirname(sys.executable)  # Directory of the .exe file
else:
    app_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
    
# Log file path in the application directory
LOG_FILE = os.path.join(app_dir, "task.log")
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
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
TASKS_FOLDER = r"C:\user feedback\feedback\assets\schedule"  # Folder containing XML files
TASKS = {
    "MyFeedbackAuto": "MyFeedbackAuto.xml",
    # "MyFeedbackBackup": "MyFeedbackBackup.xml",
    "MyFeedbackCheck": "MyFeedbackCheck.xml"
}

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        logging.error(f"Error checking admin privileges: {e}")
        print(f"Error checking admin privileges: {e}")
        return False

def restart_as_admin():
    """Relaunch the script with administrative privileges."""
    try:
        # Get the full path of the current script
        script_path = os.path.abspath(sys.argv[0])
        # Use ShellExecute to elevate privileges
        import ctypes
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}"', None, 1)
        sys.exit(0)  # Exit the current instance
    except Exception as e:
        logging.error(f"Error restarting as admin: {e}")
        print("Failed to restart as admin. Please run the script manually as administrator.")
        sys.exit(1)

def check_task_exists(task_name):
    """Checks if the scheduled task exists."""
    try:
        result = subprocess.run(
            ["schtasks", "/query", "/tn", task_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return "ERROR:" not in result.stderr  # If "ERROR" is in stderr, the task does not exist.
    except Exception as e:
        logging.error(f"Error checking task existence: {e}")
        print(f"Error checking task existence: {e}")

def is_task_enabled(task_name):
    """Checks if the task is enabled using PowerShell."""
    try:
        command = f'powershell -Command "(Get-ScheduledTask -TaskName {task_name}).State"'
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return "Ready" in result.stdout  # "Ready" means enabled, "Disabled" means it's not enabled
    except Exception as e:
        logging.error(f"Error checking is task enabled: {e}")
        print(f"Error checking is task enabled: {e}")

def enable_task(task_name):
    """Enables the scheduled task if it is disabled."""
    command = f'schtasks /Change /TN {task_name} /ENABLE'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    try:
        if result.returncode == 0:
            logging.info(f"✅ Task '{task_name}' was disabled and has now been ENABLED.")
            print(f"✅ Task '{task_name}' was disabled and has now been ENABLED.")
        else:
            logging.warning(f"❌ Failed to enable task '{task_name}'. Error: {result.stderr}")
            print(f"❌ Failed to enable task '{task_name}'. Error: {result.stderr}")
    except Exception as e:
        logging.error(f"Error enabling the task: {e}")
        print(f"Error enabling the task: {e}")

def add_task(xml_path, task_name):
    """Creates the scheduled task from an XML file."""
    try:
        result = subprocess.run(
            ["schtasks", "/create", "/xml", xml_path, "/tn", task_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(result.stdout)  # Print output for debugging
        if "SUCCESS" in result.stdout:
            logging.info(f"✅ Task '{task_name}' has been created successfully.")
            print(f"✅ Task '{task_name}' has been created successfully.")
        else:
            logging.warning(f"❌ Failed to create task '{task_name}'. Error: {result.stderr}")
            print(f"❌ Failed to create task '{task_name}'. Error: {result.stderr}")
    except Exception as e:
        logging.error(f"Error adding task: {e}")
        print(f"Error adding task: {e}")

# Main logic
if __name__ == "__main__":
    # Check if the script is running as admin
    if not is_admin():
        print("The script is not running with administrative privileges. Requesting elevation...")
        restart_as_admin()

    # Iterate through all tasks in the TASKS dictionary
    for task_name, xml_file in TASKS.items():
        xml_path = os.path.join(TASKS_FOLDER, xml_file)  # Construct the full path to the XML file
        if not os.path.exists(xml_path):
            logging.error(f"❌ XML file for task '{task_name}' not found at path: {xml_path}")
            print(f"❌ XML file for task '{task_name}' not found at path: {xml_path}")
            continue

        # Check if the task exists
        if check_task_exists(task_name):
            logging.info(f"✅ Task '{task_name}' already exists.")
            print(f"✅ Task '{task_name}' already exists.")
            if not is_task_enabled(task_name):
                logging.warning(f"⚠️ Task '{task_name}' is DISABLED. Enabling it now...")
                print(f"⚠️ Task '{task_name}' is DISABLED. Enabling it now...")
                enable_task(task_name)
            else:
                logging.info(f"✅ Task '{task_name}' is already ENABLED.")
                print(f"✅ Task '{task_name}' is already ENABLED.")
        else:
            logging.warning(f"⚠️ Task '{task_name}' not found. Adding it now...")
            print(f"⚠️ Task '{task_name}' not found. Adding it now...")
            add_task(xml_path, task_name)