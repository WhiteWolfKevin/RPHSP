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

# Imports for Keypad
from pad4pi import rpi_gpio

# Initialize LCD object, turn the LCD screen on, and create the LCD lock object
mylcd = i2c_driver.LCD()
mylcd.backlight(1)
updateLCDLock = threading.Lock()

# Configure Keypad Buttons
KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

# Define pins used for Keypad, create variable for keypress counting, and create empty variable for keycode entry
ROW_PINS = [15, 22, 27, 13]
COL_PINS = [18, 14, 17]
keypressCounter = 0
userEntry = ""

# Redis server configuration
redisServer = redis.Redis(host='piserver', port=6379, db=0)

# Create timer variable for the backlight timer
backlightTimer = 10

# Configure the pins for LED feedback and turn them off to start
GPIO.setmode(GPIO.BCM)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.output(6,0)
GPIO.output(12,0)

# LCD class that contains functions to update the LCD screen
class LCD():
    @staticmethod
    def updateLCDScreen(text, line):
        updateLCDLock.acquire()
        mylcd.lcd_display_string(text, line)
        updateLCDLock.release()

    @staticmethod
    def updateLCDScreenLine(text, line, position):
        updateLCDLock.acquire()
        mylcd.lcd_display_string_pos(text, line, position)
        updateLCDLock.release()

# Function for access granted LED feedback
def accessGrantedLED():
    GPIO.output(12,1)
    time.sleep(1)
    GPIO.output(12,0)

# Function for access denied LED feedback
def accessDeniedLED():
    GPIO.output(6,1)
    time.sleep(1)
    GPIO.output(6,0)

# Function to handle keypad presses
def keyPress(key):

    # Reset backlight timer
    global backlightTimer
    backlightTimer = 10
    mylcd.backlight(1)

    # Grab the global keypressCounter variable to display code entry correctly
    global keypressCounter

    # Grab the global string variable to hold the entered key
    global userEntry

    # Correct Keycode
    correctKeys = ["123456", "111111", "999999"]

    # Do stuff depending on what key was pressed
    if (key == "#"):

        for correctKey in correctKeys:
            if (userEntry == correctKey):
                LCD.updateLCDScreen("Passcode Correct!", 2)
                accessGrantedLED()
                time.sleep(1)
                LCD.updateLCDScreen("                    ", 2)

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
            LCD.updateLCDScreen("Incorrect Passcode!", 2)
            accessDeniedLED()
            time.sleep(1)
            LCD.updateLCDScreen("                    ", 2)

        LCD.updateLCDScreen("Passcode:[      ]", 1)
        keypressCounter = 0

        # Clear User Code
        userEntry = ""

    elif (key == "*"):
        LCD.updateLCDScreen("Passcode:[      ]", 1)
        LCD.updateLCDScreen("                    ", 2)
        keypressCounter = 0

        # Clear User Code
        userEntry = ""
    elif (keypressCounter == 6):
        # Reset user code with pressed key
        userEntry = str(key)

        LCD.updateLCDScreen("Passcode:[      ]", 1)
        LCD.updateLCDScreenLine("*", 1, 10)
        keypressCounter = 1
    else:
        # Add pressed key
        userEntry = userEntry + str(key)

        LCD.updateLCDScreenLine("*", 1, (10 + keypressCounter))
        keypressCounter += 1

def backlightCountdown():
    global backlightTimer
    while True:
        while (backlightTimer > 0):
            backlightTimer = backlightTimer - 1
            time.sleep(1)

        if (backlightTimer == 0):
            mylcd.backlight(0)

def controlPanel():
    # Keypad configuration
    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
    keypad.registerKeyPressHandler(keyPress)

    # Set the LCD to the default display
    LCD.updateLCDScreen("Passcode:[      ]", 1)
    LCD.updateLCDScreen("Clear:*   Submit:#", 4)

    previousAlarmStatus = ""

    while True:

        alarmStatus = redisServer.get("alarmStatus")
        print("Alarm Status: " +  str(alarmStatus))

        if (alarmStatus != previousAlarmStatus):
            previousAlarmStatus = alarmStatus
            LCD.updateLCDScreen("                    ", 3)
            LCD.updateLCDScreen("Alarm: " + str(alarmStatus), 3)

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
