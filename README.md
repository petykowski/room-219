Room 219
=============

Objectives
-------
Measure room temperature and write to MySQL database for use on website.

Example
-------
[Temperature in 219] (https://server.myprevio.us)

Requirements
-----------
* Raspberry Pi B+
* DHT11 Temperature and Humidity Sensor
* MySQL Server
* [DHT11 Library] (https://github.com/szazo/DHT11_Python)

Configuration
-----------
Edit config_example.py 
```python
host='hostname' # Host Name of MySQL Server
user='username' # Username used to conenct to MySQL Server
password='password' # Password used to conenct to MySQL Server
db='database' # Name of MySQL Database
```

Resources
------------
* DHT11 Sensor Library from [szazo](https://github.com/szazo/DHT11_Python). 
