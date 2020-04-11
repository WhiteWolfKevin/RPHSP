# RPHSP
Raspberry Pi Home Security Project

Requirements
1. pip install pi-rc522
2. pip install pad4pi
3. pip install redis


Database Configuration
======================
Network Access: Add "bind_address=192.168.1.250" and "[mysqld] bind_address=192.168.1.250" to /etc/mysql/mariadb.cnf
create database rphsp;
create table sensors( gpio_pin int(2) primary key, name varchar(30), type varchar(30));
create table alarms( id int(2) primary key, name varchar(30), status varchar(15));
create user 'rphsp'@'192.168.1.0/255.255.255.0';
grant all privileges on rphsp.* TO 'rphsp'@'192.168.1.0/255.255.255.0;


Camera Stuff
============
RTSP URL: rtsp://192.168.1.169:554/1/h264major


Keypad Configuration
=====================
GPIO Pin Numbers
14,15,18,17,27,22,13

Left to right look at keypad 14,15,18,13,17,27,22

[Col 2] [row 1] [col 1] [row 4] [col 3] [row 3] [row 2]

COL [18, 14, 17]

ROW [15, 22, 27, 13]

* To adjust the key delay, go to this file and edit the "DEFAULT_KEY_DELAY" value
* Default value is 300
* A good value to set 150
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
