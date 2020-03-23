#!/usr/bin/env python

# Imports for system functions
import RPi.GPIO as GPIO
import os
import time
import threading

# Import for Redis
import redis

# Imports for LCD Screen
import i2c_driver

# Set LCD Settings
mylcd = i2c_driver.LCD()
mylcd.backlight(1)

# Imports for keypad
from pad4pi import rpi_gpio

# LED Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.output(6,0)
GPIO.output(12,0)

def accessGrantedLED():
    GPIO.output(12,1)
    time.sleep(1)
    GPIO.output(12,0)

def accessDeniedLED():
    GPIO.output(6,1)
    time.sleep(1)
    GPIO.output(6,0)

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

    # Reset backlight timer
    global backlightTimer
    backlightTimer = 10
    mylcd.backlight(1)

    # Grab the global counter variable to display code entry correctly
    global counter

    # Grab the global string variable to hold the entered key
    global userEntry

    # Correct Keycode
    correctKeys = ["123456", "111111", "999999"]

    # Do stuff depending on what key was pressed
    if (key == "#"):

        for correctKey in correctKeys:
            if (userEntry == correctKey):
                mylcd.lcd_display_string("Passcode Correct!", 2)
                accessGrantedLED()
                time.sleep(1)
                mylcd.lcd_display_string("                    ", 2)

                if (redisServer.get("alarmStatus") == "Armed"):
                    redisServer.set("alarmStatus", "Disarmed")
                elif (redisServer.get("alarmStatus") == "Disarmed"):
                    redisServer.set("alarmStatus", "Armed")
                else:
                    redisServer.set("alarmStatus", "Disarmed")

                # Break out of the for loop
                keyNotFound = False
                break

            else:
                keyNotFound = True

        if (keyNotFound):
            mylcd.lcd_display_string("Incorrect Passcode!", 2)
            accessDeniedLED()
            time.sleep(1)
            mylcd.lcd_display_string("                    ", 2)

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
        # mylcd.lcd_display_string_pos(str(key), 1, 10)
        mylcd.lcd_display_string_pos("*", 1, 10)
        counter = 1
    else:
        # Add pressed key
        userEntry = userEntry + str(key)

        # mylcd.lcd_display_string_pos(str(key), 1, (10 + counter))
        mylcd.lcd_display_string_pos("*", 1, (10 + counter))
        counter += 1

# Redis server configuration
redisServer = redis.Redis(host='piserver', port=6379, db=0)

# Backlight timer
backlightTimer = 10

def backlightCountdown():
    global backlightTimer
    while True:
        while (backlightTimer > 0):
            backlightTimer = backlightTimer - 1
            time.sleep(1)

        mylcd.backlight(0)


def controlPanel():
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

        alarmStatus = redisServer.get("alarmStatus")
        print("Alarm Status: " +  str(alarmStatus))

        if (alarmStatus != previousAlarmStatus):
            previousAlarmStatus = alarmStatus
            mylcd.lcd_display_string("                    ", 3)
            mylcd.lcd_display_string("Alarm: " + str(alarmStatus), 3)

        time.sleep(1)

        global backlightTimer
        print("Backlight Timer: " + str(backlightTimer))

# Main Function
try:
    controlPanelRunning = threading.Thread(target=controlPanel)
    controlPanelRunning.daemon = True
    controlPanelRunning.start()

    backlightCountdownRunning = threading.Thread(target=backlightCountdown)
    backlightCountdownRunning.daemon = True
    backlightCountdownRunning.start()

    while True:
        # Keep Running Application
        time.sleep(2)

except KeyboardInterrupt:

    mylcd.lcd_clear()
    mylcd.backlight(0)
    GPIO.cleanup()
