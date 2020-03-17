#!/usr/bin/env python

# Imports for Original Security System
import RPi.GPIO as GPIO
import time
import sys
import signal
import os
import pygame
import threading

# Global Variables
alarmSoundLocation = "/home/pi/RPHSP/alarm.mp3"

# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM)

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

# Main Function
try:
    os.system('clear')

    securitySystemRunning = threading.Thread(target=securitySystem)
    securitySystemRunning.daemon = True
    securitySystemRunning.start()

    while True:
        # Keep Running Application
        print("Starting sleep...")
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
