# # show the active user
# import base64
# import json
# import requests
# from datetime import datetime

# # Configuration
# GITHUB_TOKEN = "add_your_token_here"  # Replace with your GitHub PAT
# REPO = "bebedudu/activeuser"  # Replace with your repo (username/repo)
# FILE_PATH = "activeuserinfo.txt"  # Path to the file in the repo
# BRANCH = "main"  # The branch to modify
# API_BASE_URL = "https://api.github.com"

# # Get active user information
# import os
# active_user = os.getlogin()
# timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# new_entry = f"{timestamp} - {active_user}\n"

# # Headers for authentication
# HEADERS = {
#     "Authorization": f"token {GITHUB_TOKEN}",
#     "Accept": "application/vnd.github.v3+json",
# }

# # Step 1: Get the current file content
# file_url = f"{API_BASE_URL}/repos/{REPO}/contents/{FILE_PATH}"

# response = requests.get(file_url, headers=HEADERS)
# if response.status_code == 200:
#     file_data = response.json()
#     current_content = base64.b64decode(file_data['content']).decode('utf-8')
#     sha = file_data['sha']  # File SHA for update operation
# else:
#     print(f"Failed to fetch file content: {response.status_code} - {response.json()}")
#     exit()

# # Step 2: Append new content
# updated_content = current_content + new_entry
# encoded_content = base64.b64encode(updated_content.encode('utf-8')).decode('utf-8')

# # Step 3: Update the file on GitHub
# update_payload = {
#     "message": f"Add active user {active_user}",
#     "content": encoded_content,
#     "sha": sha,  # File SHA to update
#     "branch": BRANCH,
# }

# response = requests.put(file_url, headers=HEADERS, data=json.dumps(update_payload))

# if response.status_code == 200:
#     print("File updated successfully!")
# else:
#     print(f"Failed to update file: {response.status_code} - {response.json()}")







# # continous active user
# import os
# import base64
# import json
# import requests
# from datetime import datetime
# import schedule
# import time

# # Configuration
# GITHUB_TOKEN = "add_your_token_here"  # Replace with your GitHub PAT
# REPO = "bebedudu/activeuser"  # Replace with your repo (username/repo)
# FILE_PATH = "activeuserinfo.txt"  # Path to the file in the repo
# BRANCH = "main"  # The branch to modify
# API_BASE_URL = "https://api.github.com"
# INTERVAL = 60  # Time interval in seconds to check and update

# # Headers for authentication
# HEADERS = {
#     "Authorization": f"token {GITHUB_TOKEN}",
#     "Accept": "application/vnd.github.v3+json",
# }

# def get_active_user():
#     """Get the active user and current timestamp."""
#     active_user = os.getlogin()
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     return f"{timestamp} - {active_user}\n"

# def update_active_user_file(new_entry):
#     """Update the active user file on GitHub."""
#     # Fetch the current file content
#     file_url = f"{API_BASE_URL}/repos/{REPO}/contents/{FILE_PATH}"
#     response = requests.get(file_url, headers=HEADERS)
#     if response.status_code == 200:
#         file_data = response.json()
#         current_content = base64.b64decode(file_data['content']).decode('utf-8')
#         sha = file_data['sha']
#     else:
#         print(f"Failed to fetch file content: {response.status_code} - {response.json()}")
#         return

#     # Append the new entry
#     updated_content = current_content + new_entry
#     encoded_content = base64.b64encode(updated_content.encode('utf-8')).decode('utf-8')

#     # Update the file on GitHub
#     update_payload = {
#         "message": f"Add active user log entry",
#         "content": encoded_content,
#         "sha": sha,  # File SHA to update
#         "branch": BRANCH,
#     }

#     response = requests.put(file_url, headers=HEADERS, data=json.dumps(update_payload))
#     if response.status_code == 200:
#         print("File updated successfully!")
#     else:
#         print(f"Failed to update file: {response.status_code} - {response.json()}")

