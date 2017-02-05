#!/usr/bin/python

# v2.00

# Import Resources
import pymysql.cursors
import time
import RPi.GPIO as GPIO
import dht11
import datetime
import config
import subprocess
import argparse
import Adafruit_DHT

# Configure argparse
parser = argparse.ArgumentParser(description='Process to gather temperature data and write to MySQL database.')
parser.add_argument('command', choices=['start', 'stop', 'restart', 'test'])
args = parser.parse_args()

# Establish Connection to Local MySQL Database
connection = pymysql.connect(
    host=config.host,
    user=config.user,
    password=config.password,
    db=config.db,
    charset=config.charset,
    cursorclass=pymysql.cursors.DictCursor
)

# Configure GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Configure DHT11 to Operate on User Defined Pin
led = 26
GPIO.setup(led, GPIO.OUT)

# Configure DHT11 to Operate on GPIO (Deprecated)
#sensor = dht11.DHT11(pin = config.pin)

# Configure Sensor to DHT 22 to GPIO Pin
sensor = Adafruit_DHT.DHT22
pin = config.pin

# Set Bad Readings Value to 0
badReadings = 0

if args.command == "stop":
    PID = subprocess.check_output("ps -ax | grep -v grep | grep Room219.py\ start | awk '{print $1}'", shell=True).replace('\n','')
    if PID == "":
        print "Process Room 219 is not currently running."
    else:    
        print "Killing process " + PID + "."
        subprocess.call(["kill", PID])
        
if args.command == "test":
    humidity, temperature = Adafruit_DHT.read(sensor, pin)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')
        
if args.command == "start":
    try:
        while True:
            humidity, temperature = Adafruit_DHT.read(sensor, pin)
            if humidity is not None and temperature is not None:
                degreesInCelsius = temperature
                badReadings = 0
                GPIO.output(led, 1)

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
                    if degressInFahrenheit < lastTemperatureEntry - 10 or degressInFahrenheit > lastTemperatureEntry + 10:
                        print "Incorrect reading from sensor. Ignoring last reading."
                    else:
                        # Write Temperature and TempID to database
                        sql = "INSERT INTO env_sensors (TempID, TemperatureF, TemperatureC, Date_Time) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)"
                        cursor.execute(sql, (tempID, degressInFahrenheit, degreesInCelsius))
                        connection.commit()
                        print "Record", degressInFahrenheit, "F at", str(datetime.datetime.now())
                        GPIO.output(led, 0)
                        
                time.sleep(60)

            else:
#                print("Error: %d" % result.error_code)
                badReadings = badReadings + 1
                print badReadings
                if badReadings == 3:
                    print "Sensor is not responding. Re-Attempting..."
                    badReadings = 0
            time.sleep(1)

    finally:
        print "reached finally"
        connection.close()