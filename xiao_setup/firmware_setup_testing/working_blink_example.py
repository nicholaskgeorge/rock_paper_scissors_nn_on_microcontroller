from machine import Pin
import time

# Set up the LED pin
led = Pin(21, Pin.OUT)  # GPIO10 for onboard LED
#led.on()  # Turn LED on
#led.value(1)
half_delay = 1

"""
led.value(1)  # Turn on LED
time.sleep(half_delay)  # Wait for 0.5 seconds
led.value(0)  # Turn off LED
#time.sleep(half_delay)  # Wait for 0.5 seconds
"""

while True:
    led.value(1)  # Turn on LED
    time.sleep(half_delay)  # Wait for 0.5 seconds
    led.value(0)  # Turn off LED
    time.sleep(half_delay)  # Wait for 0.5 seconds