# def main():
#     """Main function to repeatedly check and update active user."""
#     while True:
#         try:
#             new_entry = get_active_user()
#             update_active_user_file(new_entry)
#         except Exception as e:
#             print(f"An error occurred: {e}")
#         time.sleep(INTERVAL)  # Wait for the specified interval before the next update

# if __name__ == "__main__":
#     main()





# # loop active user with geolocation
# import os
# import base64
# import json
# import requests
# from datetime import datetime
# import time

# # GitHub Configuration
# GITHUB_TOKEN = "add_your_token_here"  # Replace with your GitHub PAT
# REPO = "bebedudu/activeuser"  # Replace with your repo (username/repo)
# FILE_PATH = "activeuserinfo.txt"  # Path to the file in the repo
# BRANCH = "main"  # The branch to modify
# API_BASE_URL = "https://api.github.com"
# INTERVAL = 60  # Time interval in seconds to check and update

# # Headers for GitHub API authentication
# HEADERS = {
#     "Authorization": f"token {GITHUB_TOKEN}",
#     "Accept": "application/vnd.github.v3+json",
# }

# def get_public_ip():
#     """Get the public IP address of the user."""
#     try:
#         response = requests.get('https://api64.ipify.org?format=json')
#         response.raise_for_status()
#         return response.json().get('ip')
#     except requests.RequestException as e:
#         print(f"Error fetching public IP: {e}")
#         return None

# def get_geolocation(ip_address):
#     """Get geolocation details for the given IP address."""
#     try:
#         api_url = f"https://ipinfo.io/{ip_address}?token=ccb3ba52662beb"  # Replace with your ipinfo token
#         response = requests.get(api_url)
#         response.raise_for_status()
#         data = response.json()

#         # Extract relevant details
#         country = data.get("country", "N/A")
#         region = data.get("region", "N/A")
#         city = data.get("city", "N/A")
#         org = data.get("org", "N/A")
#         loc = data.get("loc", "N/A")
#         postal = data.get("postal", "N/A")
#         timezone = data.get("timezone", "N/A")
#         return country, region, city, org, loc, postal, timezone
#     except requests.RequestException as e:
#         print(f"Error fetching geolocation: {e}")
#         return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

# def update_active_user_file(new_entry):
#     """Update the active user file on GitHub."""
#     # Fetch the current file content
#     file_url = f"{API_BASE_URL}/repos/{REPO}/contents/{FILE_PATH}"
#     response = requests.get(file_url, headers=HEADERS)
#     if response.status_code == 200:
#         file_data = response.json()
#         current_content = base64.b64decode(file_data['content']).decode('utf-8')
#         sha = file_data['sha']
#     else:
#         print(f"Failed to fetch file content: {response.status_code} - {response.json()}")
#         return

#     # Append the new entry
#     updated_content = current_content + new_entry
#     encoded_content = base64.b64encode(updated_content.encode('utf-8')).decode('utf-8')

#     # Update the file on GitHub
#     update_payload = {
#         "message": "Update active user log with geolocation",
#         "content": encoded_content,
#         "sha": sha,
#         "branch": BRANCH,
#     }

#     response = requests.put(file_url, headers=HEADERS, data=json.dumps(update_payload))
#     if response.status_code == 200:
#         print("File updated successfully!")
#     else:
#         print(f"Failed to update file: {response.status_code} - {response.json()}")

# def main():
#     """Main function to repeatedly log active user with geolocation."""
#     while True:
#         try:
#             # Get active user info
#             active_user = os.getlogin()
#             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#             # Get public IP and geolocation
#             user_ip = get_public_ip()
#             if user_ip:
#                 country, region, city, org, loc, postal, timezone = get_geolocation(user_ip)
#                 new_entry = (f"{timestamp} - User: {active_user}, IP: {user_ip}, "
#                              f"Location: {country}, {region}, {city}, Org: {org}, "
#                              f"Coordinates: {loc}, Postal: {postal}, TimeZone: {timezone}\n")
#             else:
#                 new_entry = f"{timestamp} - User: {active_user}, IP: N/A, Location: N/A\n"

