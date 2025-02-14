import requests

def get_public_ip():
    try:
        # Use an external service to get the public IP address
        response = requests.get('https://api64.ipify.org?format=json')
        response.raise_for_status()
        ip = response.json().get('ip')
        return ip
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None

def get_geolocation(ip_address):
    try:
        # Replace 'YOUR_TOKEN' with your ipinfo.io token
        api_url = f"https://ipinfo.io/{ip_address}?token=ccb3ba52662beb"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        # Extract relevant details
        country = data.get("country", "N/A")
        region = data.get("region", "N/A")
        city = data.get("city", "N/A")
        org = data.get("org", "N/A")
        loc = data.get("loc", "N/A")
        postal = data.get("postal", "N/A")
        timezone = data.get("timezone", "N/A")
        return country, region, city, org, loc, postal, timezone
    except requests.RequestException as e:
        print(f"Error fetching geolocation: {e}")
        return None, None, None
    
ip_address = get_public_ip()
print(f"the ip address is: {ip_address}")
country, region, city, org, loc, postal, timezone = get_geolocation(ip_address)
print(f"Country: {country}, Region: {region}, City: {city}")

if __name__ == "__main__":
    # Step 1: Get the user's public IP
    user_ip = get_public_ip()
    if user_ip:
        print(f"Public IP: {user_ip}")
        
        # Step 2: Get geolocation info
        country, region, city, org, loc, postal, timezone = get_geolocation(user_ip)
        print(f"Country: {country}")
        print(f"Region: {region}")
        print(f"City: {city}")
        print(f"Org: {org}")
        print(f"Location: {loc}")
        print(f"Postal: {postal}")
        print(f"TimeZone: {timezone}")
    else:
        print("Could not fetch public IP address.")
