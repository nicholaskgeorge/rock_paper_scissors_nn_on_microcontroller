from machine import Pin
import time

# Set up the LED pin
led = Pin(21, Pin.OUT)  # GPIO10 for onboard LED
led.on()  # Turn LED on
led.value(1)

"""

# Blink the LED
while True:
    led.on()  # Turn LED on
    led.value(1)  
    time.sleep(0.5)  # Wait for 0.5 seconds
    led.value(0)
    led.off()  # Turn LED off
    time.sleep(0.5)  # Wait for 0.5 seconds
    
"""
