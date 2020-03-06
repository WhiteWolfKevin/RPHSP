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
import time

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

def print_key(key):

    # Grab the global counter variable to display code entry correctly
    global counter

    # Clear the line and reset the counter if 6 digits have been entered
    if (counter == 6):
        mylcd.lcd_display_string("                    ", 2)
        counter = 0



    mylcd.lcd_display_string_pos(str(key), 2, (6 + counter))
    counter += 1
# -------------------------------------------Keypad Configuration

# Global Variables
alarmSoundLocation = "/home/pi/RPHSP/alarm.mp3"

# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM)

# Set LCD Settings
mylcd = i2c_driver.LCD()

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
    while True:

        # Variables
        securityBreach = False
        global alarmArmed

        # Print alarm status
        if (alarmArmed):
            print("Alarm Status: Armed")
        else:
            print("Alarm Status: Disarmed")

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

    mylcd.lcd_display_string("Enter Passcode:", 1)

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

# Main Function
try:
    os.system('clear')

    securitySystemRunning = threading.Thread(target=securitySystem)
    securitySystemRunning.daemon = True
    securitySystemRunning.start()

    armingSystemRunning = threading.Thread(target=controlPanel)
    armingSystemRunning.daemon = True
    armingSystemRunning.start()

    while True:
        # Keep Running Application
        print("Starting sleep...")
        time.sleep(2)

except KeyboardInterrupt:
    print("Goodbye")

finally:
    keypad.cleanup()
    mylcd.lcd_clear()
    mylcd.backlight(0)