#             # Update the file
#             update_active_user_file(new_entry)
#         except Exception as e:
#             print(f"An error occurred: {e}")
#         time.sleep(INTERVAL)  # Wait for the specified interval before the next update

# if __name__ == "__main__":
#     main()






# # store the system info with geoloaction
# import os
# import base64
# import json
# import requests
# from datetime import datetime
# import time
# import platform
# import psutil
# import socket
# import uuid

# # GitHub Configuration
# GITHUB_TOKEN = "add_your_token_here"  # Replace with your GitHub PAT
# REPO = "bebedudu/activeuser"  # Replace with your repo (username/repo)
# FILE_PATH = "activeuserinfo.txt"  # Path to the file in the repo
# BRANCH = "main"  # The branch to modify
# API_BASE_URL = "https://api.github.com"
# INTERVAL = 60  # Time interval in seconds to check and update

# # Headers for GitHub API authentication
# HEADERS = {
#     "Authorization": f"token {GITHUB_TOKEN}",
#     "Accept": "application/vnd.github.v3+json",
# }

# def get_public_ip():
#     """Get the public IP address of the user."""
#     try:
#         response = requests.get('https://api64.ipify.org?format=json')
#         response.raise_for_status()
#         return response.json().get('ip')
#     except requests.RequestException as e:
#         print(f"Error fetching public IP: {e}")
#         return None

# def get_geolocation(ip_address):
#     """Get geolocation details for the given IP address."""
#     try:
#         api_url = f"https://ipinfo.io/{ip_address}?token=ccb3ba52662beb"  # Replace with your ipinfo token
#         response = requests.get(api_url)
#         response.raise_for_status()
#         data = response.json()

#         # Extract relevant details
#         country = data.get("country", "N/A")
#         region = data.get("region", "N/A")
#         city = data.get("city", "N/A")
#         org = data.get("org", "N/A")
#         loc = data.get("loc", "N/A")
#         postal = data.get("postal", "N/A")
#         timezone = data.get("timezone", "N/A")
#         return country, region, city, org, loc, postal, timezone
#     except requests.RequestException as e:
#         print(f"Error fetching geolocation: {e}")
#         return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

# def get_system_info():
#     """Get detailed system information as a string."""
#     info = {
#         "System": platform.system(),
#         "Node Name": platform.node(),
#         "Release": platform.release(),
#         "Version": platform.version(),
#         "Machine": platform.machine(),
#         "Processor": platform.processor(),
#         "CPU Cores": psutil.cpu_count(logical=False),
#         "Logical CPUs": psutil.cpu_count(logical=True),
#         "Total RAM": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
#         "Available RAM": f"{psutil.virtual_memory().available / (1024 ** 3):.2f} GB",
#         "Used RAM": f"{psutil.virtual_memory().used / (1024 ** 3):.2f} GB",
#         "RAM Usage": f"{psutil.virtual_memory().percent} percent",
#         "Disk Usage": {partition.mountpoint: {
#             "Total": f"{psutil.disk_usage(partition.mountpoint).total / (1024 ** 3):.2f} GB",
#             "Used": f"{psutil.disk_usage(partition.mountpoint).used / (1024 ** 3):.2f} GB",
#             "Free": f"{psutil.disk_usage(partition.mountpoint).free / (1024 ** 3):.2f} GB",
#             "Usage": f"{psutil.disk_usage(partition.mountpoint).percent} percent"
#         } for partition in psutil.disk_partitions()},
#         "IP Address": socket.gethostbyname(socket.gethostname()),
#         "MAC Address": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])
#     }

#     # Convert system info to a single line JSON string
#     system_info_str = json.dumps(info, separators=(',', ':'))
#     return system_info_str

