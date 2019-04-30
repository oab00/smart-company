from flask import Flask, render_template, flash, redirect, request, jsonify
from flask import current_app as app
import sqlite3 as sql
import time 
import json
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO, emit

from . import LogicSystem
from . import Statistics

#from kombu import Connection
#connection = Connection('amqp://guest:guest@0.0.0.0:5672//')
#connection.connect()

socketio = SocketIO(app)# message_queue="amqp://guest:guest@0.0.0.0:5672//")
logicSystem = LogicSystem.LogicSystem(socketio)
statistics = Statistics.Statistics()

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
   client.subscribe("Ultrasonic/Main")
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

   elif message.topic == "/esp8266/humidity":
      print("humidity update")
      socketio.emit('dht_humidity', {'data': message.payload})
   

   elif message.topic == "ULTRASONIC1":
      print("Ultrasonic1:", payload)


   elif message.topic == "RFID/Office": # Gate for now
      #print('Gate RFID: ', payload)
      logicSystem.rfid_reading(payload, "Gate")
      #print("Gate RFID: ", employee.name + ',', employee.cardID)
      socketio.emit('local_rfid', {'data': payload})
      employee = logicSystem.get_employee_by_rfid(payload)
      mqttc.publish("LCD/write", employee.name)

   elif message.topic == "RFID/Gate": # should be office
      print("Office RFID: ", payload)
      socketio.emit('remote_rfid', {'data': payload})
      logicSystem.office_rfid_reading(payload)

   elif message.topic == "RFID/MeetingRoom":
      #print("RFID_MeetingRoom: ", "'" +payload+"'")
      logicSystem.rfid_reading(payload, "Meeting Room")

   elif message.topic == "RFID/Mosque":
      print("RFID_Mosque: ", payload)
      logicSystem.rfid_reading(payload, "Mosque")

   elif message.topic == "RFID/CoffeeShop":
      print("RFID_CoffeeShop: ", payload)
      logicSystem.rfid_reading(payload, "Coffee Shop")

   elif message.topic == "RFID/Restroom":
      print("RFID_Restroom: ", payload)
      logicSystem.rfid_reading(payload, "Restroom")
      
   elif message.topic == "Ultrasonic/Main":
      logicSystem.office.set_visitors(payload)
      
   


mqttc=mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost",1883,60)
mqttc.loop_start()


mqttc.publish("LCD/write", "")

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   4 : {'name' : 'GPIO 4', 'board' : 'esp8266', 'topic' : 'esp8266/4', 'state' : 'False'},
   5 : {'name' : 'GPIO 5', 'board' : 'esp8266', 'topic' : 'esp8266/5', 'state' : 'False'}
   }

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
   #return render_template('index.html', async_mode=socketio.async_mode, **templateData)
   return render_template('wifi-sensors.html', **template_data, pins=pins)


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
   
   template_data = get_template_data(None, None)
   return render_template('wifi-statistics.html', **template_data, consumptions=consumptions)

#with app.app_context():
#   @socketio.on('post_consumptions')
#   def post_consumptions(json):
      #consumptions = statistics.consumption.get_daily_consumptions('Office', 'Omar Bamarouf')
   #   socketio.emit('get_consumptions', {'data': 1})

#      print('sent consumptions')
with app.app_context():
   def post_consumptions(json):
      print('sent consumptions')

   socketio.on_event('post_consumptions', post_consumptions)



@app.route('/employee/assets/<path:path>')
@app.route('/employees/assets/<path:path>')
@app.route('/location/assets/<path:path>')
@app.route('/locations/assets/<path:path>')
@app.route('/statistics/assets/<path:path>')
def static_files_send(path):    
    return app.send_static_file(path)

@app.route('/<path:path>')
def serve_file_in_dir(path):
    #return send_from_directory(app.static_folder, path)
    return app.send_static_file(path)


@app.route("/LCD_Write/")
def LCD_write():  
   mqttc.publish("LCD/write", "OMAR IS BOSS")

   for i in range(21):
      time.sleep(0.25)
      mqttc.publish("LCD/write", "OMAR IS BOSS " + str(i))

   print("Written to LCD")

   template_data = get_template_data(None, None)
   return render_template('wifi-data.html', **template_data, pins=pins)


#@socketio.on('my event')
#def handle_my_custom_event(json):
#    print('received json data here: ' + str(json))


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

   template_data = get_template_data(None, None)
   return render_template('wifi-data.html', **template_data, pins=pins)
