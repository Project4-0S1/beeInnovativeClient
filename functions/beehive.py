import requests
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime
from auth import *


load_dotenv()
API_URL = os.getenv("API_URL")

mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])

def reportBeehive():
    access_token = get_access_token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "beehiveName": "Raspberry Pi",
        "latitude": os.getenv("BEEHIVE_LATITUDE"),
        "longitude": os.getenv("BEEHIVE_LONGITUDE"),
        "iotId": mac_address,
        "lastCall": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),  # Use current datetime in the same format
    }
    
    # Try to update the beehive information
    response = requests.put(f"{API_URL}/api/beehives/{mac_address}", json=data, headers=headers)
    
    if response.status_code == 404:
        # If the beehive does not exist, create it
        response = requests.post(f"{API_URL}/api/beehives", json=data, headers=headers)

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        response_json = None

    print(response.status_code, response_json)

def reportBeehiveLocation():
    access_token = get_access_token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "latitude": os.getenv("BEEHIVE_LATITUDE"),
        "longitude": os.getenv("BEEHIVE_LONGITUDE")
    }
    response = requests.put(f"{API_URL}/api/beehives/iot/{mac_address}", json=data, headers=headers)

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        response_json = None

    print(response.status_code, response_json)