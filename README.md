# Raspberry Pi Home Security Project
This is a project I've been working on to use Raspberry Pis as a whole home security system.

### Keypad Pi
**Required Packages**
```
pip install pi-rc522
pip install pad4pi
```

**12-Digit Keypad Configuration**
```
GPIO Pin Numbers
14,15,18,17,27,22,13

Left to right look at keypad 14,15,18,13,17,27,22
[Col 2] [row 1] [col 1] [row 4] [col 3] [row 3] [row 2]
COL [18, 14, 17]
ROW [15, 22, 27, 13]
```
```
* To adjust the key delay, go to this file and edit the "DEFAULT_KEY_DELAY" value
* Default value is 300
* A good value to set 150
/home/pi/.local/lib/python2.7/site-packages/pad4pi/rpi_gpio.py
```

**Keypad I2C LCD Screen**
Helpful Guide
https://howchoo.com/g/zwq2zwixotu/how-to-make-a-raspberry-pi-smart-alarm-clock

Dependencies
```
sudo apt-get install i2c-tools
sudo apt-get install python-smbus
i2cdetect -y 1
```

**RFID MFRC522 Info**
Helpful Guide
https://github.com/ondryaso/pi-rc522