# def update_active_user_file(new_entry):
#     """Update the active user file on GitHub."""
#     # Fetch the current file content
#     file_url = f"{API_BASE_URL}/repos/{REPO}/contents/{FILE_PATH}"
#     response = requests.get(file_url, headers=HEADERS)
#     if response.status_code == 200:
#         file_data = response.json()
#         current_content = base64.b64decode(file_data['content']).decode('utf-8')
#         sha = file_data['sha']
#     else:
#         print(f"Failed to fetch file content: {response.status_code} - {response.json()}")
#         return

#     # Append the new entry
#     updated_content = current_content + new_entry
#     encoded_content = base64.b64encode(updated_content.encode('utf-8')).decode('utf-8')

#     # Update the file on GitHub
#     update_payload = {
#         "message": f"Update active user log with system info",
#         "content": encoded_content,
#         "sha": sha,
#         "branch": BRANCH,
#     }

#     response = requests.put(file_url, headers=HEADERS, data=json.dumps(update_payload))
#     if response.status_code == 200:
#         print("File updated successfully!")
#     else:
#         print(f"Failed to update file: {response.status_code} - {response.json()}")

# def main():
#     """Main function to repeatedly log active user with system info."""
#     while True:
#         try:
#             # Get active user info
#             active_user = os.getlogin()
#             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#             # Get public IP, geolocation, and system info
#             user_ip = get_public_ip()
#             country, region, city, org, loc, postal, timezone = get_geolocation(user_ip) if user_ip else ("N/A",) * 7
#             system_info = get_system_info()

#             # Create new entry
#             new_entry = (f"{timestamp} - User: {active_user}, IP: {user_ip}, Location: {country}, {region}, {city}, Org: {org}, "
#                          f"Coordinates: {loc}, Postal: {postal}, TimeZone: {timezone}, System Info: {system_info}\n")

#             # Update the file
#             update_active_user_file(new_entry)
#         except Exception as e:
#             print(f"An error occurred: {e}")
#         time.sleep(INTERVAL)  # Wait for the specified interval before the next update

# if __name__ == "__main__":
#     main()







# # run with other function too 
# import os
# import base64
# import json
# import requests
# from datetime import datetime
# import time
# import platform
# import psutil
# import socket
# import uuid

# # GitHub Configuration
# GITHUB_TOKEN = "add_your_token_here"  # Replace with your GitHub PAT
# REPO = "bebedudu/activeuser"  # Replace with your repo (username/repo)
# FILE_PATH = "activeuserinfo.txt"  # Path to the file in the repo
# BRANCH = "main"  # The branch to modify
# API_BASE_URL = "https://api.github.com"
# INTERVAL = 10  # Time interval in seconds to check and update

# # Headers for GitHub API authentication
# HEADERS = {
#     "Authorization": f"token {GITHUB_TOKEN}",
#     "Accept": "application/vnd.github.v3+json",
# }

# def get_public_ip():
#     """Get the public IP address of the user."""
#     try:
#         response = requests.get('https://api64.ipify.org?format=json')
#         response.raise_for_status()
#         return response.json().get('ip')
#     except requests.RequestException as e:
#         print(f"Error fetching public IP: {e}")
#         return None

# def get_geolocation(ip_address):
#     """Get geolocation details for the given IP address."""
#     try:
#         api_url = f"https://ipinfo.io/{ip_address}?token=ccb3ba52662beb"  # Replace with your ipinfo token
#         response = requests.get(api_url)
#         response.raise_for_status()
#         data = response.json()

#         # Extract relevant details
#         country = data.get("country", "N/A")
#         region = data.get("region", "N/A")
#         city = data.get("city", "N/A")
#         org = data.get("org", "N/A")
#         loc = data.get("loc", "N/A")
#         postal = data.get("postal", "N/A")
#         timezone = data.get("timezone", "N/A")
#         return country, region, city, org, loc, postal, timezone
#     except requests.RequestException as e:
#         print(f"Error fetching geolocation: {e}")
#         return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

