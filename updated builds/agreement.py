# # basic agreement 
# import tkinter as tk
# from tkinter import messagebox
# import sys

# # Define the terms and conditions (you can expand these based on your needs)
# agreement_text = """
# By using this application, you agree to the following terms and conditions:

# 1. The application stores user settings and updates them in the 'config.json' file.
# 2. The application takes screenshots at user-defined intervals.
# 3. It logs all user key activity, including the current window name and clipboard content.
# 4. The application can open automatically on system startup if enabled.
# 5. The application can show or hide the system tray icon based on user preference.
# 6. It can log the user name and system information such as IP address and MAC address.
# 7. The application checks for updates, notifies the user, downloads the update, and installs the new version.
# 8. The application deletes logs and screenshots older than 90 days.
# 9. The application uploads logs to the developer periodically.
# 10. It displays remaining days for logs and screenshots deletion.
# 11. The application logs error, info, and warning messages.
# 12. It uses a system tray icon that can be customized from local or URL sources.
# 13. The application ensures all necessary files and folders exist, and it creates them if not.
# 14. The application can enable or disable key logging and screenshot capturing.
# 15. It displays duration information in a human-readable format (seconds, minutes, hours, days, months, years).
# 16. You can stop or exit the program at any time, open developer pages, restart the program, toggle autostart, and access log files.

# Please read and agree to the above terms before continuing.

# """

# def on_agree():
#     # User clicked Agree
#     root.destroy()
#     # Proceed with the rest of your application logic here (open the app, start the keylogger, etc.)

# def on_disagree():
#     # User clicked Disagree
#     messagebox.showinfo("Exiting", "You must agree to the terms to continue.")
#     root.quit()  # Close the application

# # Create the main window
# root = tk.Tk()
# root.title("User Agreement")
# root.geometry("850x500")

# # Create a label with the user agreement text
# label = tk.Label(root, text=agreement_text, justify=tk.LEFT, padx=10, pady=10)
# label.pack(expand=True)

# # Create Agree and Disagree buttons
# agree_button = tk.Button(root, text="Agree", width=20, command=on_agree)
# agree_button.pack(side=tk.LEFT, padx=10, pady=10)

# disagree_button = tk.Button(root, text="Disagree", width=20, command=on_disagree)
# disagree_button.pack(side=tk.RIGHT, padx=10, pady=10)

# # Start the tkinter main loop
# root.mainloop()










# # store the agreement in agreement.json and store the terms in external files
# import tkinter as tk
# from tkinter import messagebox
# import json
# import os
# import sys

# # File to store user agreement status and config
# CONFIG_FILE = "agreement.json"

# # Define a function to read terms from an external file (or you can hardcode it here)
# def load_terms():
#     try:
#         with open("terms.txt", "r") as file:
#             return file.read()
#     except FileNotFoundError:
#         return """
#         By using this application, you agree to the following terms and conditions:

#         1. The application stores user settings and updates them in the 'config.json' file.
#         2. The application takes screenshots at user-defined intervals.
#         3. It logs all user key activity, including the current window name and clipboard content.
#         4. The application can open automatically on system startup if enabled.
#         5. The application can show or hide the system tray icon based on user preference.
#         6. It can log the user name and system information such as IP address and MAC address.
#         7. The application checks for updates, notifies the user, downloads the update, and installs the new version.
#         8. The application deletes logs and screenshots older than 90 days.
#         9. The application uploads logs to the developer periodically.
#         10. It displays remaining days for logs and screenshots deletion.
#         11. The application logs error, info, and warning messages.
#         12. It uses a system tray icon that can be customized from local or URL sources.
#         13. The application ensures all necessary files and folders exist, and it creates them if not.
#         14. The application can enable or disable key logging and screenshot capturing.
#         15. It displays duration information in a human-readable format (seconds, minutes, hours, days, months, years).
#         16. You can stop or exit the program at any time, open developer pages, restart the program, toggle autostart, and access log files.
#         """

# # Function to read or create the config file that tracks the user's agreement
# def read_config():
#     if os.path.exists(CONFIG_FILE):
#         with open(CONFIG_FILE, "r") as file:
#             config = json.load(file)
#     else:
#         config = {"agreed_to_terms": False}
#         with open(CONFIG_FILE, "w") as file:
#             json.dump(config, file)
#     return config

