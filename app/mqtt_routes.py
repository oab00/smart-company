from flask import Flask, render_template, flash, redirect, request, jsonify
from flask import current_app as app
import sqlite3 as sql
import time 
import json
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO, emit

from . import LogicSystem
from . import Statistics

PIN_COOLER = 17 # GPIO Pin for Cooler

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
   print("Connected with result code " + str(rc))

   # Subscribing in on_connect() means that if we lose the connection and
   # reconnect then subscriptions will be renewed.
   client.subscribe("RFID/Office")
   client.subscribe("RFID/Gate")
   client.subscribe("RFID/MeetingRoom") 
   client.subscribe("RFID/Mosque")
   client.subscribe("RFID/CoffeeShop")
   client.subscribe("RFID/Restroom")

   client.subscribe("LCD/write")
   client.subscribe("LCD/write2")
   client.subscribe("Ultrasonic/Main")
   client.subscribe("ULTRASONIC1")
   client.subscribe("ULTRASONIC2")
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

      # based on employee preference
      if (float(message.payload) > 24.0): # pref_temp):
         # turn on cooler
         GPIO.output(PIN_COOLER, GPIO.HIGH)
      else:
         # turn off cooler
         GPIO.output(PIN_COOLER, GPIO.LOW)


   elif message.topic == "/esp8266/humidity":
      print("humidity update")
      socketio.emit('dht_humidity', {'data': message.payload})
   

   elif message.topic == "ULTRASONIC1":
      print("Ultrasonic1:", payload)


   elif message.topic == "RFID/Gate": # Gate for now
      #print('Gate RFID: ', payload)
      logicSystem.rfid_reading(payload, "On Campus")
      #print("Gate RFID: ", employee.name + ',', employee.cardID)
      socketio.emit('local_rfid', {'data': payload})
      employee = logicSystem.get_employee_by_rfid(payload)
      mqttc.publish("LCD/write", employee.name)

   elif message.topic == "RFID/Office": # should be office
      #print("Office RFID: ", payload)
      socketio.emit('remote_rfid', {'data': payload})
      logicSystem.office_rfid_reading(payload)

   elif message.topic == "RFID/MeetingRoom":
      #print("RFID_MeetingRoom: ", "'" +payload+"'")
      logicSystem.rfid_reading(payload, "Meeting Room")

   elif message.topic == "RFID/Mosque":
      #print("RFID_Mosque: ", payload)
      logicSystem.rfid_reading(payload, "Mosque")

      mqttc.publish("ULTRASONIC2", "OFF")

   elif message.topic == "RFID/CoffeeShop":
      #print("RFID_CoffeeShop: ", payload)
      logicSystem.rfid_reading(payload, "Coffee Shop")

   elif message.topic == "RFID/Restroom":
      #print("RFID_Restroom: ", payload)
      logicSystem.rfid_reading(payload, "Restroom")
      

   elif message.topic == "Ultrasonic/Main":
      logicSystem.office.set_visitors(payload)
      
   
# Initialize MQTT
mqttc=mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost",1883,60)
mqttc.loop_start()

# Initialize System
socketio = SocketIO(app)
logicSystem = LogicSystem.LogicSystem(socketio, mqttc)
statistics = Statistics.Statistics()

# Clear LCD Screen
mqttc.publish("LCD/write2", "")


def get_template_data(active_list, active_item):
   return {
      "employees": logicSystem.employees,
      "locations": logicSystem.locations,
      "active_list": active_list,
      "active_item": active_item
   }


@app.route("/", strict_slashes=False)
def homepage():
   template_data = get_template_data('homepage', None)
   return render_template('wifi-homepage.html', **template_data)


@app.route("/main", strict_slashes=False)
def main():
   template_data = get_template_data(None, None)
   return render_template('wifi-main.html', **template_data)


@app.route("/wifi", strict_slashes=False)
@app.route("/sensors", strict_slashes=False)
def sensors():
   template_data = get_template_data('sensors', None)
   return render_template('wifi-sensors.html', async_mode=socketio.async_mode, **template_data)


@app.route("/employees", strict_slashes=False)
def employees():
   template_data = get_template_data('employees', None)
   return render_template('wifi-employees.html', **template_data)


@app.route("/employee/<emp_name>", strict_slashes=False)
def employee(emp_name):
   emp_name = emp_name.replace('.', ' ')
   employee = logicSystem.get_employee(emp_name)

   rfids = logicSystem.rfids.get_rfids_for_employee(employee)
   length = len(rfids)

   template_data = get_template_data('employees', emp_name)
   return render_template('wifi-employee.html', employee=employee, rfids=rfids, length=length, **template_data) 


@app.route("/locations", strict_slashes=False)
def locations():
   template_data = get_template_data('locations', None)
   return render_template('wifi-locations.html', **template_data)


@app.route("/location/<loc_name>", strict_slashes=False)
def location(loc_name):
   loc_name = loc_name.replace('.', ' ')
   location = logicSystem.get_location(loc_name)

   rfids = logicSystem.rfids.get_rfids_for_location(location)
   length = len(rfids)

   template_data = get_template_data('locations', loc_name)
   return render_template('wifi-location.html', location=location, rfids=rfids, length=length, **template_data)


@app.route("/statistics", strict_slashes=False)
def statistics_url():
   consumptions = statistics.consumption.get_daily_consumptions('Office', 'Omar Bamarouf')
   consumptions = json.dumps(consumptions)

   performances = statistics.performance.get_daily_performances('Omar Bamarouf')
   performances = json.dumps(performances)
   
   template_data = get_template_data(None, None)
   return render_template('wifi-statistics.html', **template_data, consumptions=consumptions, performances=performances)


@app.route('/<path:path>')
@app.route('/employee/assets/<path:path>')
@app.route('/employees/assets/<path:path>')
@app.route('/location/assets/<path:path>')
@app.route('/locations/assets/<path:path>')
@app.route('/statistics/assets/<path:path>')
def static_files_send(path):    
    return app.send_static_file(path)
