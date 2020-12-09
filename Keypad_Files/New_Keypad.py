#!/usr/bin/env python

# ==================================================================
# Imports
# ==================================================================

# Imports for system functions
import RPi.GPIO as GPIO
import os
import time
import threading

# Imports for LCD Screen
import i2c_driver

# Imports for Keypad
from pad4pi import rpi_gpio

# Imports for RFID
from pirc522 import RFID

# Imports for interacting with web interface
import requests

# ==================================================================
# Functions and Configurations
# ==================================================================

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

# Variable to hold the duration of the backlight timer
backlightTimerDuration = 30

# Configure GPIO pins to use Broadcom numbering
GPIO.setmode(GPIO.BCM)

# ==================
# LED Functions
# ==================

# Configure the pins for LED feedback and turn them off to start
GPIO.setup(6,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.output(6,0)
GPIO.output(12,0)

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

# Function for error LED feedback
def errorLED():
    for i in range(5):
        GPIO.output(6,1)
        time.sleep(0.2)
        GPIO.output(6,0)
        GPIO.output(12,1)
        time.sleep(0.2)
        GPIO.output(12,0)

# ==================
# Buzzer Functions
# ==================

# Configure the pins for the Buzzer output and turn it off to start
GPIO.setup(21,GPIO.OUT)
GPIO.output(21,0)

# Function for Buzzer Button Output
def buzzerButton():
    GPIO.output(21,1)
    time.sleep(0.2)
    GPIO.output(21,0)

# Function for Buzzer Access Denied Output
def accessDeniedBuzzer():
    GPIO.output(21,1)
    time.sleep(1)
    GPIO.output(21,0)

# Function for Buzzer Alarm Output
def errorBuzzer():
    for i in range(5):
        GPIO.output(21,1)
        time.sleep(0.2)
        GPIO.output(21,0)
        time.sleep(0.2)

# ==================
# LCD Screen Functions
# ==================
def accessDeniedLCDDisplay():
    lcd.updateLCDScreen("Access Denied", 2)
    time.sleep(1)
    lcd.updateLCDScreen("                    ", 2)

def accessGrantedLCDDisplay():
    lcd.updateLCDScreen("Access Granted", 2)
    time.sleep(1)
    lcd.updateLCDScreen("                    ", 2)

# ==================
# Access Configurations
# ==================
def accessDenied():
    # Run the functions that correspond to an accessDenied event
    accessDeniedLCDDisplayRun = threading.Thread(target=accessDeniedLCDDisplay)
    accessDeniedLEDRun = threading.Thread(target=accessDeniedLED)
    accessDeniedBuzzerRun = threading.Thread(target=accessDeniedBuzzer)
    accessDeniedLCDDisplayRun.start()
    accessDeniedLEDRun.start()
    accessDeniedBuzzerRun.start()
    # Sleep for 1 second while the accessDenied function finish
    time.sleep(1)

def accessGranted():

    # Grab the variable for the alarmStatus
    global alarmStatus

    if (alarmStatus == "Disarmed"):
        i = 3
        while (i > 0):
            # Make the buzzer sound
            buzzerButtonSound = threading.Thread(target=buzzerButton)
            buzzerButtonSound.start()

            # Reset the backlight timer so it doesn't go out
            backlightTimer = backlightTimerDuration

            # Display the time left until the system is armed
            print("Time to arm: " + str(i))
            lcd.updateLCDScreen("Arming in: " + str(i), 2)
            i = i - 1
            time.sleep(1)
        lcd.updateLCDScreen("SYSTEM IS ARMED", 2)
        time.sleep(2)
        lcd.updateLCDScreen("                    ", 2)
    elif (alarmStatus == "Armed"):
        print("This is where I need to disarm the system")

# Function to handle keypad presses
def keyPress(key):

    # Reset backlight timer
    global backlightTimer
    backlightTimer = backlightTimerDuration
    lcd.backlight("On")

    # Make the buzzer sound
    buzzerButtonSound = threading.Thread(target=buzzerButton)
    buzzerButtonSound.start()

    # Grab the global keypressCounter variable to display code entry correctly
    global keypressCounter

    # Grab the global string variable to hold the entered key
    global userEntry

    # Do stuff depending on what key was pressed
    if (key == "#"):

        # Run error functions if the entry is blank
        if (userEntry == ""):

            # Display the error LEDs
            errorLEDDisplay = threading.Thread(target=errorLED)
            errorLEDDisplay.start()

            # Sound the error buzzer
            errorBuzzerSound = threading.Thread(target=errorBuzzer)
            errorBuzzerSound.start()
            time.sleep(2)
        else:
            # Check if the entered code is correct
            result = requests.get("http://192.168.1.125/webinterface/confirm_user_entry.php?pin_code=" + userEntry).content

            print("Result: " + result)

            if (result == "Access Denied"):
                accessDenied()
            elif (result == "Access Granted"):
                accessGranted()

        # Clear the code that was entered
        lcd.updateLCDScreen("Passcode:[      ]", 1)
        keypressCounter = 0

        # Clear User Code
        userEntry = ""

    elif (key == "*"):
        lcd.updateLCDScreen("Passcode:[      ]", 1)
        lcd.updateLCDScreen("                    ", 2)
        keypressCounter = 0

        # Clear User Code
        userEntry = ""
    elif (keypressCounter == 6):
        # Reset user code with pressed key
        userEntry = str(key)

        lcd.updateLCDScreen("Passcode:[      ]", 1)
        lcd.updateLCDScreenLine("*", 1, 10)
        keypressCounter = 1
    else:
        # Add pressed key
        userEntry = userEntry + str(key)

        lcd.updateLCDScreenLine("*", 1, (10 + keypressCounter))
        keypressCounter += 1

def backlightCountdown():
    global backlightTimer
    while True:
        while (backlightTimer > 0):
            backlightTimer = backlightTimer - 1
            time.sleep(1)

        if (backlightTimer == 0):
            lcd.backlight("Off")
            backlightTimer = -1

        if (backlightTimer == -1):
            time.sleep(1)

def controlPanel():
    # Keypad configuration
    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
    keypad.registerKeyPressHandler(keyPress)

    # Set the LCD to the default display
    lcd.updateLCDScreen("Passcode:[      ]", 1)
    lcd.updateLCDScreen("Clear:*   Submit:#", 4)

    previousAlarmStatus = ""

    global backlightTimer

    while True:
        alarmStatus = "ARMED"

        if (alarmStatus != previousAlarmStatus):
            previousAlarmStatus = alarmStatus
            lcd.updateLCDScreen("                    ", 3)
            lcd.updateLCDScreen("Alarm: " + str(alarmStatus), 3)
            backlightTimer = backlightTimerDuration

        time.sleep(1)

def rfidReader():
    #rdr = RFID()s
    rdr = RFID(pin_rst=25, pin_irq=24, pin_mode=GPIO.BCM)
    util = rdr.util()

    # Set util debug to true - it will print what's going on
    util.debug = True

    while True:
        # Wait for tag
        rdr.wait_for_tag()

        # Request tag
        (error, data) = rdr.request()
        if not error:
            print("Detected")

            (error, uid) = rdr.anticoll()
            if not error:

                # Reset backlight timer
                global backlightTimer
                backlightTimer = backlightTimerDuration
                lcd.backlight("On")

                # Print UID
                print("UID in Dec: " + str(uid))

                uidInHex = []
                uidInString = ""
                for field in uid:
                    uidInHex.append('%02x' % (field))
                    uidInString += ('%02x' % (field))

                print("UID in Hex: " + str(uidInHex))
                print("UID in Str: " + uidInString)

                result = "Access Denied"

                # We must stop crypto
                util.deauth()
                print("")
        time.sleep(1)

# ==================================================================
# Main Function
# ==================================================================
try:

    # Set the default backlight time and create the lock to be used by the LCD screen
    backlightTimer = backlightTimerDuration
    updateLCDLock = threading.Lock()

    # Initialize LCD object, turn the LCD screen on, create the LCD lock object, and set the backlight timer
    lcd = i2c_driver.LCD(updateLCDLock)
    lcd.backlight("On")

    controlPanelRunning = threading.Thread(target=controlPanel)
    controlPanelRunning.daemon = True
    controlPanelRunning.start()

    backlightCountdownRunning = threading.Thread(target=backlightCountdown)
    backlightCountdownRunning.daemon = True
    backlightCountdownRunning.start()

    rfidReaderRunning = threading.Thread(target=rfidReader)
    rfidReaderRunning.daemon = True
    rfidReaderRunning.start()

    while True:
        # Keep Running Application
        time.sleep(2)

except KeyboardInterrupt:
    lcd.lcd_clear()
    lcd.backlight("Off")
    GPIO.cleanup()