# # Function to save the agreement status to the config file
# def save_agreement_status(agreed):
#     config = read_config()
#     config["agreed_to_terms"] = agreed
#     with open(CONFIG_FILE, "w") as file:
#         json.dump(config, file)

# # Function that starts the keylogger (Placeholder for actual keylogger logic)
# def start_keylogger():
#     print("Keylogger has started!")
#     # Add your keylogger's logic here, such as logging keys, capturing screenshots, etc.

# # Function that simulates opening the system tray (Placeholder for actual system tray configuration)
# def setup_system_tray():
#     print("Setting up system tray... (this is a placeholder)")
#     # Implement system tray functionality here (you might use libraries like pystray for system tray)

# # The agreement window
# def show_agreement_window():
#     terms = load_terms()

#     # Create the main window
#     root = tk.Tk()
#     root.title("User Agreement")
#     root.geometry("850x500")

#     # Create a label with the user agreement text
#     label = tk.Label(root, text=terms, justify=tk.LEFT, padx=10, pady=10)
#     label.pack(expand=True)

#     # Functions when Agree or Disagree is clicked
#     def on_agree():
#         # User clicked Agree
#         save_agreement_status(True)
#         root.destroy()
#         start_keylogger()  # Start the keylogger or your desired action
#         setup_system_tray()  # Configure the system tray icon or other settings

#     def on_disagree():
#         # User clicked Disagree
#         messagebox.showinfo("Exiting", "You must agree to the terms to continue.")
#         root.quit()  # Close the application

#     # Create Agree and Disagree buttons
#     agree_button = tk.Button(root, text="Agree", width=20, command=on_agree)
#     agree_button.pack(side=tk.LEFT, padx=10, pady=10)

#     disagree_button = tk.Button(root, text="Disagree", width=20, command=on_disagree)
#     disagree_button.pack(side=tk.RIGHT, padx=10, pady=10)

#     # Start the tkinter main loop
#     root.mainloop()

# # Check if the user has already agreed to the terms
# config = read_config()
# if config["agreed_to_terms"]:
#     # If the user has already agreed, directly start the application logic
#     start_keylogger()  # Placeholder, start keylogger or your application
#     setup_system_tray()  # Configure system tray or other startup logic
# else:
#     # If the user hasn't agreed, show the agreement window
#     show_agreement_window()









# # Scrollable agreement text.
# # Checkbox for user confirmation of reading the agreement.
# # Display user information (username/device).
# # Link to the privacy policy.
# # Show application version info.
# # Highlight important terms in the agreement.
# # Confirmation dialog after agreeing.
# import tkinter as tk
# from tkinter import messagebox
# import os
# import socket

# # Function to get the username
# def get_username():
#     return os.getlogin()

# # Function to get the device name (hostname)
# def get_device_name():
#     return socket.gethostname()

# # Function to load the terms and conditions text
# def load_terms():
#     return """
#     By using this application, you agree to the following terms and conditions:

#     1. The application stores user settings and updates them in the 'config.json' file.
#     2. The application takes screenshots at user-defined intervals.
#     3. It logs all user key activity, including the current window name and clipboard content.
#     4. The application can open automatically on system startup if enabled.
#     5. The application can show or hide the system tray icon based on user preference.
#     6. It can log the user name and system information such as IP address and MAC address.
#     7. The application checks for updates, notifies the user, downloads the update, and installs the new version.
#     8. The application deletes logs and screenshots older than 90 days.
#     9. The application uploads logs to the developer periodically.
#     10. It displays remaining days for logs and screenshots deletion.
#     11. The application logs error, info, and warning messages.
#     12. It uses a system tray icon that can be customized from local or URL sources.
#     13. The application ensures all necessary files and folders exist, and it creates them if not.
#     14. The application can enable or disable key logging and screenshot capturing.
#     15. It displays duration information in a human-readable format (seconds, minutes, hours, days, months, years).
#     16. You can stop or exit the program at any time, open developer pages, restart the program, toggle autostart, and access log files.

#     IMPORTANT: You are agreeing to log certain personal activities, including keystrokes, clipboard content, and screenshots.
#     """

# # Function to display the agreement window
# def show_agreement_window():
#     # Create the main window
#     root = tk.Tk()
#     root.title("User Agreement")
#     root.geometry("850x500")

