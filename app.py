from functions import *
from auth import *
import cv2
import numpy as np
import math
import time
import csv
from ultralytics import YOLO
import os
import RPi.GPIO as GPIO

# Load environment variables
from dotenv import load_dotenv
load_dotenv('/opt/beeInnovativeClient/.env')

# Get ALERT_GPIO pin from .env file
ALERT_GPIO = int(os.getenv('ALERT_GPIO', 25))

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ALERT_GPIO, GPIO.OUT)

def flash_light(duration=4):
    GPIO.output(ALERT_GPIO, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(ALERT_GPIO, GPIO.LOW)

# Report the device information to the server
reportBeehive()

# Load YOLO model (optimized for Raspberry Pi)
model = YOLO('/opt/beeInnovativeClient/yolov11_custom8_640.onnx')  # Change to your model

# Open camera
cap = cv2.VideoCapture(0)  # Use 0 for USB cam, change if needed

# Check if the camera stream is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    GPIO.cleanup()
    exit(1)

# CSV file setup (append mode)
csv_file = "hornet_tracking.csv"


# Ensure the CSV file has a header if it doesn't exist
if not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0:
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Flight Direction (°)", "Marking Color"])

# Tracking & detection storage
tracked_positions = []
detected_markings = []
last_detection_time = time.time()
NO_DETECTION_THRESHOLD = 3  # Store data if no detection for 3 seconds


lightFlashed = False
# Continuous detection loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if not lightFlashed:
        flash_light()
        lightFlashed = True

    # Perform object tracking
    results = model.track(frame, conf=0.3, max_det=1, persist=True)

    if results[0].boxes:


        last_detection_time = time.time()  # Reset timer since we detected something
        switchRelay(True)  # Turn the relay on

        for box in results[0].boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)

            # Compute centroid for movement tracking
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            tracked_positions.append((cx, cy))

            # Extract center region for marking color detection
            box_width = x2 - x1
            box_height = y2 - y1
            center_x1 = x1 + box_width // 3
            center_y1 = y1 + box_height // 3
            center_x2 = x2 - box_width // 3
            center_y2 = y2 - box_height // 3
            center_region = frame[center_y1:center_y2, center_x1:center_x2]

            if center_region.size > 0:
                # Convert to HSV for accurate color detection
                hsv_center = cv2.cvtColor(center_region, cv2.COLOR_BGR2HSV)

                # Define HSV color ranges for Red, Blue, Green
                color_ranges = {
                    "Red": [(0, 100, 100), (10, 255, 255), (160, 100, 100), (180, 255, 255)],
                    "Blue": [(90, 100, 100), (140, 255, 255)],
                    "Green": [(35, 100, 100), (85, 255, 255)]
                }

                # Count pixels for each color
                color_counts = {}
                for color, ranges in color_ranges.items():
                    mask = sum(cv2.inRange(hsv_center, np.array(ranges[i]), np.array(ranges[i + 1])) for i in range(0, len(ranges), 2))
                    color_counts[color] = np.count_nonzero(mask)

                # Determine the dominant color or mark as Unmarked
                if all(count < 100 for count in color_counts.values()):
                    color_label = "Unmarked"
                else:
                    color_label = max(color_counts, key=color_counts.get)

                # Append detected color
                detected_markings.append(color_label)

    # **Check if the hornet disappeared for X seconds**
    if time.time() - last_detection_time > NO_DETECTION_THRESHOLD:
        switchRelay(False)  # Turn the relay off
        if len(tracked_positions) > 5:  # Ensure we tracked something
            # **Process and store the flight data**
            if len(detected_markings) > 0:
                final_marking = max(set(detected_markings), key=detected_markings.count)
            else:
                final_marking = "Unknown"

            # Compute flight direction
            start_x, start_y = tracked_positions[0]
            end_x, end_y = tracked_positions[-1]

            dx = end_x - start_x
            dy = end_y - start_y
            flight_angle = (math.degrees(math.atan2(dy, dx)) + 90) % 360

            # When final detected color is Unmarked set isMarked to False
            isMarked = True if final_marking != "Unmarked" else False
            # **Write data to DB**
            saveHornetDetection(final_marking, flight_angle, isMarked)
            print(f"\n[!] Hornet Event Stored in CSV")
            print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Final Detected Marking Color: {final_marking}")
            print(f"Final Flight Direction: {flight_angle:.2f}°")

            # **Reset tracking for the next occurrence**
            tracked_positions = []
            detected_markings = []
            last_detection_time = time.time()  # Reset timer

cap.release()
GPIO.cleanup() 