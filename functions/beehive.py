import requests
from dotenv import load_dotenv
import os
import uuid

load_dotenv()
API_URL = os.getenv("API_URL")

mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])

def reportBeehive():

    data = {
        "beehiveName": "Baguette",
        "latitude": os.getenv("BEEHIVE_LATITUDE"),
        "longitude": os.getenv("BEEHIVE_LONGITUDE"),
        "iotId": mac_address
    }
    response = requests.post(f"{API_URL}/api/beehives", json=data)

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        response_json = None

    print(response.status_code, response_json)


def reportBeehiveLocation():
    data = {
        "latitude": os.getenv("BEEHIVE_LATITUDE"),
        "longitude": os.getenv("BEEHIVE_LONGITUDE")
    }
    response = requests.put(f"{API_URL}/api/beehives/iot/{mac_address}", json=data)

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        response_json = None

    print(response.status_code, response_json)



