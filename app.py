from functions import *
from auth import *
import cv2
import numpy as np
import math
import time
import csv
from ultralytics import YOLO

# Report the device information to the server
reportBeehive()

# Load YOLO model (optimized for Raspberry Pi)
model = YOLO('/opt/beeInnovativeClient/yolov11_custom8_640.onnx')  # Change to your model

# Open camera
cap = cv2.VideoCapture(0)  # Use 0 for USB cam, change if needed

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

# Continuous detection loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

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
                # Convert to HSV for better color detection
                hsv_center = cv2.cvtColor(center_region, cv2.COLOR_BGR2HSV)

                # Define RED, BLUE, and GREEN color ranges in HSV
                red_lower1, red_upper1 = np.array([0, 100, 100]), np.array([10, 255, 255])
                red_lower2, red_upper2 = np.array([160, 100, 100]), np.array([180, 255, 255])
                blue_lower, blue_upper = np.array([90, 100, 100]), np.array([140, 255, 255])
                green_lower, green_upper = np.array([35, 100, 100]), np.array([85, 255, 255])

                # Create masks for each color
                red_mask = cv2.inRange(hsv_center, red_lower1, red_upper1) + cv2.inRange(hsv_center, red_lower2, red_upper2)
                blue_mask = cv2.inRange(hsv_center, blue_lower, blue_upper)
                green_mask = cv2.inRange(hsv_center, green_lower, green_upper)

                # Count pixels for each color
                red_count = np.count_nonzero(red_mask)
                blue_count = np.count_nonzero(blue_mask)
                green_count = np.count_nonzero(green_mask)

                # Determine dominant marking color
                color_label = "Unknown"
                if red_count > blue_count and red_count > green_count:
                    color_label = "Red"
                elif blue_count > red_count and blue_count > green_count:
                    color_label = "Blue"
                elif green_count > red_count and green_count > blue_count:
                    color_label = "Green"

                # Store detected marking color
                if color_label != "Unknown":
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

            # **Write data to DB**
            saveHornetDetection(final_marking, flight_angle)
            print(f"\n[!] Hornet Event Stored in CSV")
            print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Final Detected Marking Color: {final_marking}")
            print(f"Final Flight Direction: {flight_angle:.2f}°")

            # **Reset tracking for the next occurrence**
            tracked_positions = []
            detected_markings = []
            last_detection_time = time.time()  # Reset timer

cap.release()
