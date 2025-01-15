# This function switches the relay on the GPIO pin configured in the .env file in the root of the project. The function is called by the main function when the temperature is above the threshold. The function uses the GPIO library to switch the relay on and off.

import os
import RPi.GPIO as GPIO
from dotenv import load_dotenv

load_dotenv()

def switchRelay(targetState):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(int(os.getenv('RELAY_GPIO')), GPIO.OUT)
    GPIO.output(int(os.getenv('RELAY_GPIO')), targetState)
    GPIO.cleanup()
