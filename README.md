# RPHSP
Raspberry Pi Home Security Project

Requirements
1. pip install pi-rc522
2. pip install pad4pi
3. pip install redis



Keypad Configuration
=====================
GPIO Pin Numbers
14,15,18,17,27,22,13

Left to right look at keypad 14,15,18,13,17,27,22

[Col 2] [row 1] [col 1] [row 4] [col 3] [row 3] [row 2]

COL [18, 14, 17]

ROW [15, 22, 27, 13]

* To adjust the key delay, go to this file and edit the "DEFAULT_KEY_DELAY" value
/home/pi/.local/lib/python2.7/site-packages/pad4pi/rpi_gpio.py




Dependencies
============
sudo apt-get install i2c-tools
sudo apt-get install python-smbus
i2cdetect -y 1


Tutorial
============
https://howchoo.com/g/zwq2zwixotu/how-to-make-a-raspberry-pi-smart-alarm-clock

PHP Redis Admin
===============
https://github.com/erikdubbelboer/phpRedisAdmin
https://www.knowledgebase-script.com/kb/article/how-to-enable-mbstring-in-php-46.html
