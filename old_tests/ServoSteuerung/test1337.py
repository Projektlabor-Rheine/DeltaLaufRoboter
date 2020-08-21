"""Simple test for a standard servo on channel 0 and a continuous rotation servo on channel 1."""

import time

from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.

# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.

kit = ServoKit(channels=16)

kit.servo[0].angle = 60

time.sleep(1)

kit.servo[0].angle = 30

time.sleep(1)
