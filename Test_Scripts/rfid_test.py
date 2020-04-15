#!/usr/bin/env python

from pirc522 import RFID
import signal
import time
import RPi.GPIO as GPIO
import os
import requests

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

                req = requests.get("http://192.168.1.125/webinterface/keypad_auth.php?rfid_card_number=" + uidInString)

                print(req.content)

                # We must stop crypto
                util.deauth()
                print("")

        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
