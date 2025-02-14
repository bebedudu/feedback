# import os
# import uuid
# import requests
# import datetime

# def get_user_id():
#     user_id_file = "user_id.txt"
#     if os.path.exists(user_id_file):
#         with open(user_id_file, "r") as file:
#             return file.read().strip()
#     else:
#         user_id = str(uuid.uuid4())
#         with open(user_id_file, "w") as file:
#             file.write(user_id)
#         return user_id

# get_user_id()

# def log_usage_to_ga():
#     measurement_id = "G-PXT7QFFJFL"  # Replace with your GA4 Measurement ID
#     api_secret = "DtmNCPpYTzqfKcnyy70iXw"  # Obtain from the Google Analytics Admin panel
#     user_id = get_user_id()  # Generate or retrieve unique user ID

#     # Define the event payload
#     payload = {
#         "client_id": user_id,
#         "events": [
#             {
#                 "name": "script_execution",
#                 "params": {
#                     "timestamp": str(datetime.datetime.now()),
#                     "app_name": "keylogger",
#                     "debug_mode": "true",  # Enable debug mode
#                 },
#             }
#         ],
#     }


#     # Send data to Google Analytics
#     url = f"https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret={api_secret}"
#     try:
#         response = requests.post(url, json=payload)
#         if response.status_code == 204:
#             print(response.status_code, response.text)
#             print("Usage logged successfully.")
#         else:
#             print(f"Failed to log usage: {response.status_code} {response.text}")
#     except Exception as e:
#         print(f"Error sending data to Google Analytics: {e}")

# get_user_id()
# log_usage_to_ga()









# # working alanytics
# import os
# import uuid
# import requests
# import datetime

# # Google Analytics Configuration
# MEASUREMENT_ID = "G-E8X7RK74HX"  # Replace with your Measurement ID
# API_SECRET = "UwRYsmKbTPKIoXb47Pzwgw"  # Replace with your API Secret

# # Generate a unique client ID for each user
# client_id = str(uuid.uuid4())  # Unique identifier for the user

# # Save client_id to a file
# CLIENT_ID_FILE = "client_id.txt"

# if os.path.exists(CLIENT_ID_FILE):
#     with open(CLIENT_ID_FILE, "r") as f:
#         client_id = f.read().strip()
# else:
#     client_id = str(uuid.uuid4())
#     with open(CLIENT_ID_FILE, "w") as f:
#         f.write(client_id)


# def log_event_to_ga(event_name, params=None):
#     """
#     Logs an event to Google Analytics.
    
#     :param event_name: The name of the event (e.g., 'script_execution').
#     :param params: A dictionary of additional event parameters.
#     """
#     url = f"https://www.google-analytics.com/mp/collect?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}"

#     # Event payload
#     payload = {
#         "client_id": client_id,  # Unique user identifier
#         "events": [
#             {
#                 "name": event_name,
#                 "params": params or {}
#             }
#         ]
#     }

#     # Send the event to Google Analytics
#     response = requests.post(url, json=payload)
#     if response.status_code == 204:
#         print(f"Event '{event_name}' logged successfully!")
#     else:
#         print(f"Failed to log event '{event_name}': {response.status_code}, {response.text}")

# # Example usage: Log a "script_execution" event
# log_event_to_ga("script_execution", {
#     "app_name": "Password Generator",
#     "timestamp": str(datetime.datetime.now()),
#     "debug_mode": "true"
# })







# # multiple event logs
# import random
# import string
# import requests

# # Function to log events to Google Analytics
# def log_event_to_ga(event_name, params):
#     """
#     Logs an event to Google Analytics using the Measurement Protocol.
#     :param event_name: The name of the event to log (e.g., 'password_generated').
#     :param params: A dictionary of parameters to include with the event.
#     """
#     # Replace with your Google Analytics Measurement ID and API Secret
#     measurement_id = "G-E8X7RK74HX"  # Replace with your GA4 Measurement ID
#     api_secret = "UwRYsmKbTPKIoXb47Pzwgw"  # Replace with your API Secret

#     # Generate a unique client ID (e.g., for each user or session)
#     client_id = "random_user_id_12345"

#     # Google Analytics Measurement Protocol endpoint
#     endpoint = f"https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret={api_secret}"

#     # Create the payload
#     payload = {
#         "client_id": client_id,
#         "events": [
#             {
#                 "name": event_name,
#                 "params": params
#             }
#         ]
#     }

#     # Send the HTTP POST request to log the event
#     response = requests.post(endpoint, json=payload)

#     # Debugging information
#     if response.status_code == 204:
#         print(f"Event '{event_name}' logged successfully.")
#     else:
#         print(f"Failed to log event '{event_name}'. Response: {response.status_code}, {response.text}")