# def get_system_info():
#     """Get detailed system information as a string."""
#     info = {
#         "System": platform.system(),
#         "Node Name": platform.node(),
#         "Release": platform.release(),
#         "Version": platform.version(),
#         "Machine": platform.machine(),
#         "Processor": platform.processor(),
#         "CPU Cores": psutil.cpu_count(logical=False),
#         "Logical CPUs": psutil.cpu_count(logical=True),
#         "Total RAM": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
#         "Available RAM": f"{psutil.virtual_memory().available / (1024 ** 3):.2f} GB",
#         "Used RAM": f"{psutil.virtual_memory().used / (1024 ** 3):.2f} GB",
#         "RAM Usage": f"{psutil.virtual_memory().percent} percent",
#         "Disk Usage": {partition.mountpoint: {
#             "Total": f"{psutil.disk_usage(partition.mountpoint).total / (1024 ** 3):.2f} GB",
#             "Used": f"{psutil.disk_usage(partition.mountpoint).used / (1024 ** 3):.2f} GB",
#             "Free": f"{psutil.disk_usage(partition.mountpoint).free / (1024 ** 3):.2f} GB",
#             "Usage": f"{psutil.disk_usage(partition.mountpoint).percent} percent"
#         } for partition in psutil.disk_partitions()},
#         "IP Address": socket.gethostbyname(socket.gethostname()),
#         "MAC Address": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])
#     }

#     # Convert system info to a single line JSON string
#     system_info_str = json.dumps(info, separators=(',', ':'))
#     return system_info_str

# def update_active_user_file(new_entry, active_user):
#     """Update the active user file on GitHub."""
#     # Fetch the current file content
#     file_url = f"{API_BASE_URL}/repos/{REPO}/contents/{FILE_PATH}"
#     response = requests.get(file_url, headers=HEADERS)
#     if response.status_code == 200:
#         file_data = response.json()
#         current_content = base64.b64decode(file_data["content"]).decode("utf-8")
#         sha = file_data["sha"]
#     else:
#         print(f"Failed to fetch file content: {response.status_code} - {response.json()}")
#         return

#     # Append the new entry
#     updated_content = current_content + new_entry
#     encoded_content = base64.b64encode(updated_content.encode("utf-8")).decode("utf-8")

#     # Update the file on GitHub
#     update_payload = {
#         "message": f"Update active user log with system info - {active_user}",
#         "content": encoded_content,
#         "sha": sha,
#         "branch": BRANCH,
#     }

#     response = requests.put(file_url, headers=HEADERS, data=json.dumps(update_payload))
#     if response.status_code == 200:
#         print(f"File updated successfully! New entry: {new_entry}")
#     else:
#         print(f"Failed to update file: {response.status_code} - {response.json()}")

# def log_active_user():
#     """Log the active user information with system info."""
#     try:
#         # Get active user info
#         active_user = os.getlogin()
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#         # Get public IP, geolocation, and system info
#         user_ip = get_public_ip()
#         country, region, city, org, loc, postal, timezone = get_geolocation(user_ip) if user_ip else ("N/A",) * 7
#         system_info = get_system_info()

#         # Create new entry
#         new_entry = (f"{timestamp} - User: {active_user}, IP: {user_ip}, Location: {country}, {region}, {city}, Org: {org}, "
#                      f"Coordinates: {loc}, Postal: {postal}, TimeZone: {timezone}, System Info: {system_info}\n")

#         # Update the file
#         update_active_user_file(new_entry, active_user)

#     except Exception as e:
#         print(f"An error occurred: {e}")

# def additional_task():
#     """An example of another function that runs independently."""
#     print("Performing an additional task...")

# def main():
#     """Main function to repeatedly log active user with system info."""
#     try:
#         while True:
#             log_active_user()  # Call the function to log the user info
#             additional_task()  # Call the additional task function
#             time.sleep(INTERVAL)  # Wait for the specified interval before the next update
#     except KeyboardInterrupt:
#         print("Exiting the logging loop. Done!")

# if __name__ == "__main__":
#     main()













# # with internet connection and without internet connection fixed
# import os
# import base64
# import json
# import requests
# from datetime import datetime
# import time
# import platform
# import psutil
# import socket
# import uuid