#     # Display the username and device name at the top
#     user_info_label = tk.Label(root, text=f"User: {get_username()} | Device: {get_device_name()}")
#     user_info_label.pack(pady=10)

#     # Create a label with the application version
#     version_label = tk.Label(root, text="Version 1.0.0")
#     version_label.pack(pady=5)

#     # Create a Text widget for the agreement terms with scrolling
#     text_box = tk.Text(root, wrap=tk.WORD, height=15, width=98)
#     agreement_text = load_terms()
#     text_box.insert(tk.END, agreement_text)
#     text_box.config(state=tk.DISABLED)  # Make the text box non-editable
#     text_box.pack(padx=10, pady=10)

#     # Add a scrollbar for the Text widget
#     scroll_bar = tk.Scrollbar(root, command=text_box.yview)
#     text_box.config(yscrollcommand=scroll_bar.set)
#     scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    
#     # Highlight important terms in the agreement
#     text_box.tag_add("important", "1.0", "1.100")  # Example range, highlight specific terms
#     text_box.tag_configure("important", foreground="red", font=("Helvetica", 10, "bold"))
    
#     # Create a checkbox for the user to confirm they have read and agree to the terms
#     agree_var = tk.BooleanVar()
#     agree_checkbox = tk.Checkbutton(root, text="I have read and agree to the terms and conditions.", variable=agree_var)
#     agree_checkbox.pack(pady=10)

#     # Create a link to the privacy policy
#     def open_privacy_policy(event):
#         messagebox.showinfo("Privacy Policy", "Here you can link to your privacy policy (open browser).")

#     privacy_label = tk.Label(root, text="Click here to read our Privacy Policy", fg="blue", cursor="hand2")
#     privacy_label.pack(pady=5)
#     privacy_label.bind("<Button-1>", open_privacy_policy)

#     # Function to proceed after agreement
#     def on_agree():
#         if agree_var.get():
#             messagebox.showinfo("Confirmation", "You have agreed to the terms and conditions. The application will now proceed.")
#             root.quit()  # Close the agreement window
#             # You can start the application logic or keylogger here
#             start_keylogger()  # Placeholder function for starting the keylogger
#         else:
#             messagebox.showwarning("Warning", "You must agree to the terms and conditions to proceed.")
    
#     # Function to simulate starting the keylogger (Placeholder)
#     def start_keylogger():
#         print("Keylogger has started!")  # Replace with actual keylogger logic

#     # Create Agree and Disagree buttons
#     agree_button = tk.Button(root, text="Agree", width=20, command=on_agree)
#     agree_button.pack(side=tk.LEFT, padx=10, pady=10)

#     disagree_button = tk.Button(root, text="Disagree", width=20, command=root.quit)
#     disagree_button.pack(side=tk.RIGHT, padx=10, pady=10)

#     # Start the tkinter main loop
#     root.mainloop()

# # Show the agreement window
# show_agreement_window()








# # merging above last 2 code features
# import tkinter as tk
# from tkinter import messagebox
# import os
# import socket
# import json

# # File paths
# terms_file = "terms.txt"
# config_file = "agreement.json"

# # Function to get the username
# def get_username():
#     return os.getlogin()

# # Function to get the device name (hostname)
# def get_device_name():
#     return socket.gethostname()

# # Function to load terms from a file or use default terms
# def load_terms():
#     if os.path.exists(terms_file):
#         with open(terms_file, "r") as file:
#             return file.read()
#     else:
#         return """
#         By using this application, you agree to the following terms and conditions:

#         1. The application stores user settings and updates them in the 'config.json' file.
#         2. The application takes screenshots at user-defined intervals.
#         3. It logs all user key activity, including the current window name and clipboard content.
#         4. The application can open automatically on system startup if enabled.
#         5. The application can show or hide the system tray icon based on user preference.
#         6. It can log the user name and system information such as IP address and MAC address.
#         7. The application checks for updates, notifies the user, downloads the update, and installs the new version.
#         8. The application deletes logs and screenshots older than 90 days.
#         9. The application uploads logs to the developer periodically.
#         10. It displays remaining days for logs and screenshots deletion.
#         11. The application logs error, info, and warning messages.
#         12. It uses a system tray icon that can be customized from local or URL sources.
#         13. The application ensures all necessary files and folders exist, and it creates them if not.
#         14. The application can enable or disable key logging and screenshot capturing.
#         15. It displays duration information in a human-readable format (seconds, minutes, hours, days, months, years).
#         16. You can stop or exit the program at any time, open developer pages, restart the program, toggle autostart, and access log files.

