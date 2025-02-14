import sqlite3
import json
import uuid
import requests
from dotenv import load_dotenv
import os
from datetime import datetime
from auth import *
from functions import *
import threading

# Load environment variables
load_dotenv()
API_URL = os.getenv("API_URL")

# Connect to the database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Fetch all detections
cursor.execute("SELECT detectionTime, hornetId, direction, isMarked FROM detection")
detections = cursor.fetchall()

# Generate the mac address
mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])

# Prepare the data
detection_list = []
for detection in detections:
    detection_time = datetime.strptime(detection[0], '%Y-%m-%d %H:%M:%S').isoformat()  # Convert to ISO format without 'Z' suffix
    detection_data = {
        "detectionTimeStamp": detection_time,
        "isMarked": False if detection[3] == 0 else True,
        "direction": detection[2],
        "hornetId": detection[1],
        "BeehiveId": mac_address
    }
    detection_list.append(detection_data)

# Print the JSON value
json_data = json.dumps(detection_list, indent=4)
print(json_data)

# Function to switch relay on and off
def switch_relay(times):
    for _ in range(times):
        switchAlert(True)
        time.sleep(0.2)
        switchAlert(False)
        time.sleep(0.2)

if detection_list:
    access_token = get_access_token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    # Publish the JSON list to /api/HornetDetections/multiple
    response = requests.post(f"{API_URL}/api/HornetDetections/multiple", json=detection_list, headers=headers)

    # Print the response status and content
    print(response.status_code)
    try:
        print(response.json())
    except requests.exceptions.JSONDecodeError:
        print("Response is not in JSON format")

    # Switch relay based on response status
    if response.status_code == 200:
        threading.Thread(target=switch_relay, args=(2,)).start()
        # Clear the detection table
        cursor.execute("DELETE FROM detection")
        conn.commit()
    else:
        threading.Thread(target=switch_relay, args=(8,)).start()


else:
    # No detections, switch the relay 3 times
    threading.Thread(target=switch_relay, args=(3,)).start()

# Close the connection
conn.close()