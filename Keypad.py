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
import requests

# Import to provide IP address to keypad_auth.php
import netifaces as ni

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

# Configure the pins for LED feedback and turn them off to start
GPIO.setmode(GPIO.BCM)
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
    GPIO.output(6,1)
    time.sleep(0.2)
    GPIO.output(6,0)
    GPIO.output(12,1)
    time.sleep(0.2)
    GPIO.output(12,0)
    GPIO.output(6,1)
    time.sleep(0.2)
    GPIO.output(6,0)
    GPIO.output(12,1)
    time.sleep(0.2)
    GPIO.output(12,0)
    GPIO.output(6,1)
    time.sleep(0.2)
    GPIO.output(6,0)
    GPIO.output(12,1)
    time.sleep(0.2)
    GPIO.output(12,0)

# Configure the pins for the Buzzer output and turn it off to start
GPIO.setup(21,GPIO.OUT)
GPIO.output(21,0)

# Function for Buzzer Button Output
def buzzerButton():
    GPIO.output(21,1)
    time.sleep(0.05)
    GPIO.output(21,0)

# Function for Buzzer Alarm Output
def buzzerAlarm():
    for i in range(10):
        GPIO.output(21,1)
        time.sleep(0.5)
        GPIO.output(21,0)
        time.sleep(0.5)



# Function to handle if an access attempt was requested
def accessAttempt(result):
    if (result == "Access Granted"):
        lcd.updateLCDScr
        een(result, 2)
        accessGrantedLED()
        time.sleep(1)
        lcd.updateLCDScreen("                    ", 2)
    elif (result == "Access Denied"):
        lcd.updateLCDScreen(result, 2)
        accessDeniedLED()
        time.sleep(1)
        lcd.updateLCDScreen("                    ", 2)
    else:
        lcd.updateLCDScreen(result, 2)
        errorLED()
        time.sleep(1)
        lcd.updateLCDScreen("                    ", 2)

# Send a request to the web interface via a GET request
def securitySystemRequest(url):
    try:
        return requests.get("http://192.168.1.125/webinterface/" + url).content
    except:
        return "ERROR CONN..."

# Function to get the IP address of the keypad
def keypadIPAddress():
    try:
        return "&keypad_ip_address=" + ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    except:
        return("IP UNAVL")

# Function to handle keypad presses
def keyPress(key):

    # Reset backlight timer
    global backlightTimer
    backlightTimer = backlightTimerDuration
    lcd.backlight("On")

    # Make Buzzer Sound
    buzzerButton()

    # Grab the global keypressCounter variable to display code entry correctly
    global keypressCounter

    # Grab the global string variable to hold the entered key
    global userEntry

    # Do stuff depending on what key was pressed
    if (key == "#"):

        result = securitySystemRequest("keypad_auth.php?pin_code=" + userEntry)

        # Added the empty userEntry check as a quick test of error LEDs
        if (userEntry == ""):
            buzzerAlarm()
            errorLED()
            time.sleep(1)
        else:
            accessAttempt(result)

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
        alarmStatus = securitySystemRequest("alarm_status.php")

        if (alarmStatus != previousAlarmStatus):
            previousAlarmStatus = alarmStatus
            lcd.updateLCDScreen("                    ", 3)
            lcd.updateLCDScreen("Alarm: " + str(alarmStatus), 3)
            backlightTimer = backlightTimerDuration

        time.sleep(1)

        print("Backlight Timer: " + str(backlightTimer))

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

                result = securitySystemRequest("keypad_auth.php?rfid_card_number=" + uidInString)

                accessAttempt(result)

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