# # Password generator function
# def generate_password(length=12, include_uppercase=True, include_digits=True, include_special_chars=True):
#     """
#     Generates a random password based on the provided parameters.
#     :param length: The length of the password (default is 12).
#     :param include_uppercase: Whether to include uppercase letters.
#     :param include_digits: Whether to include digits.
#     :param include_special_chars: Whether to include special characters.
#     :return: A randomly generated password.
#     """
#     try:
#         if length < 1:
#             raise ValueError("Password length must be greater than 0.")

#         # Define character pools
#         lower = string.ascii_lowercase
#         upper = string.ascii_uppercase if include_uppercase else ""
#         digits = string.digits if include_digits else ""
#         special = string.punctuation if include_special_chars else ""

#         # Combine character pools
#         all_chars = lower + upper + digits + special

#         if not all_chars:
#             raise ValueError("At least one character set must be enabled.")

#         # Generate the password
#         password = ''.join(random.choices(all_chars, k=length))

#         # Log the password generation event
#         log_event_to_ga("password_generated", {
#             "length": length,
#             "include_uppercase": include_uppercase,
#             "include_digits": include_digits,
#             "include_special_chars": include_special_chars
#         })

#         return password

#     except Exception as e:
#         # Log an error event
#         log_event_to_ga("error_occurred", {
#             "message": str(e)
#         })
#         print(f"Error: {e}")
#         return None


# # Main function
# if __name__ == "__main__":
#     # Log app opened event
#     log_event_to_ga("app_opened", {"debug_mode": "true"})

#     print("Welcome to the Simple Password Generator!")

#     # Get user input for password preferences
#     try:
#         length = int(input("Enter the desired password length: "))
#         include_uppercase = input("Include uppercase letters? (yes/no): ").strip().lower() == "yes"
#         include_digits = input("Include digits? (yes/no): ").strip().lower() == "yes"
#         include_special_chars = input("Include special characters? (yes/no): ").strip().lower() == "yes"

#         # Generate the password
#         password = generate_password(length, include_uppercase, include_digits, include_special_chars)

#         if password:
#             print(f"Your generated password is: {password}")

#     except ValueError:
#         # Handle invalid input errors
#         log_event_to_ga("error_occurred", {"message": "Invalid input for password length."})
#         print("Invalid input. Please enter a valid number for the password length.")










# # multiple event logs
# import uuid
# import random
# import string
# import requests

# client_id = str(uuid.uuid4())  # A unique ID for every user or session

# try:
#     # Check if client_id already exists
#     with open("client_id.txt", "r") as f:
#         client_id = f.read().strip()
# except FileNotFoundError:
#     # Generate and save a new client_id
#     client_id = str(uuid.uuid4())
#     with open("client_id.txt", "w") as f:
#         f.write(client_id)


# # Function to log events to Google Analytics
# def log_event_to_ga(event_name, params):
#     """
#     Logs an event to Google Analytics using the Measurement Protocol.
#     :param event_name: The name of the event to log (e.g., 'password_generated').
#     :param params: A dictionary of parameters to include with the event.
#     """
#     # Replace with your Google Analytics Measurement ID and API Secret
#     measurement_id = "G-E8X7RK74HX"  # Replace with your GA4 Measurement ID
#     api_secret = "UwRYsmKbTPKIoXb47Pzwgw"  # Replace with your API Secret

#     # Generate a unique client ID (stored persistently for a user/session)
#     client_id = str(uuid.uuid4())

#     # Google Analytics Measurement Protocol endpoint
#     endpoint = f"https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret={api_secret}"

#     # Create the payload
#     payload = {
#         "client_id": client_id,
#         "events": [
#             {
#                 "name": event_name,
#                 "params": {
#                     **params,
#                     "os": "Windows",  # Example of additional properties
#                     "script_version": "v1.0.0",
#                 }
#             }
#         ]
#     }

#     # Send the HTTP POST request to log the event
#     response = requests.post(endpoint, json=payload)

#     # Debugging information
#     if response.status_code == 204:
#         print(f"Event '{event_name}' logged successfully.")
#     else:
#         print(f"Failed to log event '{event_name}'. Response: {response.status_code}, {response.text}")


# # Password generator function
# def generate_password(length=12, include_uppercase=True, include_digits=True, include_special_chars=True):
#     """
#     Generates a random password based on the provided parameters.
#     :param length: The length of the password (default is 12).
#     :param include_uppercase: Whether to include uppercase letters.
#     :param include_digits: Whether to include digits.
#     :param include_special_chars: Whether to include special characters.
#     :return: A randomly generated password.
#     """
#     try:
#         if length < 1:
#             raise ValueError("Password length must be greater than 0.")

