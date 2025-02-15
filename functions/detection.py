import requests
from dotenv import load_dotenv
import os
import uuid
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS detection (
    ID INTEGER PRIMARY KEY,
    detectionTime DATETIME,
    hornetId INTEGER,
    direction INTEGER,
    isMarked BOOLEAN DEFAULT 0
);
''')

load_dotenv()
API_URL = os.getenv("API_URL")

mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])

# Write the detection to the DB
def saveHornetDetection(color, directionValue, isMarked):
    # Assign hornet ID based on color
    color_to_hornet_id = {
        "Red": 1,
        "Blue": 2,
        "Green": 3
    }
    hornetID = color_to_hornet_id.get(color, 4)  # Default to 0 if color is not found

    # Round the direction value to the nearest integer
    directionValue = round(directionValue)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO detection (detectionTime, hornetId, direction, isMarked) VALUES (datetime('now'), ?, ?, ?)", (hornetID, directionValue, isMarked))
    conn.commit()
    conn.close()

conn.close()