import requests
from dotenv import load_dotenv
import os
import uuid

load_dotenv()
API_URL = os.getenv("API_URL")


def reportDevice():
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])
    data = {
        "beehiveName": "Beehive Demo",
        "latitude": 51.160154648639526,
        "longitude": 5.003539056066445,
        "iotId": mac_address
    }
    response = requests.post(f"{API_URL}/api/beehives", json=data)

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        response_json = None

    print(response.status_code, response_json)