# # GitHub Configuration
# GITHUB_TOKEN = "add_your_token_here"  # Replace with your GitHub PAT
# REPO = "bebedudu/activeuser"  # Replace with your repo (username/repo)
# FILE_PATH = "activeuserinfo.txt"  # Path to the file in the repo
# BRANCH = "main"  # The branch to modify
# API_BASE_URL = "https://api.github.com"
# INTERVAL = 60  # Time interval in seconds to check and update

# # Headers for GitHub API authentication
# HEADERS = {
#     "Authorization": f"token {GITHUB_TOKEN}",
#     "Accept": "application/vnd.github.v3+json",
# }


# def is_internet_available():
#     """Check if the internet connection is available."""
#     try:
#         requests.get("https://www.google.com", timeout=3)
#         return True
#     except requests.RequestException:
#         return False


# def get_public_ip():
#     """Get the public IP address of the user."""
#     try:
#         response = requests.get("https://api64.ipify.org?format=json")
#         response.raise_for_status()
#         return response.json().get("ip")
#     except requests.RequestException as e:
#         print(f"Error fetching public IP: {e}")
#         return None


# def get_geolocation(ip_address):
#     """Get geolocation details for the given IP address."""
#     try:
#         api_url = f"https://ipinfo.io/{ip_address}?token=ccb3ba52662beb"  # Replace with your ipinfo token
#         response = requests.get(api_url)
#         response.raise_for_status()
#         data = response.json()
#         return (
#             data.get("country", "N/A"),
#             data.get("region", "N/A"),
#             data.get("city", "N/A"),
#             data.get("org", "N/A"),
#             data.get("loc", "N/A"),
#             data.get("postal", "N/A"),
#             data.get("timezone", "N/A"),
#         )
#     except requests.RequestException as e:
#         print(f"Error fetching geolocation: {e}")
#         return ("N/A",) * 7


# def get_system_info():
#     """Get detailed system information as a string."""
#     info = {
#         "System": platform.system(),
#         "Node Name": platform.node(),
#         "Release": platform.release(),
#         "Version": platform.version(),
#         "Machine": platform.machine(),
#         "Processor": platform.processor(),
#         "CPU Cores": psutil.cpu_count(logical=False),
#         "Logical CPUs": psutil.cpu_count(logical=True),
#         "Total RAM": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
#         "Available RAM": f"{psutil.virtual_memory().available / (1024 ** 3):.2f} GB",
#         "Used RAM": f"{psutil.virtual_memory().used / (1024 ** 3):.2f} GB",
#         "RAM Usage": f"{psutil.virtual_memory().percent} percent",
#         "Disk Usage": {
#             partition.mountpoint: {
#                 "Total": f"{psutil.disk_usage(partition.mountpoint).total / (1024 ** 3):.2f} GB",
#                 "Used": f"{psutil.disk_usage(partition.mountpoint).used / (1024 ** 3):.2f} GB",
#                 "Free": f"{psutil.disk_usage(partition.mountpoint).free / (1024 ** 3):.2f} GB",
#                 "Usage": f"{psutil.disk_usage(partition.mountpoint).percent} percent"
#             }
#             for partition in psutil.disk_partitions()
#         },
#         "IP Address": socket.gethostbyname(socket.gethostname()),
#         "MAC Address": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])
#     }
#     return json.dumps(info, separators=(",", ":"))


# def update_active_user_file(new_entry, active_user):
#     """Update the active user file on GitHub."""
#     file_url = f"{API_BASE_URL}/repos/{REPO}/contents/{FILE_PATH}"
#     try:
#         response = requests.get(file_url, headers=HEADERS)
#         if response.status_code == 200:
#             file_data = response.json()
#             current_content = base64.b64decode(file_data["content"]).decode("utf-8")
#             sha = file_data["sha"]
#         else:
#             print(f"Failed to fetch file content: {response.status_code} - {response.json()}")
#             return

#         updated_content = current_content + new_entry
#         encoded_content = base64.b64encode(updated_content.encode("utf-8")).decode("utf-8")

