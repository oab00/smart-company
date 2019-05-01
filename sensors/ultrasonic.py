
import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
		
	client.subscribe("Ultrasonic/Main")
	client.subscribe("ULTRASONIC1") # Remote (Out)
	client.subscribe("ULTRASONIC2") # Local (In)


ultrasonics_status = "OFF"
ultrasonic_out = 0
ultrasonic_in = 0


def on_message(client, userdata, message):
	global ultrasonics_status, ultrasonic_in, ultrasonic_out
	payload = str(message.payload.decode('utf-8'))
	#print("Received message '" + payload + "' on topic '" + message.topic + "' with QoS " + str(message.qos))
	
	# Turn On or Off
	if message.topic == "Ultrasonic/Main":
		if payload == "ON":
			ultrasonics_status = "ON"
		elif payload == "OFF":
			ultrasonics_status = "OFF"

	# Remote Ultrasonic (Out)
	elif message.topic == "ULTRASONIC1":
		if ultrasonics_status == "OFF":
			return

		ultrasonic_out = int(payload)

	# Local Ultrasonic (In)
	elif message.topic == "ULTRASONIC2":
		if ultrasonics_status == "OFF":
			return

		ultrasonic_in = int(payload)


mqttc=mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost",1883,60)
mqttc.loop_start() # start another thread


while True:
	if ultrasonic_out < 18:
		# time.sleep(1)
		if ultrasonic_in < 18:
			# visitors = visitors + 1
			mqttc.publish("Ultrasonic/Main", "INCREASE")

	elif ultrasonic_in < 18:
		# time.sleep(1)
		if ultrasonic_out < 18:
			# visitors = visitors - 1
			mqttc.publish("Ultrasonic/Main", "DECREASE")








