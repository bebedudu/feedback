# keylogger

<a href="https://github.com/bebedudu/autoupdate">👉 Download application</a>

# Keylogger and Screenshot Monitoring Application

## Table of Contents
- [Introduction](#introduction)
- [System Features](#system-features)
- [Functional Requirements](#functional-requirements)
- [Non-Functional Requirements](#non-functional-requirements)
- [System Design](#system-design)
- [Installation](#installation)
- [Usage](#usage)
- [Limitations](#limitations)
- [Legal and Ethical Considerations](#legal-and-ethical-considerations)

---

## Introduction

This application is a Python-based monitoring tool that combines keylogging and periodic screenshot capturing functionality. It integrates seamlessly with the system tray, offering dynamic menus and notifications for better user interaction. 

> **Disclaimer:** This software is intended for ethical purposes, such as self-monitoring or parental control, with explicit consent. Unauthorized use may violate privacy laws.

---

## System Features

### 1. **Screenshot Capture**
- Periodically captures screenshots and saves them with a timestamp.
- User-configurable intervals through the tray menu (30s, 60s, 120s, 300s).
- Pause and resume functionality.

### 2. **Keylogging**
- Captures and logs keystrokes in real-time.
- Logs are saved locally for user review.
- Toggle keylogging via the system tray.

### 3. **Clipboard Monitoring**
- Monitors clipboard activity and saves copied content.

### 4. **System Tray Integration**
- A tray icon with a menu for quick access to features:
  - Start/Stop keylogging and screenshot capturing.
  - Set screenshot intervals dynamically.
  - Enable/Disable startup at boot.
  - View logs and restart the application.
  - Access the developer page.

### 5. **Notifications**
- Provides system notifications for key events (e.g., enabling/disabling features).

### 6. **Startup Configuration**
- Allows enabling or disabling the application to run at system startup.

### 7. **Error Logging**
- Logs errors and important events for debugging and monitoring purposes.

---

## Functional Requirements

### User Interactions
- The user can start or stop keylogging and screenshot capturing via the system tray menu.
- The user can configure the screenshot interval dynamically.

### File Management
- Screenshots are saved in a user-defined folder with a timestamp-based naming format.
- Logs of keystrokes and clipboard activity are stored in a `.txt` file.

### Notifications
- Notifications inform users about changes, such as enabling/disabling features or errors.

### System Tray Menu Options
- Toggle screenshots and keylogging.
- Adjust screenshot intervals.
- Enable or disable startup at boot.
- View logs and access developer information.
- Restart or exit the application.

---

## Non-Functional Requirements

### Performance
- The application must run efficiently without impacting system performance.
- Screenshots and keylogging operations should not consume excessive memory or CPU.

### Usability
- The system tray menu must be intuitive and easy to navigate.
- Notifications should clearly convey the status of features.

### Security
- Logs and screenshots should be stored securely, preventing unauthorized access.
- The application must not execute any unauthorized actions on the user's system.

### Compatibility
- **Operating System**: Windows 10 or later.
- **Python Version**: 3.8 or later.

---

## System Design

### Architecture
- **Threads**: Separate threads for screenshot capturing, keylogging, and clipboard monitoring.
- **System Tray**: Built using the `pystray` library.
- **Notification System**: Leverages platform-specific APIs for notifications.

### Libraries Used
- `pyautogui`: For capturing screenshots.
- `keyboard`: For keylogging.
- `pystray`: For system tray integration.
- `Pillow`: For handling tray icon images.
- `requests`: For downloading icons from URLs.

---

## Installation

### Prerequisites
1. Python 3.8 or later installed.
2. Required libraries installed via `pip`.

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/username/repository.git
   ```
2. Navigate to the project directory:
   ```bash
   cd repository
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```

---

## Usage

1. Launch the application.
2. Access the system tray icon for control:
   - Toggle features like screenshots or keylogging.
   - Adjust screenshot intervals or view logs.
3. Notifications will inform you of key events.

---

## Limitations

- Only supports Windows operating systems.
- Icons and notifications depend on system-specific APIs and may vary slightly.

---

## Legal and Ethical Considerations

**Warning**: Unauthorized monitoring of another user's system is illegal and unethical. This software is intended for lawful purposes only, such as:
- Monitoring personal devices.
- Parental control (with consent).
- Debugging or educational purposes.

> Always obtain explicit consent from the user before deploying this application.

---