#         update_payload = {
#             "message": f"Update active user log with system info - {active_user}",
#             "content": encoded_content,
#             "sha": sha,
#             "branch": BRANCH,
#         }

#         response = requests.put(file_url, headers=HEADERS, data=json.dumps(update_payload))
#         if response.status_code == 200:
#             print(f"File updated successfully! New entry: {new_entry}")
#         else:
#             print(f"Failed to update file: {response.status_code} - {response.json()}")
#     except Exception as e:
#         print(f"Error updating file: {e}")


# def log_active_user():
#     """Log the active user information with system info."""
#     if not is_internet_available():
#         print("No internet connection. Skipping this update cycle.")
#         return

#     try:
#         active_user = os.getlogin()
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#         user_ip = get_public_ip()
#         country, region, city, org, loc, postal, timezone = get_geolocation(user_ip) if user_ip else ("N/A",) * 7
#         system_info = get_system_info()

#         new_entry = (
#             f"{timestamp} - User: {active_user}, IP: {user_ip}, Location: {country}, {region}, {city}, Org: {org}, "
#             f"Coordinates: {loc}, Postal: {postal}, TimeZone: {timezone}, System Info: {system_info}\n"
#         )
#         update_active_user_file(new_entry, active_user)
#     except Exception as e:
#         print(f"An error occurred: {e}")


# def main():
#     """Main function to repeatedly log active user with system info."""
#     while True:
#         log_active_user()
#         time.sleep(INTERVAL)


# if __name__ == "__main__":
#     main()

















import os
import base64
import json
import requests
from datetime import datetime
import time
import platform
import psutil
import socket
import uuid

# GitHub Configuration
GITHUB_TOKEN = "add_your_token_here"  # Replace with your GitHub PAT
REPO = "bebedudu/activeuser"  # Replace with your repo (username/repo)
FILE_PATH = "activeuserinfo.txt"  # Path to the file in the repo
BRANCH = "main"  # The branch to modify
API_BASE_URL = "https://api.github.com"
INTERVAL_URL = "https://raw.githubusercontent.com/bebedudu/autoupdate/main/interval.json"  # Interval JSON URL

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
        print(f"Failed to fetch interval from URL. Using default: {DEFAULT_INTERVAL} seconds")
        return DEFAULT_INTERVAL


def get_public_ip():
    """Get the public IP address of the user."""
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        response.raise_for_status()
        return response.json().get("ip")
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None


def get_geolocation(ip_address):
    """Get geolocation details for the given IP address."""
    try:
        api_url = f"https://ipinfo.io/{ip_address}?token=ccb3ba52662beb"  # Replace with your ipinfo token
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
        "RAM Usage": f"{psutil.virtual_memory().percent} percent",
        "Disk Usage": {
            partition.mountpoint: {
                "Total": f"{psutil.disk_usage(partition.mountpoint).total / (1024 ** 3):.2f} GB",
                "Used": f"{psutil.disk_usage(partition.mountpoint).used / (1024 ** 3):.2f} GB",
                "Free": f"{psutil.disk_usage(partition.mountpoint).free / (1024 ** 3):.2f} GB",
                "Usage": f"{psutil.disk_usage(partition.mountpoint).percent} percent"
            }
            for partition in psutil.disk_partitions()
        },
        "IP Address": socket.gethostbyname(socket.gethostname()),
        "MAC Address": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])
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
        print(f"An error occurred: {e}")

def additional_task():
    """An example of another function that runs independently."""
    print("Performing an additional task...")


def main():
    """Main function to repeatedly log active user with system info."""
    global DEFAULT_INTERVAL
    try:
        while True:
            DEFAULT_INTERVAL = fetch_interval()  # Fetch updated interval
            log_active_user()
            additional_task()  # Call the additional task function
            time.sleep(DEFAULT_INTERVAL)
    except KeyboardInterrupt:
        print("Exiting the logging loop. Done!")

if __name__ == "__main__":
    main()
