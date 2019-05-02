
import sqlite3 as sql
from datetime import datetime

class LogicSystem:
    def __init__(self, socketio, mqttc):
        self.socketio = socketio
        self.mqttc = mqttc

        self.office = None
        self.locations = []
        self.initalize_locations()

        self.employees = []
        self.initialize_employees()

        self.rfids = RFIDs()


    def initalize_locations(self):
        locations = ["Outside", "On Campus", "Office", 
                    "Meeting Room", "Mosque", "Coffee Shop", "Restroom"]
        
        for loc in locations:
            rfid_code = "RFID/{}".format(loc.replace(' ', ''))

            if loc == "Office":
                location = Office(loc, rfid_code, self)
                self.office = location
            else:
                location = Location(loc, rfid_code)
                
            self.locations.append(location)


    def initialize_employees(self):
        with sql.connect("database.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM EMPLOYEES")
            employees = cur.fetchall()
            
            outside = self.get_location("Outside")

            for emp in employees:
                employee = Employee(emp['EMPLOYEE_NAME'], 
                                    emp['EMPLOYEE_STATUS'],
                                    emp['RFID_CARD_ID'],
                                    emp['LOCATION_NAME'])


                employee.pref_temp = emp['PREF_TEMPERATURE']
                employee.pref_light = emp['PREF_LIGHT']
                
                self.employees.append(employee)
                outside.employees.append(employee)

            # the first employee is the main emplyee
            self.office.employee = self.employees[0]
            #print('Main Office:', self.office.employee.name)

            


    def get_employee(self, emp_name):
        for emp in self.employees:
            if emp.name == emp_name:
                return emp
        return None

    def get_employee_by_rfid(self, cardID):
        for emp in self.employees:
            if emp.cardID == cardID:
                return emp
        return None

    def get_location(self, loc_name):
        for loc in self.locations:
            if loc.name == loc_name:
                return loc
        return None

    def rfid_reading(self, cardID, location):
        employee = ''
        for emp in self.employees:
            if emp.cardID == cardID:
                employee = emp
                break
        if employee == '':
            print("Couldn't find employee") 
            return
        
        current_location = ''
        for loc in self.locations:
            if loc.name == location:
                current_location = loc
                break
        if current_location == '':
            print("Couldn't find location")
            return
        
        self.register_rfid_event(employee, current_location)


    def register_rfid_event(self, employee, location):
        #print('register: ', employee.name, location.name)

        if not employee.locations[location.name]: # If Entering a Room  
            # Check if employee is inside one of the rooms
            if not employee.location == "Outside" and not employee.location == "On Campus":
                print("{} can't get to {} because he's inside {}".format(employee.name,
                                                                    location.name, employee.location))
                return False

            # Can't enter any room unless on campus
            if not location.name == "Outside" and not employee.location == "On Campus" and not location.name == "On Campus":
                print("{} can't get to {} becaue he's not On Campus".format(employee.name, location.name))
                return False

            old_location = self.get_location(employee.location)
            #print('woof', old_location.name, [employee.name for employee in old_location.employees])
            #print(old_location.name, [emp.name for emp in old_location.employees])
            old_location.employees.remove(employee)
            #print('woof', old_location.name, [employee.name for employee in old_location.employees])
            employee.locations[location.name] = True
            #print('nani', location.name)
            location.employees.append(employee)

            #print("{} : {}".format(location.name, location.get_number_of_visitors()))
            employee.location = location.name

            current_location = location.name
            is_in = ' in '
            if current_location == 'On Campus':
                current_location = 'Gate'
                is_in = ' '
            if current_location == 'Outside':
                is_in = ' '
            if current_location == 'Meeting Room':
                employee.status = 'Busy'
                print("{}'s status set to Busy".format(employee.name))

            print("\033[1;36;40m{}\033[0;37;40m has\033[1;32;40m entered\033[0;37;40m the \033[1;33;40m{}\033[0;37;40m and is now{}\033[1;33;40m{}\033[0;37;40m".format(employee.name, current_location, is_in, location.name))

            self.socketio.emit('refresh', {})

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO RFIDS (EMPLOYEE_NAME, RFID_CARD_ID, RFID_LOCATION, RFID_STATUS)
                           VALUES ('{}', '{}', '{}', 'Enter');'''.format( employee.name,
                                                                          employee.cardID,
                                                                          location.name))
                con.commit()
            return True

        else:
            if location.name == "On Campus" and not employee.location == "On Campus": 
                print("{} can't get Outside because he's inside {}".format(employee.name, employee.location))
                return False

            employee.locations[location.name] = False
            location.employees.remove(employee)
            if location.name == 'Meeting Room':
                employee.status = 'Available'
                print("{}'s status set to Available".format(employee.name))

            current_location = ''
            if location.name == 'On Campus':
                current_location = 'Gate'
                employee.location = 'Outside'
            else:
                current_location = location.name
                employee.location = 'On Campus'
            

            new_location = self.get_location(employee.location)
            new_location.employees.append(employee)

            print("\033[1;36;40m{}\033[0;37;40m has\033[1;31;40m left\033[0;37;40m the \033[1;33;40m{}\033[0;37;40m and is now \033[1;33;40m{}\033[0;37;40m".format(employee.name, current_location, employee.location))

            self.socketio.emit('refresh', {})

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO RFIDS (EMPLOYEE_NAME, RFID_CARD_ID, RFID_LOCATION, RFID_STATUS)
                           VALUES ('{}', '{}', '{}', 'Leave');'''.format( employee.name,
                                                                          employee.cardID,
                                                                          location.name))
                con.commit()
            return True


    def office_rfid_reading(self, cardID):
        self.office.rfid_reading(cardID)




