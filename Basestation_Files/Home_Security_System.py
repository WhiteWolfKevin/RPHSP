#!/usr/bin/env python

# Imports for Original Security System
import RPi.GPIO as GPIO
import time
import os
import pygame
import threading
import mysql.connector as mariadb

# Global Variables
alarmSoundLocation = "/home/pi/RPHSP/Basestation_Files/alarm.mp3"

# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM)

# Door Sensor class
class magneticSensor:
    def __init__(self, gpioPin, previousStatus):
        self.gpioPin = gpioPin
        self.previousStatus = previousStatus

# MariaDB server configuration
mariadb_connection = mariadb.connect(host='piserver', user='rphsp', password='password', database='rphsp')
database = mariadb_connection.cursor()

database.execute("select gpio_pin, status from sensors")

sensors = []
for item in database:
    sensors.append(magneticSensor(item[0], item[1]))
    GPIO.setup(item[0], GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Audio player settings
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

# Security System Thread
def securitySystem():

    rounds = 0

    while True:

        # Grab Alarm Status from MariaDB server
        database.execute("select status from alarms where id = 1")
        result = database.fetchone()
        alarmStatus = result[0]
        print("alarmStatus = " + alarmStatus)

        # Troubleshooting
        print("Rounds=" + rounds)
        rounds+=1

        # Variables
        securityBreach = False

        # Check each sensor for a security breach
        for sensor in sensors:
            if (GPIO.input(sensor.gpioPin)):
                # Door/Window is open
                securityBreach = True
                if (sensor.previousStatus != "OPEN"):
                    database.execute("update sensors set status = 'OPEN' where gpio_pin = " + str(sensor.gpioPin))
                    mariadb_connection.commit()
                    sensor.previousStatus = "OPEN"
                print(str(sensor.gpioPin) + " Status: OPEN - WARNING!!!")
            else:
                # Door/Window is closed
                if (sensor.previousStatus != "CLOSED"):
                    database.execute("update sensors set status = 'CLOSED' where gpio_pin = " + str(sensor.gpioPin))
                    mariadb_connection.commit()
                    sensor.previousStatus = "CLOSED"
                print(str(sensor.gpioPin) + " Status: CLOSED")

        if (securityBreach and alarmStatus == "ARMED"):
            if (not pygame.mixer.music.get_busy()):
                pygame.mixer.music.load(alarmSoundLocation)
                pygame.mixer.music.play(-1)
        else:
            if (pygame.mixer.music.get_busy()):
                pygame.mixer.music.stop()

        # Time delay
        time.sleep(1)
        os.system('clear')

# Main Function
try:
    securitySystemRunning = threading.Thread(target=securitySystem)
    securitySystemRunning.daemon = True
    securitySystemRunning.start()

    while True:
        # Keep Running Application
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
