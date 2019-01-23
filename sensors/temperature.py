import RPi.GPIO as GPIO
import dht11
import time

GPIO.setmode(GPIO.BCM)

instance = dht11.DHT11(pin=14)


try:
	while True:
		result = instance.read()

		if result.is_valid():
			print("Temperature: %d C" % result.temperature)
			print("Humidity: %d %%" % result.humidity)
	
		time.sleep(0.25)

finally:
	GPIO.cleanup()