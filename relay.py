import RPi.GPIO as GPIO
import time
import os
from dotenv import load_dotenv
load_dotenv()
# Setup
print("RELAY_GPIO:", os.getenv('RELAY_GPIO'))

def switchRelay(targetState):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(int(os.getenv('RELAY_GPIO')), GPIO.OUT)

    if targetState == False:
        targetState = GPIO.LOW
    else:
        targetState = GPIO.HIGH

    GPIO.output(int(os.getenv('RELAY_GPIO')), targetState)


switchRelay(True)
