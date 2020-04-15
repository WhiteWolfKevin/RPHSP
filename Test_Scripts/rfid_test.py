#!/usr/bin/env python

from pirc522 import RFID
import signal
import time
import RPi.GPIO as GPIO
import os

rdr = RFID()
util = rdr.util()

# Set util debug to true - it will print what's going on
util.debug = True

try:

    os.system('clear')

    print("Starting...")

    while True:
        # Wait for tag
        rdr.wait_for_tag()

        # Request tag
        (error, data) = rdr.request()
        if not error:
            print("Detected")

            (error, uid) = rdr.anticoll()
            if not error:
                # Print UID
                print("UID in Dec: " + str(uid))

                uidInHex = []
                uidInString = ""
                for field in uid:
                    uidInHex.append('%02x' % (field))
                    uidInString += ('%02x' % (field))

                print("UID in Hex: " + str(uidInHex))
                print("UID in Str: " + uidInString)

                if (uidInString == "4a1a560f09"):
                    print("This card belongs to Kevin")
                elif (uidInString == "5a82d2212b"):
                    print("This card belongs to Scrap")
                elif (uidInString == "5a50bf2194"):
                    print("This card belongs to Abby")
                else:
                    print("Unknown Card")

                # We must stop crypto
                util.deauth()
                print("")

        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
