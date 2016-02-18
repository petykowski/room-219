Room 219
=============

Objectives
-------
Measure room temperature and write to MySQL database for use on website, iOS, and Apple Watch app.

Example
-------
[Temperature in 219] (https://server.myprevio.us)

Requirements
-----------
* Raspberry Pi B+
* DHT11 Temperature and Humidity Sensor
* MySQL Server
* [DHT11 Library] (https://github.com/szazo/DHT11_Python)

Installation
-----------
Navigate to your working directory in Terminal.app.
```shell
$ cd /path/to/working/directory
```
Clone the repo to your directory.
```shell
$ git clone https://github.com/spetykowski/room-219.git
```
Clone [szazo's DHT11 Python library](https://github.com/szazo/DHT11_Python) repo to your directory.
```shell
$ git clone https://github.com/szazo/DHT11_Python.git
```
Rename file [config_example.py] (https://github.com/spetykowski/room-219/blob/master/config_example.py) to config.py.
```shell
$ mv config_example.py config.py
```

Configuration
-----------
Edit your newly renamed config.py 
```python
host='hostname' # Host Name of MySQL Server
user='username' # Username used to conenct to MySQL Server
password='password' # Password used to conenct to MySQL Server
db='database' # Name of MySQL Database
charset='SQLcharset' # Charset for MySQL Database
pin=4 # refer to RaspberryPi GPIO pin layout
```

Usage
-----------
Room 219 can be started a number of ways. First is by calling Python to run the script.
```shell
$ python Room219.py start
```
Call the process directly: (file requires execute permissions)
```shell
$ ./Room219.py start
```
To run the script continiously in the background:
```shell
$ nohup ./Room219.py start &
```
Stop a background process with:
```shell
$ ./Room219.py stop
```

Resources
------------
* DHT11 Sensor Library from [szazo](https://github.com/szazo/DHT11_Python). 
