import RPi.GPIO as GPIO
import threading
import time
import sys
import signal
import os
import pygame

# Global Variables
alarmSoundLocation = "/home/pi/RaspberryPiHomeSecurityProject/RPHSP/alarm.mp3"

# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM)

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

#Create array of sensors
sensors = []
sensors.append(doorSensor("Front Door", 16))
sensors.append(doorSensor("Back Door", 26))
sensors.append(doorSensor("Garage Door", 20))
sensors.append(doorSensor("Basement Door", 21))

# Set up the door sensor pins.
for sensor in sensors:
    GPIO.setup(sensor.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Audio player settings
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)

# Create Threads
def securitySystem():
    securityCompromised = False
    while True:
        # Loop through each sensor and update its states
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

        #Time delay
        time.sleep(0.5)

def controlPanel():
    userResponse = raw_input("Would you like to do something? (y/n): ")

# Main Function
os.system('clear')

securitySystemRunning = threading.Thread(target=securitySystem)
securitySystemRunning.daemon = True
securitySystemRunning.start()

userInputRunning = threading.Thread(target=controlPanel)
userInputRunning.daemon = True
userInputRunning.start()

while True:
    print "Program is running"
    time.sleep(2)
