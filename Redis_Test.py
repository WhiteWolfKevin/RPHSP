#!/usr/bin/env python

# Imports for system functions
import RPi.GPIO as GPIO
import os
import time

# Import for Redis
import redis

# Imports for LCD Screen
import i2c_driver

# Set LCD Settings
mylcd = i2c_driver.LCD()
mylcd.backlight(1)

# Imports for keypad
from pad4pi import rpi_gpio

# -------------------------------------------Keypad Configuration
KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

ROW_PINS = [15, 22, 27, 13] # BCM numbering
COL_PINS = [18, 14, 17] # BCM numbering

# Counter used to space the input
counter = 0

# String used to hold the entered code
userEntry = ""

# -------------------------------------------Keypad Configuration

def print_key(key):

    # Grab the global counter variable to display code entry correctly
    global counter

    # Grab the global string variable to hold the entered key
    global userEntry

    # Correct Keycode
    correctKey = "123456"

    # Do stuff depending on what key was pressed
    if (key == "#"):

        if (userEntry == correctKey):

            if (r.get("alarmStatus") == "Armed"):
                r.set("alarmStatus", "Disarmed")
            elif (r.get("alarmStatus") == "Disarmed"):
                r.set("alarmStatus", "Armed")
            else:
                r.set("alarmStatus", "Disarmed")

            mylcd.lcd_display_string("                    ", 2)
            mylcd.lcd_display_string("Passcode Correct!", 2)

        else:
            mylcd.lcd_display_string("                    ", 2)
            mylcd.lcd_display_string("Incorrect Passcode!", 2)

        mylcd.lcd_display_string("Passcode:[      ]", 1)
        counter = 0

        # Clear User Code
        userEntry = ""

    elif (key == "*"):
        mylcd.lcd_display_string("Passcode:[      ]", 1)
        mylcd.lcd_display_string("                    ", 2)
        counter = 0

        # Clear User Code
        userEntry = ""
    elif (counter == 6):
        # Reset user code with pressed key
        userEntry = str(key)

        mylcd.lcd_display_string("Passcode:[      ]", 1)
        mylcd.lcd_display_string_pos(str(key), 1, 10)
        counter = 1
    else:
        # Add pressed key
        userEntry = userEntry + str(key)

        mylcd.lcd_display_string_pos(str(key), 1, (10 + counter))
        counter += 1





# Redis server configuration
r = redis.Redis(host='localhost', port=6379, db=0)

# Main Function
try:
    os.system('clear')

    # Keypad configuration
    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
    keypad.registerKeyPressHandler(print_key)

    # Set the LCD to the default display
    mylcd.lcd_display_string("Passcode:[      ]", 1)
    mylcd.lcd_display_string("Clear:*   Submit:#", 4)

    previousAlarmStatus = ""

    while True:

        alarmStatus = r.get("alarmStatus")
        print("Alarm Status: " + alarmStatus)

        if (alarmStatus != previousAlarmStatus):
            previousAlarmStatus = alarmStatus
            mylcd.lcd_display_string("                    ", 3)
            mylcd.lcd_display_string("Alarm: " + str(alarmStatus), 3)

        time.sleep(3)

except KeyboardInterrupt:
    mylcd.lcd_clear()
    mylcd.backlight(0)
    GPIO.cleanup()
