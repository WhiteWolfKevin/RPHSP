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

**Keypad I2C LCD Screen**\
Helpful Guide
https://howchoo.com/g/zwq2zwixotu/how-to-make-a-raspberry-pi-smart-alarm-clock

Dependencies
```
sudo apt-get install i2c-tools
sudo apt-get install python-smbus
i2cdetect -y 1
```

**RFID MFRC522 Info**\
Helpful Guide
https://github.com/ondryaso/pi-rc522

### Database Configuration
**Raspberry Pi Configuration**\
Make the database accessible from the network.
```
Network Access: Add "bind_address=192.168.1.250" and "[mysqld] bind_address=192.168.1.250" to /etc/mysql/mariadb.cnf
```

Create the main database.
```
CREATE DATABASE rphsp;
```

Create the user of the database and give all privileges to that user.
```
CREATE USER 'rphsp'@'192.168.1.0/255.255.255.0';
```
```
GRANT ALL PRIVILEGES ON rphsp.* TO 'rphsp'@'192.168.1.0/255.255.255.0';
```

Create all of the tables.
```
CREATE TABLE sensors (
     gpio_pin INT(2) PRIMARY KEY,
     name VARCHAR(30),
     type VARCHAR(30)
);
```
```
CREATE TABLE alarms (
     id INT(2) PRIMARY KEY,
     name VARCHAR(30),
     status VARCHAR(15)
);
```
```
CREATE TABLE user_information (
     user_id int(4) AUTO_INCREMENT,
     first_name varchar(30) NOT NULL,
     last_name varchar(30) NOT NULL,
     date_added datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
     enabled bool NOT NULL DEFAULT 1,
     PRIMARY KEY (user_id)
);
```
```
CREATE TABLE rfid_cards (
     card_number char(10),
     user_id int(4),
     PRIMARY KEY (card_number),
     FOREIGN KEY (user_id) REFERENCES user_information(user_id)
);
```
```
CREATE TABLE pin_codes (
     pin_code int(6),
     user_id int(4),
     PRIMARY KEY (pin_code),
     FOREIGN KEY (user_id) REFERENCES user_information(user_id)
);
```
```
CREATE TABLE relays (
     relay_id int(4) AUTO_INCREMENT,
     relay_name varchar(30) NOT NULL,
     channels int (2) NOT NULL,
     PRIMARY KEY (relay_id)
);
```
```
CREATE TABLE relay_pins (
     relay_id int(4),
     relay_pin int(2),
     status char(3),
     PRIMARY KEY (relay_id, relay_pin),
     FOREIGN KEY (relay_id) REFERENCES relays(relay_id)
);
```

Test data inserts.
```
INSERT INTO sensors (gpio_pin, name, type) VALUES (16, "Front Door", "Door");
INSERT INTO sensors (gpio_pin, name, type) VALUES (20, "Garage Door", "Door");
INSERT INTO sensors (gpio_pin, name, type) VALUES (21, "Basement Door", "Door");
INSERT INTO sensors (gpio_pin, name, type) VALUES (26, "Living Room Window", "Window");
```

```
INSERT INTO user_information (first_name, last_name) VALUES ("Kevin", "Tate");
INSERT INTO rfid_cards VALUES ("4a1a560f09", 1);
INSERT INTO pin_codes VALUES (111111, 1);
```

```
INSERT INTO relays (relay_name, channels) VALUES ("Test Relay", 4);
INSERT INTO relay_pins VALUES (1, 4, "Off");
INSERT INTO relay_pins VALUES (1, 17, "Off");
INSERT INTO relay_pins VALUES (1, 27, "Off");
INSERT INTO relay_pins VALUES (1, 22, "Off");
```
