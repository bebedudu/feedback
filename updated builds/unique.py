import uuid
import hashlib
import re

unique_id = uuid.uuid4()
print(unique_id)


def get_mac_address():
    mac = uuid.getnode()
    mac_str = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
    print(mac_str)
    return mac_str

def generate_computer_id():
    mac_address = get_mac_address()
    computer_id = hashlib.md5(mac_address.encode()).hexdigest()
    print(computer_id)
    return computer_id

unique_id = generate_computer_id()
print(unique_id)


import subprocess

def get_windows_uuid():
    try:
        output = subprocess.check_output('wmic csproduct get uuid', shell=True).decode()
        return output.split('\n')[1].strip()
    except Exception as e:
        return str(e)

print("Windows Persistent UUID:", get_windows_uuid())



import hashlib
import platform
import os

def get_persistent_machine_id():
    # Gather system-specific information
    system_info = f"{platform.node()}_{platform.system()}_{platform.release()}_{platform.processor()}_{os.getenv('PROCESSOR_IDENTIFIER', '')}"
    # Hash the combined system information
    return hashlib.sha256(system_info.encode()).hexdigest()

machine_id = get_persistent_machine_id()
print("Persistent Machine ID:", machine_id)


import hashlib
import os
import platform

def get_hashed_system_identity():
    system_info = f"{platform.node()}_{platform.system()}_{platform.release()}_{os.getenv('PROCESSOR_IDENTIFIER', '')}"
    return hashlib.sha256(system_info.encode()).hexdigest()

print("Hashed System Identity:", get_hashed_system_identity())










# Function to get the BIOS UUID on Windows for unique identification
def get_windows_uuid():
    try:
        output = subprocess.check_output('wmic csproduct get uuid', shell=True).decode()
        uuid_value = output.split('\n')[1].strip()
        if uuid_value:
            return uuid_value
        else:
            raise ValueError("Empty UUID value")
    except Exception as e:
        # logging.warning(f"Failed to get BIOS UUID: {e}")
        print(f"Failed to get BIOS UUID: {e}")
        return get_mac_address()  # Fallback to MAC address if BIOS UUID retrieval fails
# Function to get the MAC address (used if BIOS UUID retrieval fails)
def get_mac_address():
    try:
        mac = uuid.getnode()
        mac_str = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
        if mac_str:
            return mac_str
        else:
            raise ValueError("Failed to get MAC address")
    except Exception as e:
        # logging.error(f"Failed to get MAC address: {e}")
        print(f"Failed to get MAC address: {e}")
        return str(e)
# Main script
# logging.info(f"🖥️ Windows Persistent UUID: {get_windows_uuid()}")
print("🖥️ Windows Persistent UUID:", get_windows_uuid())
unique_id = get_windows_uuid()  # generate universally unique identifiers (UUIDs) across all devices