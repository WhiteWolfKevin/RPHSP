#!/usr/bin/python
from pad4pi import rpi_gpio

KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

ROW_PINS = [14, 15, 18, 13] # BCM numbering
COL_PINS = [17, 27, 22] # BCM numbering

def print_key(key):
    print(key)

try:
    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
    keypad.registerKeyPressHandler(print_key)

    print("Press buttons on your keypad. Ctrl+C to exit.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Goodbye")
finally:
    keypad.cleanup()
