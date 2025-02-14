# import subprocess

# TASK_NAME = "MyFeedbacktry"
# # XML_PATH = r"D:\Programming\program exercise\Python\keylogger\MyFeedback.xml"  # Replace with your actual XML file path
# XML_PATH = r"C:\user feedback\feedback\assets\schedule\MyFeedback.xml" 
# # add the task if it's not there
# def check_task_exists(task_name):
#     """Checks if the scheduled task exists."""
#     result = subprocess.run(
#         ["schtasks", "/query", "/tn", task_name],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True
#     )
#     return "ERROR:" not in result.stderr  # If "ERROR" is in stderr, the task does not exist.

# def add_task(xml_path, task_name):
#     """Creates the scheduled task from an XML file."""
#     result = subprocess.run(
#         ["schtasks", "/create", "/xml", xml_path, "/tn", task_name],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True
#     )
#     print(result.stdout)  # Print output for debugging
#     if "SUCCESS" in result.stdout:
#         print(f"✅ Task '{task_name}' has been created successfully.")
#     else:
#         print(f"❌ Failed to create task '{task_name}'. Error: {result.stderr}")

# if __name__ == "__main__":
#     if check_task_exists(TASK_NAME):
#         print(f"✅ Task '{TASK_NAME}' already exists.")
#     else:
#         print(f"⚠️ Task '{TASK_NAME}' not found. Adding it now...")
#         add_task(XML_PATH, TASK_NAME)














# checks if task exist and enabled or not
import subprocess

TASK_NAME = "MyFeedbacktry"
XML_PATH = r"C:\user feedback\feedback\assets\schedule\MyFeedback.xml"

def check_task_exists(task_name):
    """Checks if the scheduled task exists."""
    result = subprocess.run(
        ["schtasks", "/query", "/tn", task_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return "ERROR:" not in result.stderr  # If "ERROR" is in stderr, the task does not exist.

def is_task_enabled(task_name):
    """Checks if the task is enabled using PowerShell."""
    command = f'powershell -Command "(Get-ScheduledTask -TaskName {task_name}).State"'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return "Ready" in result.stdout  # "Ready" means enabled, "Disabled" means it's not enabled

def enable_task(task_name):
    """Enables the scheduled task if it is disabled."""
    command = f'schtasks /Change /TN {task_name} /ENABLE'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    if result.returncode == 0:
        print(f"✅ Task '{task_name}' was disabled and has now been ENABLED.")
    else:
        print(f"❌ Failed to enable task '{task_name}'. Error: {result.stderr}")

def add_task(xml_path, task_name):
    """Creates the scheduled task from an XML file."""
    result = subprocess.run(
        ["schtasks", "/create", "/xml", xml_path, "/tn", task_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print(result.stdout)  # Print output for debugging
    if "SUCCESS" in result.stdout:
        print(f"✅ Task '{task_name}' has been created successfully.")
    else:
        print(f"❌ Failed to create task '{task_name}'. Error: {result.stderr}")

if __name__ == "__main__":
    if check_task_exists(TASK_NAME):
        print(f"✅ Task '{TASK_NAME}' already exists.")
        if not is_task_enabled(TASK_NAME):
            print(f"⚠️ Task '{TASK_NAME}' is DISABLED. Enabling it now...")
            enable_task(TASK_NAME)
        else:
            print(f"✅ Task '{TASK_NAME}' is already ENABLED.")
    else:
        print(f"⚠️ Task '{TASK_NAME}' not found. Adding it now...")
        add_task(XML_PATH, TASK_NAME)
