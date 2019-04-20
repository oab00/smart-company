from flask import Flask, render_template, flash, redirect, request, jsonify
from flask import current_app as app
import sqlite3 as sql
from time import time
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO, emit

from . import LogicSystem
logicSystem = LogicSystem.LogicSystem()

#socketio = SocketIO(app)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("RFID/Office")
    client.subscribe("RFID/Gate")
    client.subscribe("RFID/MeetingRoom") 
    client.subscribe("RFID/Mosque")
    client.subscribe("RFID/CoffeeShop")
    client.subscribe("RFID/Restroom")

    client.subscribe("ULTRASONIC1")
    
    client.subscribe("LCD/write")
    
    client.subscribe("/esp8266/temperature")
    client.subscribe("/esp8266/humidity")
    

# The callback for when a PUBLISH message is received from the ESP8266.
def on_message(client, userdata, message):
   payload = str(message.payload.decode('utf-8'))
   #socketio.emit('my variable')
   #print("Received message '" + payload + "' on topic '" + message.topic + "' with QoS " + str(message.qos))
   if message.topic == "/esp8266/temperature":
       print("temperature update")
       #socketio.emit('dht_temperature', {'data': message.payload})
   if message.topic == "/esp8266/humidity":
       print("humidity update")
       #socketio.emit('dht_humidity', {'data': message.payload})
   #if message.topic == "RFID/cardID":
   #print('RFID update', message.payload.decode("utf-8"))

   if message.topic == "ULTRASONIC1":
      #print("Ultrasonic1:", payload)
      pass



   if message.topic == "RFID/Office": # Gate for now
      print('Gate RFID: ', payload)
      logicSystem.gate_rfid_reading(payload, "Gate")
      #print("Gate RFID: ", employee.name + ',', employee.cardID)
      #socketio.emit('local_rfid', {'data': payload})

   elif message.topic == "RFID/Gate": # should be office
      print("Office RFID: ", payload)
      #socketio.emit('remote_rfid', {'data': payload})

   elif message.topic == "RFID/MeetingRoom":
      print("RFID_MeetingRoom: ", payload)
   elif message.topic == "RFID/Mosque":
      print("RFID_Mosque: ", payload)
   elif message.topic == "RFID/CoffeeShop":
      print("RFID_CoffeeShop: ", payload)
   elif message.topic == "RFID/Restroom":
      print("RFID_Restroom: ", payload)
      
   


mqttc=mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost",1883,60)
mqttc.loop_start()

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   4 : {'name' : 'GPIO 4', 'board' : 'esp8266', 'topic' : 'esp8266/4', 'state' : 'False'},
   5 : {'name' : 'GPIO 5', 'board' : 'esp8266', 'topic' : 'esp8266/5', 'state' : 'False'}
   }

# Put the pin dictionary into the template data dictionary:
templateData = {
   'pins' : pins
   }

@app.route("/main")
def main():
   # Pass the template data into the template main.html and return it to the user
   #return render_template('index.html', async_mode=socketio.async_mode, **templateData)
   return render_template('main.html', **templateData)

@app.route("/")
def wifi():
   # Pass the template data into the template main.html and return it to the user
   #return render_template('index.html', async_mode=socketio.async_mode, **templateData)
   return render_template('wifi-data.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<board>/<changePin>/<action>")
def action(board, changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   devicePin = pins[changePin]['name']
   # If the action part of the URL is "1" execute the code indented below:
   if action == "1" and board == 'esp8266':
      mqttc.publish(pins[changePin]['topic'],"1")
      pins[changePin]['state'] = 'True'
   if action == "0" and board == 'esp8266':
      mqttc.publish(pins[changePin]['topic'],"0")
      pins[changePin]['state'] = 'False'
   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }
   return render_template('wifi-data.html', **templateData)

@app.route("/LCD_Write/")
def LCD_write():  
   mqttc.publish("LCD/write", "OMAR IS BOSS")

   for i in range(21):
      time.sleep(0.25)
      mqttc.publish("LCD/write", "OMAR IS BOSS " + str(i))

   print("Written to LCD")

   return render_template('wifi-data.html', **templateData)

#@socketio.on('my event')
#def handle_my_custom_event(json):
#    print('received json data here: ' + str(json))
