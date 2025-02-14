import os
import logging
from plyer import notification  # Assuming you're using the plyer library for notifications

# Set the icon path (update this with the actual path if needed)
ICON_PATH = "path/to/icon.ico"  # Modify this as needed

def show_notification(title, message, show=True):
    """
    Show a system notification based on the 'show' argument.
    """
    if not show:
        print("Notification suppressed.")
        return

    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Keylogger",
            app_icon=ICON_PATH if os.path.exists(ICON_PATH) else None,
            timeout=3
        )
    except Exception as e:
        logging.error(f"Notification Error: {e}")
        print(f"Notification Error: {e}")



show_notification("Test Title", "This is a test message.", show=True)  # This will show the notification.
show_notification("Test Title", "This is a test message.", show=False)  # This will not show the notification.