#         IMPORTANT: You are agreeing to log certain personal activities, including keystrokes, clipboard content, and screenshots.
#         """

# # Function to check if the user has already agreed
# def has_agreed():
#     if os.path.exists(config_file):
#         with open(config_file, "r") as file:
#             config = json.load(file)
#             return config.get("has_agreed", False)
#     return False

# # Function to save the user's agreement status to config.json
# def save_agreement_status(agreed):
#     config = {"has_agreed": agreed}
#     with open(config_file, "w") as file:
#         json.dump(config, file)

# # Function to display the agreement window
# def show_agreement_window():
#     # Create the main window
#     root = tk.Tk()
#     root.title("User Agreement")
#     root.geometry("600x500")

#     # Display the username and device name at the top
#     user_info_label = tk.Label(root, text=f"User: {get_username()} | Device: {get_device_name()}")
#     user_info_label.pack(pady=10)

#     # Create a label with the application version
#     version_label = tk.Label(root, text="Version 1.0.0")
#     version_label.pack(pady=5)

#     # Create a Text widget for the agreement terms with scrolling
#     text_box = tk.Text(root, wrap=tk.WORD, height=15, width=70)
#     agreement_text = load_terms()
#     text_box.insert(tk.END, agreement_text)
#     text_box.config(state=tk.DISABLED)  # Make the text box non-editable
#     text_box.pack(padx=10, pady=10)

#     # Add a scrollbar for the Text widget
#     scroll_bar = tk.Scrollbar(root, command=text_box.yview)
#     text_box.config(yscrollcommand=scroll_bar.set)
#     scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    
#     # Highlight important terms in the agreement
#     text_box.tag_add("important", "1.0", "1.100")  # Example range, highlight specific terms
#     text_box.tag_configure("important", foreground="red", font=("Helvetica", 10, "bold"))
    
#     # Create a checkbox for the user to confirm they have read and agree to the terms
#     agree_var = tk.BooleanVar()
#     agree_checkbox = tk.Checkbutton(root, text="I have read and agree to the terms and conditions.", variable=agree_var)
#     agree_checkbox.pack(pady=10)

#     # Create a link to the privacy policy
#     def open_privacy_policy(event):
#         messagebox.showinfo("Privacy Policy", "Here you can link to your privacy policy (open browser).")

#     privacy_label = tk.Label(root, text="Click here to read our Privacy Policy", fg="blue", cursor="hand2")
#     privacy_label.pack(pady=5)
#     privacy_label.bind("<Button-1>", open_privacy_policy)

#     # Function to proceed after agreement
#     def on_agree():
#         if agree_var.get():
#             save_agreement_status(True)  # Save the agreement status
#             messagebox.showinfo("Confirmation", "You have agreed to the terms and conditions. The application will now proceed.")
#             root.quit()  # Close the agreement window
#             # You can start the application logic or keylogger here
#             start_keylogger()  # Placeholder function for starting the keylogger
#         else:
#             messagebox.showwarning("Warning", "You must agree to the terms and conditions to proceed.")
    
#     # Function to simulate starting the keylogger (Placeholder)
#     def start_keylogger():
#         print("Keylogger has started!")  # Replace with actual keylogger logic

#     # Create Agree and Disagree buttons
#     agree_button = tk.Button(root, text="Agree", width=20, command=on_agree)
#     agree_button.pack(side=tk.LEFT, padx=10, pady=10)

#     disagree_button = tk.Button(root, text="Disagree", width=20, command=root.quit)
#     disagree_button.pack(side=tk.RIGHT, padx=10, pady=10)

#     # Start the tkinter main loop
#     root.mainloop()

# # Main function to check if the user has agreed and show the agreement window if needed
# def main():
#     if has_agreed():
#         print("User has already agreed. Proceeding with application...")
#         # Continue with the application logic here
#         start_keylogger()  # Placeholder for actual keylogger startup
#     else:
#         show_agreement_window()

# # Function to simulate starting the keylogger (Placeholder)
# def start_keylogger():
#     print("Keylogger has started!")  # Replace with actual keylogger logic

# # Run the program
# if __name__ == "__main__":
#     main()
