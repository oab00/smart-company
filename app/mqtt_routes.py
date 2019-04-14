from flask import Flask, render_template, flash, redirect, request, jsonify
from app import app, db
from app.forms import LoginForm
import sqlite3 as sql
from datetime import datetime
from time import strftime
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO, emit
import logging

from app.LogicSystem import LogicSystem
logicSystem = LogicSystem()

socketio = SocketIO(app)

log = logging.getLogger('werkzeug')
log.disabled = True

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("RFID/cardID") # Office
    client.subscribe("Remote_RFID/cardID") # Gate
    client.subscribe("RFID/MeetingRoom") 
    client.subscribe("RFID/Mosque")
    client.subscribe("RFID/CoffeeShop")
    client.subscribe("RFID/Bathroom")

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
       socketio.emit('dht_temperature', {'data': message.payload})
   if message.topic == "/esp8266/humidity":
       print("humidity update")
       socketio.emit('dht_humidity', {'data': message.payload})
   #if message.topic == "RFID/cardID":
   #print('RFID update', message.payload.decode("utf-8"))

   if message.topic == "ULTRASONIC1":
      print("Ultrasonic1:", payload)

   '''
   if payload == "8A 86 B8 73":
      payload = "Mohammed Al-Qarni"
   elif payload == "91 D8 9E 66":
      payload = "Baraa Ismail"
   elif payload == "41 24 9B 66":
      payload = "Omar Bamarouf"
   elif payload == "9 BA 52 5":
      payload = "Raed Al-Harthi"
   elif payload == "90 A2 42 83":
      payload = "Ibrahim Al-Hasan"
   '''


   if message.topic == "Remote_RFID/cardID" or True:
      print("Remote RFID: ", payload)
      socketio.emit('remote_rfid', {'data': payload})

      logicSystem.gate_rfid_reading(payload)

   elif message.topic == "RFID/cardID":
      print("Local RFID:  ", payload)
      socketio.emit('local_rfid', {'data': payload})

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

@app.route("/wifi")
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
   mqttc.publish("LCD/write", "Omar is the BOSS")
   print("Written to LCD")

   templateData = {
      'pins' : pins
   }
   return render_template('wifi-data.html', **templateData)

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json data here: ' + str(json))
