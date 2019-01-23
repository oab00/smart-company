import RPi.GPIO as GPIO
from libs import dht11
import time
import requests

GPIO.setmode(GPIO.BCM)

instance = dht11.DHT11(pin=14)


try:
	time.sleep(2)
	while True:
		result = instance.read()

		if result.is_valid():
			print("Temperature: %d C" % result.temperature)
			print("Humidity: %d %%" % result.humidity)

			temp = result.temperature
			hum = result.humidity

			requests.get('http://localhost:5000/addtemp?temp={}&hum={}'.format(temp, hum))

		time.sleep(1)

finally:
	GPIO.cleanup()