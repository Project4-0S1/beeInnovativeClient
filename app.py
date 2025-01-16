import time
from functions import *

# Report the device information to the server
reportDevice()

# Turn on the relay
switchRelay(True)

# Wait for 1 second
time.sleep(1)

# Turn off the relay
switchRelay(False)