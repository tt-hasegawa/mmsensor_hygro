import RPi.GPIO as GPIO
import datetime
import dht11
import os
import requests
import sys
import time
import logging

logging.basicConfig(filename='/tmp/sensor-hygrometer.log', level=logging.DEBUG)

#url='https://frozen-reef-90562.herokuapp.com/'
url='http://192.168.46.128:3000'
#proxies = {
#    'http': 'http://proxy.matsusaka.co.jp:12080',
#    'https': 'http://proxy.matsusaka.co.jp:12080'
#}
proxies = {
    'http': None,
    'https': None
}

logging.info("Hygrometer Start.[{}]".format(url))

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 4
instance = dht11.DHT11(pin=4)
 
logging.info("Hygrometer Initialized.")

try:
    while True:
        logging.info("Check Start.")
        temperature=0
        humidity=0
        result = instance.read()
        if result.is_valid():
            temperature=result.temperature
            humidity=result.humidity

        logging.info("Check Temperature:{} Humidity:{}.".format(temperature,humidity))

        uploadData={
                'temperature':str(temperature),
                'humidity':str(humidity)
        }
        logging.info(uploadData)
        try:
            logging.info("POST Start.{}")
            response = requests.post(url + '/addHygrometer/' , json=uploadData, proxies=proxies)
            logging.info("POST End. {}".format(response.text))
        except Exception as e:
            logging.info(e)
        time.sleep(10)

except KeyboardInterrupt:
    logging.info("Cleanup")
    GPIO.cleanup()

