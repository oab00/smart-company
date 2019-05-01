
import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
		
	client.subscribe("Ultrasonic/Main")
	client.subscribe("ULTRASONIC2") # Local (In)

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.connect("localhost",1883,60)
mqttc.loop_start() # start another thread

try:

	GPIO.setmode(GPIO.BCM)

	PIN_TRIGGER = 4
	PIN_ECHO = 17

	GPIO.setup(PIN_TRIGGER, GPIO.OUT)
	GPIO.setup(PIN_ECHO, GPIO.IN)

	GPIO.output(PIN_TRIGGER, GPIO.LOW)

	print("Waiting for sensor to settle")

	time.sleep(2)

	print("Calculating distance")

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
		mqttc.publish("ULTRASONIC2", str(distance))
		print("Distance:", distance, "cm")
		time.sleep(2)

finally:
	GPIO.cleanup()                     