class Employee:
    def __init__(self, name, status, cardID, location):
        self.name = name
        self.status = status
        self.cardID = cardID
        self.location = location
        self.pref_temp = 24.0
        self.pref_light = "MED"
        self.locations = { # False = Leave , True = Enter
            "Outside": True,
            "On Campus": False,
            "Office": False,
            "Meeting Room": False,
            "Mosque": False,
            "Coffee Shop": False,
            "Bathroom": False
        }  


class Location:
    def __init__(self, name, rfid_code):
        self.name = name
        self.rfid_code = rfid_code
        self.visitors = 0
        self.employees = []

    def get_num_of_visitors(self):
        return len(self.employees) + self.visitors


class Office(Location):
    def __init__(self, name, rfid_code, logicSystem):
        self.employee = None # Default Employee
        self.logicSystem = logicSystem
        Location.__init__(self, name, rfid_code)

    def rfid_reading(self, cardID):
        # check if employee's office
        employee = self.logicSystem.get_employee_by_rfid(cardID)

        if employee.cardID == self.employee.cardID:
            
            if not employee.locations['Office']: # If Entering Office
                # Turn System On Based on Preference
                
                if not employee.location == 'On Campus':
                    print(self.employee.name, "can't enter his Office because he's not On Campus.")
                    return
                
                onCampus = self.logicSystem.get_location("On Campus")
                onCampus.employees.remove(self.employee)
                employee.locations['On Campus'] = False
                self.employees.append(self.employee)
                employee.locations['Office'] = True
                employee.location = 'Office'

                with sql.connect("database.db") as con:
                    cur = con.cursor()
                    cur.execute('''INSERT INTO RFIDS (EMPLOYEE_NAME, RFID_CARD_ID, RFID_LOCATION, RFID_STATUS)
                            VALUES ('{}', '{}', '{}', 'Enter');'''.format( self.employee.name,
                                                                            self.employee.cardID,
                                                                            "Office"))
                    con.commit()
                    
                
                self.logicSystem.socketio.emit('refresh', {})
                print("\033[1;36;40m{}\033[0;37;40m has\033[1;32;40m entered\033[0;37;40m their \033[1;33;40mOffice\033[0;37;40m".format(employee.name))

                # Turn On Ultrasonic
                pref_light = self.employee.pref_light
                self.logicSystem.mqttc.publish("ULTRASONIC2", pref_light)
                print('Office LEDS turned on to', pref_light)

            else: # If Leaving Office

                self.employees.append(self.employee)
                employee.locations['Office'] = False
                onCampus = self.logicSystem.get_location("On Campus")
                onCampus.employees.append(self.employee)
                employee.locations['On Campus'] = True
                employee.location = 'On Campus'

                with sql.connect("database.db") as con:
                    cur = con.cursor()
                    cur.execute('''INSERT INTO RFIDS (EMPLOYEE_NAME, RFID_CARD_ID, RFID_LOCATION, RFID_STATUS)
                            VALUES ('{}', '{}', '{}', 'Leave');'''.format( self.employee.name,
                                                                            self.employee.cardID,
                                                                            "Office"))
                    con.commit()
                
                self.logicSystem.socketio.emit('refresh', {})
                print("\033[1;36;40m{}\033[0;37;40m has\033[1;31;40m left\033[0;37;40m their \033[1;33;40mOffice\033[0;37;40m".format(employee.name))

                self.logicSystem.mqttc.publish("ULTRASONIC2", "OFF")
                print('Office LEDS turned OFF')
            

        else:
            other_employee = employee
            rfid_register = self.logicSystem.register_rfid_event(other_employee, self)

            if not rfid_register:
                return

            # If Entering
            if other_employee.location == 'Office':
                # Check if Main Employee not in Office
                if not self.employee.location == 'Office':
                    # Turn System On Based on Defaults
                    # Default Light = Medium
                    # Default Temperature = 24C
                    self.logicSystem.mqttc.publish("ULTRASONIC2", "MED")
                    print('Office LEDS turned MED')
                else:
                    other_employee.status = 'Busy'
                    print("{}'s status set to Busy".format(other_employee.name))
                    if len(self.employees) <= 2:
                        self.employee.status = 'Busy'
                        print("{}'s status set to Busy".format(self.employee.name))

            else: # If Leaving
                # Check if Main Employee not in Office
                if not self.employee.location == 'Office':
                    self.logicSystem.mqttc.publish("ULTRASONIC2", "OFF")
                    print('Office LEDS turned OFF')
                else:
                    other_employee.status = 'Available'
                    print("{}'s status set to Available".format(other_employee.name))
                    # Check if there are other employees in office
                    if len(self.employees) <= 1:
                        self.employee.status = 'Available'
                        print("{}'s status set to Available".format(self.employee.name))


    def set_visitors(self, status):
        visitors = self.visitors
        if status == "INCREASE":
            self.visitors = visitors + 1
        elif status == "DECREASE":
            if visitors > 0:
                self.visitors = visitors - 1
            
            elif visitors == 0:
                # EmployeeStatus = "Available"
                self.employee.status = "Available"


class RFIDs:
    def __init__(self):
        pass
    
    def get_rfids_for_employee(self, employee):
        with sql.connect("database.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM RFIDS WHERE EMPLOYEE_NAME = '{}';".format(employee.name))
            rfid_readings = cur.fetchall()

            rfids = []
            count = 1
            for reading in rfid_readings:
                date_time = reading['DATETIME'].split(' ')
                rfid = {
                        'count': count,
                        'date': date_time[0],
                        'time': date_time[1],
                        'location': reading['RFID_LOCATION'], 
                        'status':   reading['RFID_STATUS']
                        }
                rfids.append(rfid)
                count = count + 1

            return rfids

    def get_rfids_for_location(self, location):
        with sql.connect("database.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM RFIDS WHERE RFID_LOCATION = '{}';".format(location.name))
            rfid_readings = cur.fetchall()

            rfids = []
            count = 1
            for reading in rfid_readings:
                date_time = reading['DATETIME'].split(' ')
                rfid = {
                        'count': count,
                        'date': date_time[0],
                        'time': date_time[1],
                        'employee': reading['EMPLOYEE_NAME'], 
                        'status':   reading['RFID_STATUS']
                        }
                rfids.append(rfid)
                count = count + 1

            return rfids
                