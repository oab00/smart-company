import time
import RPi.GPIO as GPIO
import MFRC522

import paho.mqtt.client as paho
client= paho.Client("RFID_Office")
time.sleep(2)

print("connecting to broker ","localhost")
client.connect("192.168.1.192", 1883, 0)#connect
print("subscribing ")
client.subscribe("RFID/Office")#subscribe

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
 
# Welcome message
print("Looking for cards")
print("Press Ctrl-C to stop.")
 
# This loop checks for chips. If one is near it will get the UID
try:
   
  while True:
 
    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
 
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
 
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
 
      # Print UID
      #UID = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

      UID = ''

      for i in range(4):
        UID = UID + "{0:x}".format(uid[i]).zfill(2).upper() + ' '

      UID = UID[:-1]
      #print(UID)

      #UID = "{0:x} {1:x} {2:x} {3:x}".format(uid[0], uid[1], uid[2], uid[3]).upper()

      print("UID: ", UID)
      client.publish("RFID/Office", UID)#publish
 
      time.sleep(2)
 
except KeyboardInterrupt:
  client.disconnect() #disconnect
  GPIO.cleanup()
