import sqlite3
import json
import uuid
import requests
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()
API_URL = os.getenv("API_URL")

# Connect to the database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Fetch all detections
cursor.execute("SELECT detectionTime, hornetId, direction FROM detection")
detections = cursor.fetchall()

# Generate the mac address
# mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])
mac_address = "1"
# Prepare the data
detection_list = []
for detection in detections:
    detection_time = datetime.fromtimestamp(detection[0] / 1000).isoformat()
    detection_data = {
        "detectionTimeStamp": detection_time,
        "isGemarkeerd": True,
        "direction": detection[2],
        "hornetId": detection[1],
        "BeehiveID": mac_address
    }
    detection_list.append(detection_data)

# Print the JSON value
json_data = json.dumps(detection_list, indent=4)
print(json_data)

# Publish the JSON list to /api/HornetDetections/multiple
response = requests.post(f"{API_URL}/api/HornetDetections/multiple", json=detection_list)

# Print the response status and content
print(response.status_code)
try:
    print(response.json())
except requests.exceptions.JSONDecodeError:
    print("Response is not in JSON format")

# Clear the detection table
# cursor.execute("DELETE FROM detection")
conn.commit()

# Close the connection
conn.close()