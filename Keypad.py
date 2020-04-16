#!/usr/bin/env python

# Imports for system functions
import RPi.GPIO as GPIO
import os
import time
import threading
import mysql.connector as mariadb

# Imports for LCD Screen
import i2c_driver

# Imports for Keypad
from pad4pi import rpi_gpio

# Imports for RFID
from pirc522 import RFID
import requests

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

# MariaDB server configuration
mariadb_connection = mariadb.connect(host='piserver', user='rphsp', password='password', database='rphsp')

# Variable to hold the duration of the backlight timer
backlightTimerDuration = 30

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
    backlightTimer = backlightTimerDuration
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

                # Get the alarm status from MariaDB
                database = mariadb_connection.cursor()
                database.execute("select status from alarms where id = 1")
                result = database.fetchone()
                alarmStatus = result[0]

                if (alarmStatus == "ARMED"):
                    database.execute("update alarms set status = 'DISARMED' where id = 1")
                elif (alarmStatus == "DISARMED"):
                    database.execute("update alarms set status = 'ARMED' where id = 1")
                else:
                    database.execute("update alarms set status = 'DISARMED' where id = 1")
                mariadb_connection.commit()
                database.close()

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
            backlightTimer = -1

        if (backlightTimer == -1):
            time.sleep(1)

def controlPanel():
    # Keypad configuration
    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
    keypad.registerKeyPressHandler(keyPress)

    # Set the LCD to the default display
    LCD.updateLCDScreen("Passcode:[      ]", 1)
    LCD.updateLCDScreen("Clear:*   Submit:#", 4)

    previousAlarmStatus = ""

    database = mariadb_connection.cursor()
    while True:

        # Get the alarm status from MariaDB
        database.execute("select status from alarms where id = 1")
        result = database.fetchone()
        alarmStatus = result[0]
        print("Alarm Status: " +  alarmStatus)

        if (alarmStatus != previousAlarmStatus):
            previousAlarmStatus = alarmStatus
            LCD.updateLCDScreen("                    ", 3)
            LCD.updateLCDScreen("Alarm: " + str(alarmStatus), 3)

        time.sleep(1)

        global backlightTimer
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
                mylcd.backlight(1)

                # Print UID
                print("UID in Dec: " + str(uid))

                uidInHex = []
                uidInString = ""
                for field in uid:
                    uidInHex.append('%02x' % (field))
                    uidInString += ('%02x' % (field))

                print("UID in Hex: " + str(uidInHex))
                print("UID in Str: " + uidInString)

                req = requests.get("http://192.168.1.125/webinterface/keypad_auth.php?rfid_card_number=" + uidInString)

                print(req.content)

                # We must stop crypto
                util.deauth()
                print("")
        time.sleep(1)

# Main Function
try:

    # Initialize the backlight timer variable with the duration setting
    backlightTimer = backlightTimerDuration

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
    mylcd.lcd_clear()
    mylcd.backlight(0)
    GPIO.cleanup()
