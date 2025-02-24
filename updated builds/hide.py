import os
import ctypes

def hide_folder(path):
    # Check if the path exists
    if not os.path.exists(path):
        print(f"The path {path} does not exist.")
        return
    
    # Use ctypes to set the file attribute to hidden
    try:
        # FILE_ATTRIBUTE_HIDDEN = 0x2
        ctypes.windll.kernel32.SetFileAttributesW(path, 0x2)
        print(f"Folder '{path}' has been hidden successfully.")
    except Exception as e:
        print(f"Failed to hide folder: {e}")

# Path to the folder you want to hide
folder_path = r"C:\user feedback"
# Call the function to hide the folder
hide_folder(folder_path)