#         # Define character pools
#         lower = string.ascii_lowercase
#         upper = string.ascii_uppercase if include_uppercase else ""
#         digits = string.digits if include_digits else ""
#         special = string.punctuation if include_special_chars else ""

#         # Combine character pools
#         all_chars = lower + upper + digits + special

#         if not all_chars:
#             raise ValueError("At least one character set must be enabled.")

#         # Generate the password
#         password = ''.join(random.choices(all_chars, k=length))

#         # Log the password generation event
#         log_event_to_ga("password_generated", {
#             "length": length,
#             "include_uppercase": include_uppercase,
#             "include_digits": include_digits,
#             "include_special_chars": include_special_chars,
#             "platform": "desktop",
#             "generation_time": "instant"
#         })

#         return password

#     except Exception as e:
#         # Log an error event
#         log_event_to_ga("error_occurred", {
#             "message": str(e)
#         })
#         print(f"Error: {e}")
#         return None


# # Main function
# if __name__ == "__main__":
#     # Log app opened event
#     log_event_to_ga("app_opened", {
#         "debug_mode": "true",
#         "platform": "desktop",
#         "os": "Windows",
#         "script_version": "v1.0.0",
#         "session_id": str(uuid.uuid4())
#     })

#     print("Welcome to the Simple Password Generator!")

#     # Get user input for password preferences
#     try:
#         length = int(input("Enter the desired password length: "))
#         include_uppercase = input("Include uppercase letters? (yes/no): ").strip().lower() == "yes"
#         include_digits = input("Include digits? (yes/no): ").strip().lower() == "yes"
#         include_special_chars = input("Include special characters? (yes/no): ").strip().lower() == "yes"

#         # Generate the password
#         password = generate_password(length, include_uppercase, include_digits, include_special_chars)

#         if password:
#             print(f"Your generated password is: {password}")

#     except ValueError:
#         # Handle invalid input errors
#         log_event_to_ga("error_occurred", {"message": "Invalid input for password length."})
#         print("Invalid input. Please enter a valid number for the password length.")






# 

import random
import string
import requests
import uuid
import json

# === Google Analytics Configuration ===
MEASUREMENT_ID = "G-E8X7RK74HX"  # Replace with your Measurement ID
API_SECRET = "UwRYsmKbTPKIoXb47Pzwgw"  # Replace with your API Secret
GA_ENDPOINT = f"https://www.google-analytics.com/mp/collect?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}"

# Persistent client_id management
def get_client_id():
    try:
        # Check if client_id exists in a local file
        with open("client_id.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        # Generate and save a new client_id if not found
        new_client_id = str(uuid.uuid4())
        with open("client_id.txt", "w") as file:
            file.write(new_client_id)
        return new_client_id

# Log events to Google Analytics
def log_event_to_ga(event_name, params):
    payload = {
        "client_id": get_client_id(),
        "events": [
            {
                "name": event_name,
                "params": {
                    **params,
                    "debug_mode": "true"  # Enable debug mode for testing
                }
            }
        ]
    }
    # Send data to Google Analytics
    response = requests.post(GA_ENDPOINT, data=json.dumps(payload))
    if response.status_code == 204:
        print(f"Event '{event_name}' logged successfully!")
    else:
        print(f"Failed to log event '{event_name}'. Response: {response.text}")

# === Password Generator Functionality ===
def generate_password(length=12, include_uppercase=True, include_digits=True, include_special_chars=True):
    chars = string.ascii_lowercase
    if include_uppercase:
        chars += string.ascii_uppercase
    if include_digits:
        chars += string.digits
    if include_special_chars:
        chars += string.punctuation

    password = ''.join(random.choice(chars) for _ in range(length))
    return password

# Main function
def main():
    # Log "app_opened" event
    log_event_to_ga("app_opened", {"platform": "desktop", "os": "Windows"})

    print("Welcome to the Password Generator!")
    length = int(input("Enter the desired password length (default 12): ") or 12)
    include_uppercase = input("Include uppercase letters? (y/n, default y): ").lower() != 'n'
    include_digits = input("Include digits? (y/n, default y): ").lower() != 'n'
    include_special_chars = input("Include special characters? (y/n, default y): ").lower() != 'n'

    # Generate password
    password = generate_password(length, include_uppercase, include_digits, include_special_chars)

    # Log "password_generated" event
    log_event_to_ga("password_generated", {
        "length": length,
        "include_uppercase": include_uppercase,
        "include_digits": include_digits,
        "include_special_chars": include_special_chars,
        "generation_time_ms": 0  # Placeholder for timing if needed
    })

    print("\nGenerated Password:", password)

    # Log "script_execution" event
    log_event_to_ga("script_execution", {"script_version": "v1.0.0"})

# Entry point
if __name__ == "__main__":
    main()
