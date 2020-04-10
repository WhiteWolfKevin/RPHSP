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

# MariaDB server configuration
mariadb_connection = mariadb.connect(host='piserver' user='rphsp', database='rphsp')
database = mariadb_connection.cursor()

# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM)

# Get all GPIO pins for the sensors
database.execute("select gpio_pin from sensors")
for gpio_pin in database:
    print("GPIO Pin: " + gpio_pin)
    GPIO.setup(gpio_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Audio player settings
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

# # Security System Thread
# def securitySystem():
#
#     while True:
#
#         # Grab Alarm Status from Redis server
#         alarmStatus = redisServer.get("alarmStatus")
#
#         # Variables
#         securityBreach = False
#
#         # Print alarm status
#         print(alarmStatus)
#
#         # Check each sensor for a security breach
#         for sensor in sensors:
#             sensor.currentState = GPIO.input(sensor.pin)
#             if (sensor.currentState):
#                 # This means the door/window is open
#                 securityBreach = True
#                 print(sensor.name + " Status: OPEN - WARNING!!!")
#                 redisServer.set(sensor.name, "OPEN - WARNING!!!")
#             else:
#                 print(sensor.name + " Status: CLOSED")
#                 redisServer.set(sensor.name, "CLOSED")
#
#         if (securityBreach and alarmStatus == "Armed"):
#             if (not pygame.mixer.music.get_busy()):
#                 pygame.mixer.music.load(alarmSoundLocation)
#                 pygame.mixer.music.play(-1)
#         else:
#             if (pygame.mixer.music.get_busy()):
#                 pygame.mixer.music.stop()
#
#         # Time delay
#         time.sleep(2)
#         os.system('clear')
#
# # Main Function
# try:
#
#     securitySystemRunning = threading.Thread(target=securitySystem)
#     securitySystemRunning.daemon = True
#     securitySystemRunning.start()
#
#     while True:
#         # Keep Running Application
#         print("Starting sleep...")
#         time.sleep(2)
#
# except KeyboardInterrupt:
#     GPIO.cleanup()
