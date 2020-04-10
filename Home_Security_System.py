#!/usr/bin/env python

# Imports for Original Security System
import RPi.GPIO as GPIO
import time
import os
import pygame
import threading
import mysql.connector as mariadb

# Global Variables
alarmSoundLocation = "/home/pi/RPHSP/alarm.mp3"

# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM)

# MariaDB server configuration
mariadb_connection = mariadb.connect(host='piserver', user='rphsp', database='rphsp')
database = mariadb_connection.cursor()

database.execute("select gpio_pin from sensors")

sensors = []
for gpio_pin in database:
    sensors.append(gpio_pin[0])

for sensor in sensors:
    print(sensor)
    GPIO.setup(sensor, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Audio player settings
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

# Security System Thread
def securitySystem():

    while True:

        # Grab Alarm Status from Redis server
        alarmStatus = "Armed"

        # Variables
        securityBreach = False

        # Print alarm status
        print(alarmStatus)

        # Check each sensor for a security breach
        for sensor in sensors:
            currentState = GPIO.input(sensor)
            if (currentState):
                # This means the door/window is open
                securityBreach = True
                print(str(sensor) + " Status: OPEN - WARNING!!!")
            else:
                print(str(sensor) + " Status: CLOSED")

        if (securityBreach and alarmStatus == "Armed"):
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

    securitySystemRunning = threading.Thread(target=securitySystem)
    securitySystemRunning.daemon = True
    securitySystemRunning.start()

    while True:
        # Keep Running Application
        print("Starting sleep...")
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
