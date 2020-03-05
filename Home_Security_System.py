#!/usr/bin/env python

# Imports for Original Security System
import RPi.GPIO as GPIO
import time
import sys
import signal
import os
import pygame

# Imports for LCD Screen
import i2c_driver
import time

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
        self.status = "null"
        self.currentState = True
        self.previousState = True

    def display_output(self):
        print(self.name + " Status: " + self.status)

    def get_string(self):
        doorSensorString = self.name + " Status: " + self.status
        print(doorSensorString)
        return doorSensorString

# Create array of sensors
sensors = []
sensors.append(doorSensor("Front Door", 16))
sensors.append(doorSensor("Back Door", 26))
sensors.append(doorSensor("Garage Door", 20))
sensors.append(doorSensor("Basement Door", 21))

# Set up the door sensor pins.
for sensor in sensors:
    GPIO.setup(sensor.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Variables
securityCompromised = False
alarmSystemArmed = False

# Audio player settings
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

# Main Function
os.system('clear')

try:
    while True:
        for sensor in sensors:
            sensor.currentState = GPIO.input(sensor.pin)
            if (sensor.currentState):
                securityCompromised = True
                if (not pygame.mixer.music.get_busy()):
                    pygame.mixer.music.load(alarmSoundLocation)
                    pygame.mixer.music.play(-1)
                if (sensor.currentState != sensor.previousState):
                    sensor.status = "Open"
                    sensor.previousState = sensor.currentState
            elif (sensor.currentState != sensor.previousState):
                sensor.status = "Closed"
                sensor.previousState = sensor.currentState

            sensor.display_output()
            mylcd.lcd_display_string(sensor.get_string(), 1)

        # If there has been a compromise, display the compromised locations
        if (securityCompromised):
            print("")
            print("")
            for sensor in sensors:
                if (sensor.currentState):
                    print("WARNING: " + sensor.name + " is currently open!")
            securityCompromised = False
        else:
            if (pygame.mixer.music.get_busy()):
                pygame.mixer.music.stop()

        # Time delay
        time.sleep(2)

except KeyboardInterrupt:
    print("Goodbye")
