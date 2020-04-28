#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import mysql.connector as mariadb

GPIO.setmode(GPIO.BCM)

# MariaDB server configuration
mariadb_connection = mariadb.connect(host='piserver', user='rphsp', password='password', database='rphsp')
database = mariadb_connection.cursor()


# init list with pin numbers
pinList = [4, 17, 22, 27]

# loop through pins and set mode and state to 'high'
for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

try:

    while True:
        for pin in pinList:
            database.execute("select status from relay_pins where relay_id = 1 and relay_pin = " + str(pin))
            result = database.fetchone()
            relayStatus = result[0]

            print("Relay Pin " + str(pin) + ": " + relayStatus)

            if (relayStatus == "ON"):
                GPIO.output(pin, GPIO.LOW)
            elif (relayStatus == "OFF"):
                GPIO.output(pin, GPIO.HIGH)

            mariadb_connection.commit()

        time.sleep(0.2)


# End program cleanly with keyboard
except KeyboardInterrupt:
  print ("  Quit")

  # Reset GPIO settings
  GPIO.cleanup()
