
'''
UltrasonicReadingOut = 0
UltrasonicReadingIn = 0
Visitors = 0

while True:
	while UltrasonicReadingOut <100:
		time.sleep(1)
		if UltrasonicReadingIn <100:
			Visitors += 1
		else:
			break

	while UltrasonicReadingIn <100:
		time.sleep(1)
		if UltrasonicReadingOut <100:
			Visitors -= 1
			if Visitors = 0:
				EmployeeStatus = "Available"
		else:
			break 
'''

# MQTT Turn On
# MQTT Turn OFF
# MQTT Reading

import paho.mqtt.client as paho
client= paho.Client("Ultrasonic_Main")














