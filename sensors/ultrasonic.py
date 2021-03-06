import RPi.GPIO as GPIO
import time
import requests

try:

      GPIO.setmode(GPIO.BCM)

      PIN_TRIGGER = 4
      PIN_ECHO = 17

      GPIO.setup(PIN_TRIGGER, GPIO.OUT)
      GPIO.setup(PIN_ECHO, GPIO.IN)

      GPIO.output(PIN_TRIGGER, GPIO.LOW)

      print "Waiting for sensor to settle"

      time.sleep(2)

      print "Calculating distance"
      
      while True:

	      GPIO.output(PIN_TRIGGER, GPIO.HIGH)
	
	      time.sleep(0.00001)
	
	      GPIO.output(PIN_TRIGGER, GPIO.LOW)
	
	      while GPIO.input(PIN_ECHO)==0:
	            pulse_start_time = time.time()
	      while GPIO.input(PIN_ECHO)==1:
	            pulse_end_time = time.time()
	
	      pulse_duration = pulse_end_time - pulse_start_time
	      distance = round(pulse_duration * 17150, 2)

	      requests.get('http://localhost:5000/adddist?dist={}'.format(distance))
	      

	      print("Distance:", distance, "cm")

              if distance <= 10.0:
		     print("There is an object closeby.")

	      time.sleep(3)

finally:
      GPIO.cleanup()                     