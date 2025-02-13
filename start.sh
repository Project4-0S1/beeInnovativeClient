#!/bin/bash

# Define the ffmpeg command
FFMPEG_CMD="ffmpeg -f v4l2 -input_format yuyv422 -framerate 30 -video_size 1280x720 -i /dev/video0 -c:v libx264 -preset ultrafast -f rtsp rtsp://localhost:8554/live/stream"

# Loop to keep trying ffmpeg
while true; do
    echo "Starting ffmpeg..."
    
    # Run ffmpeg and capture the error output
    OUTPUT=$($FFMPEG_CMD 2>&1)
    
    # Check if the output contains the "Connection refused" error
    if echo "$OUTPUT" | grep -q "Connection to tcp://localhost:8554.*failed: Connection refused"; then
        echo "Connection refused detected. Stopping script."

        # Run the application
        echo "Starting BeeInnovativeClient..."
        /opt/beeInnovativeClient/client/bin/python /opt/beeInnovativeClient/app.py
        
        break
    fi

    echo "ffmpeg stopped, retrying..."
    sleep 1  # Small delay before retrying
done
