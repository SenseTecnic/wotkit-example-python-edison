#!/usr/bin/python

# A python script that will get data from GPIO and send as a JSON event to WoTKit
import time
import httplib, urllib, urllib2, base64
import psutil
import threading
import sys

# add gpio library from emutex
# https://github.com/emutex/wiring-x86
from wiringx86 import GPIOEdison as GPIO

try:
    import json
except ImportError:
    import simplejson as json

#TODO: ADD YOUR SENSOR NAME AND CREDENTIALS
SENSOR_NAME = 'YOURSENSORNAME'
USERNAME = 'YOURUSERNAME'
PASSWORD = 'YOURPASSWORD'

HOST = "wotkit.sensetecnic.com"

gpio = GPIO(debug=False) #set after serial is done
# Set pins
pin = 8
gpio.pinMode(pin, gpio.OUTPUT)
analogpin = 14
gpio.pinMode(analogpin, gpio.ANALOG_INPUT)

#declaring our schema
sensor_data = {
    "value": "0",
    "cpu": "0",
    "memory": "0",
    "relay1": "0",
    "sensor1": "0"
}

auth = base64.encodestring('%s:%s' % (USERNAME, PASSWORD)).replace('\n', '')
headers = {"Content-type": "application/x-www-form-urlencoded",
        "Authorization": "Basic %s" % auth
} 

def getProcData(sensor_data):
    cpu = psutil.cpu_percent(interval=0);
    memory = psutil.virtual_memory()
    sensor_data['value'] = cpu
    sensor_data['cpu'] = cpu
    sensor_data['memory'] = memory[2] #percent

def getPinData(sensor_data):
    value = gpio.analogRead(analogpin)
    sensor_data['sensor1'] = value

def registerListener(headers, params):
    URL = "/api/v1/control/sub/%s" % SENSOR_NAME
    conn = httplib.HTTPConnection(HOST);
    conn.request("POST", URL, urllib.urlencode(params), headers)
    response = conn.getresponse()
    data = json.load(response)
    conn.close()
    return data['subscription']

class eventThread (threading.Thread):
    def __init__(self, subscriptionID):
        threading.Thread.__init__(self)
        self.subscriptionID = subscriptionID
    def run(self):
        while True:
            URL = "/api/v1/control/sub/%s?wait=10" % self.subscriptionID
            params = urllib.urlencode({})
            conn = httplib.HTTPConnection(HOST)
            conn.request("GET", URL, params, headers)
            response = conn.getresponse()
            data = json.load(response)
            if len(data) > 0: 
                button = data[0]['button'] 
                if button == 'off':
                    gpio.digitalWrite(pin, gpio.LOW)
                    sensor_data['relay1'] = 0
                if button == 'on':
                    gpio.digitalWrite(pin, gpio.HIGH)
                    sensor_data['relay1'] = 1
            conn.close()

class sensorThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            URL = "/api/v1/sensors/%s/data" % SENSOR_NAME
            getProcData(sensor_data)
            getPinData(sensor_data)
            params = urllib.urlencode(sensor_data)
            conn = httplib.HTTPConnection(HOST);
            conn.request("POST", URL, params, headers)
            response = conn.getresponse()
            conn.close()
        
            time.sleep(2)

def main():

    subscriptionID = registerListener(headers, {})

    event_thread = eventThread(subscriptionID)
    event_thread.start()

    sensor_thread = sensorThread()
    sensor_thread.start()

    while True:
        sys.stdout.write("\rSensor: %s | Relay1: %s  " % (sensor_data['sensor1'], sensor_data['relay1']) )
        sys.stdout.flush()
        time.sleep(1)
    
if __name__ == "__main__":
    main()
    


