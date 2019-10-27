#!/usr/bin/env python

import RPi.GPIO as GPIO
import sys
import time
from pirc522 import RFID

reader = RFID()

number = 0

print("Starting Program")

while True:
	print number
	number = number + 1
	reader.wait_for_tag()
	(error, tag_type) = reader.request()
	if not error:
		print("Tag detected")
		(error, uid) = reader.anticoll()
		if not error:
			print("UID: " + str(uid))
			# Select Tag is required before Auth
			if not reader.select_tag(uid):
				# Auth for block 10 (block 2 of sector 2) using default shipping key A
				if not reader.card_auth(reader.auth_a, 10, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], uid):
				  # This will print something like (False, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
				  print("Reading block 10: " + str(reader.read(10)))
				  # Always stop crypto1 when done working
				  reader.stop_crypto()

# Calls GPIO cleanup
reader.cleanup()
