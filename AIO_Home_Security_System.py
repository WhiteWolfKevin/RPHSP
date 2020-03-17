#!/usr/bin/env python

# Imports for Original Security System
import RPi.GPIO as GPIO
import time
import sys
import signal
import os
import pygame
import threading

# Imports for LCD Screen
import i2c_driver

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

# Global Variables
alarmSoundLocation = "/home/pi/RPHSP/alarm.mp3"

# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM)

# Set LCD Settings
mylcd = i2c_driver.LCD()
mylcd.backlight(1)

# Door Sensor class
class doorSensor:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin

# Create array of sensors
sensors = []
sensors.append(doorSensor("Front Door", 16))
sensors.append(doorSensor("Living Room Window", 26))
sensors.append(doorSensor("Garage Door", 20))
sensors.append(doorSensor("Basement Door", 21))

# Set up the door sensor pins.
for sensor in sensors:
    GPIO.setup(sensor.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Audio player settings
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

# Global Variables
alarmArmed = False

# Security System Thread
def securitySystem():

    previousAlarmStatus = False

    while True:

        # Variables
        securityBreach = False
        global alarmArmed

        # Print alarm status
        if (alarmArmed):
            if (alarmArmed != previousAlarmStatus):
                print("Alarm Status: Armed")

            previousAlarmStatus = alarmArmed
        else:
            if (alarmArmed != previousAlarmStatus):
                print("Alarm Status: Disarmed")

        previousAlarmStatus = alarmArmed

        # Check each sensor for a security breach
        for sensor in sensors:
            sensor.currentState = GPIO.input(sensor.pin)
            if (sensor.currentState):
                # This means the door/window is open
                securityBreach = True
                print(sensor.name + " Status: OPEN - WARNING!!!")
            else:
                print(sensor.name + " Status: CLOSED")

        if (securityBreach and alarmArmed):
            if (not pygame.mixer.music.get_busy()):
                pygame.mixer.music.load(alarmSoundLocation)
                pygame.mixer.music.play(-1)
        else:
            if (pygame.mixer.music.get_busy()):
                pygame.mixer.music.stop()

        # Time delay
        time.sleep(2)
        os.system('clear')

# Arming/Disarming System Thread
def controlPanel():
    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
    keypad.registerKeyPressHandler(print_key)

    # Variables
    global alarmArmed

    while True:
        if (alarmArmed):
            userResponse = raw_input("Disarm the system? (y/n): ")
            if (userResponse == "y"):
                alarmArmed = False
        else:
            userResponse = raw_input("Arm the system? (y/n): ")
            if (userResponse == "y"):
                alarmArmed = True

def print_key(key):

    # Grab the global counter variable to display code entry correctly
    global counter

    # Grab the global string variable to hold the entered key
    global userEntry

    # Grab the global value for arming and disarming the system
    global alarmArmed

    # Correct Keycode
    correctKey = "123456"

    # Do stuff depending on what key was pressed
    if (key == "#"):

        if (userEntry == correctKey):
            mylcd.lcd_display_string("                    ", 2)
            mylcd.lcd_display_string("Passcode Correct!", 2)

            if (alarmArmed):
                alarmArmed = False
            elif (not alarmArmed):
                alarmArmed = True
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


# Main Function
try:
    os.system('clear')

    # Set the LCD to the default display
    mylcd.lcd_display_string("Passcode:[      ]", 1)
    mylcd.lcd_display_string("Alarm: Disarmed", 3)
    mylcd.lcd_display_string("Clear:*   Submit:#", 4)

    securitySystemRunning = threading.Thread(target=securitySystem)
    securitySystemRunning.daemon = True
    securitySystemRunning.start()

    controlPanelRunning = threading.Thread(target=controlPanel)
    controlPanelRunning.daemon = True
    controlPanelRunning.start()

    while True:
        # Keep Running Application
        print("Starting sleep...")
        time.sleep(2)

except KeyboardInterrupt:

    mylcd.lcd_clear()
    mylcd.backlight(0)
    GPIO.cleanup()
