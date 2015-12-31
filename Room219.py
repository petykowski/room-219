#!/usr/bin/python

# v1.02

import pymysql.cursors
import random
import time
import RPi.GPIO as GPIO
import dht11
import datetime
import config

# Establish Connection to Local MySQL Database
connection = pymysql.connect(
    host=config.host,
    user=config.user,
    password=config.password,
    db=config.db,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# Configure GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Configure DHT11 to Operate on Pin 4
sensor = dht11.DHT11(pin = 4)

# Set Bad Readings Value to 0
badReadings = 0

while True:
    result = sensor.read()
    if result.is_valid():
        degreesInCelsius = result.temperature
        badReadings = 0
        
        # Establish a connection to request current Temperature ID
        # Temperature ID is numerical order value
        with connection.cursor() as cursor:
            currentID = "SELECT COUNT(TempID) FROM env_sensors"
            cursor.execute(currentID)
            result = cursor.fetchone()
            tempID = result['COUNT(TempID)']
            
        # Convert Celsius to Fahrenheit
        degressInFahrenheit = degreesInCelsius * 1.8 + 32
        
        # Sensor is reading room temperature. Reading should not exceed 5 degrees since last reading.
        with connection.cursor() as cursor:
            getLastTemperatureEntry = "SELECT TemperatureF FROM env_sensors ORDER BY TempID DESC LIMIT 1"
            cursor.execute(getLastTemperatureEntry)
            fetchedLastTemperatureEntry = cursor.fetchone()
            lastTemperatureEntry = fetchedLastTemperatureEntry['TemperatureF']
            
            # Verify that Temperature Reading is Correct
            if degressInFahrenheit < lastTemperatureEntry - 5 or degressInFahrenheit > lastTemperatureEntry + 5:
                print "Incorrect reading from sensor. Ignoring last reading."
            else:
                # Write Temperature and TempID to database
                sql = "INSERT INTO env_sensors (TempID, TemperatureF, TemperatureC, Date_Time) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)"
                cursor.execute(sql, (tempID, degressInFahrenheit, degreesInCelsius))
                connection.commit()
                print "Record", degressInFahrenheit, "F at", str(datetime.datetime.now())
        time.sleep(60)
        
    else:
        badReadings = badReadings + 1
        print badReadings
        if badReadings == 3:
            print "Sensor is not responding. Re-Attempting..."
            badReadings = 0
    time.sleep(1)