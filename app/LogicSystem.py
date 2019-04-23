
import sqlite3 as sql

class LogicSystem:
    def __init__(self, socketio):
        self.socketio = socketio

        self.office = None
        self.locations = []
        self.initalize_locations()

        self.employees = []
        self.initialize_employees()


    def initalize_locations(self):
        locations = ["Outside", "On Campus", "Gate", "Office", 
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
        if not employee.locations[location.name]: # If Entering a Room  
            #print('lol', employee.name, location.name)
            # Check if employee is inside one of the rooms
            if not employee.location == "Outside" and not employee.location == "On Campus":
                print('meow')
                print("{} can't get to {} because he's inside {}".format(employee.name,
                                                                    location.name, employee.location))
                return

            old_location = self.get_location(employee.location)
            #print('woof', old_location.name, [employee.name for employee in old_location.employees])
            old_location.employees.remove(employee)
            #print('woof', old_location.name, [employee.name for employee in old_location.employees])
            employee.locations[location.name] = True
            #print('nani', location.name)
            location.employees.append(employee)

            #print("{} : {}".format(location.name, location.get_number_of_visitors()))
            employee.location = location.name

            current_location = location.name
            if current_location == 'Gate':
                current_location = 'On Campus'
                employee.location = 'On Campus'
            
            print("\033[1;36;40m{}\033[0;37;40m has\033[1;32;40m entered\033[0;37;40m the \033[1;33;40m{}\033[0;37;40m and is now \033[1;33;40m{}\033[0;37;40m".format(employee.name, location.name, current_location))

            self.socketio.emit('refresh', {})

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO RFIDS (EMPLOYEE_NAME, RFID_CARD_ID, RFID_LOCATION, RFID_STATUS)
                           VALUES ('{}', '{}', '{}', 'Enter');'''.format( employee.name,
                                                                          employee.cardID,
                                                                          location.name))
                con.commit()

        else:
            employee.locations[location.name] = False
            location.employees.remove(employee)

            current_location = ''
            if location.name == 'Gate':
                current_location = 'Outside'
                employee.location = 'Outside'
            else:
                current_location = 'On Campus'
                employee.location = 'On Campus'

            new_location = self.get_location(current_location)
            new_location.employees.append(employee)

            print("\033[1;36;40m{}\033[0;37;40m has\033[1;31;40m left\033[0;37;40m the \033[1;33;40m{}\033[0;37;40m and is now \033[1;33;40m{}\033[0;37;40m".format(employee.name, location.name, current_location))

            self.socketio.emit('refresh', {})

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO RFIDS (EMPLOYEE_NAME, RFID_CARD_ID, RFID_LOCATION, RFID_STATUS)
                           VALUES ('{}', '{}', '{}', 'Leave');'''.format( employee.name,
                                                                          employee.cardID,
                                                                          current_location))
                con.commit()

    def office_rfid_reading(self, cardID):
        self.office.rfid_reading(cardID)




class Employee:
    def __init__(self, name, status, cardID, location):
        self.name = name
        self.status = status
        self.cardID = cardID
        self.location = location
        self.pref_temp = 0.0
        self.locations = { # False = Leave , True = Enter
            "Outside": True,
            "On Campus": False,
            "Gate": False,
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
        if cardID == self.employee.cardID:
            print(self.employee.name, "has entered their office.")

            # Turn System On Based on Preference
            
            onCampus = self.logicSystem.get_location("On Campus")
            if self.employee in onCampus.employees:
                onCampus.employees.remove(self.employee)
            self.employees.append(self.employee)

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO RFIDS (EMPLOYEE_NAME, RFID_CARD_ID, RFID_LOCATION, RFID_STATUS)
                           VALUES ('{}', '{}', '{}', 'Enter');'''.format( self.employee.name,
                                                                          self.employee.cardID,
                                                                          "Office"))
                con.commit()

            # Turn On Ultrasonic
            

        else:
            other_employee = self.logicSystem.get_employee_by_rfid(cardID)
            print("{} has entered {}'s office".format(other_employee, self.employee.name))

            # Turn System On Based on Defaults
            

            # Turn On System
    # Office RFID Detected?

    # Default = [Lights:MEDIUM,Temperature:24C]
    # Preference = [Lights:Pref, Temperature:Pref]
    
    # def OfficeRFID(cardID):
    #    if cardID =! "41 24 9B 66"
    #    TurnSystemOn = Default
    #    SaveEmployeeData
    #    elif cardID == "41 24 9B 66"
    #    TurnSystemOn = Preference
    #    time.sleep(5)
    #    Ultrasonics = ON