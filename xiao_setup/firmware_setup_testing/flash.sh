#!/bin/bash

# Erase flash on first ESP32S3
esptool.py --chip esp32s3 --port /dev/tty.usbmodem1101 erase_flash

# Flash firmware to second ESP32S3
esptool.py --chip esp32s3 --port /dev/tty.usbmodem1101 --baud 460800 write_flash -z 0x0 /Users/nicokofi/Documents/GitHub/AI_managment/xiao_setup/firmware_setup_testing/firmware.bin