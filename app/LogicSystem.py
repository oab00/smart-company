
import sqlite3 as sql

class LogicSystem:
    def __init__(self):
        self.db_con = ''
        self.db_cur = ''
        #self.initialize_database()
        self.employees = []
        self.initialize_employees()
        self.locations = []
        self.initalize_locations()

    def initialize_database(self):
        #self.db_con = sql.connect("database.db")
        #self.db_con.row_factory = sql.Row
        #self.db_cur = self.db_con.cursor()
        pass

    def initialize_employees(self):
        with sql.connect("database.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM EMPLOYEES")
            employees = cur.fetchall()
            for emp in employees:
                self.employees.append( Employee(emp['EMPLOYEE_NAME'], 
                                                emp['EMPLOYEE_STATUS'],
                                                emp['RFID_CARD_ID'],
                                                emp['LOCATION_NAME']) )
            #con.close()

    def initalize_locations(self):
        locations = ["Gate", "Office", "Meeting Room",
                     "Mosque", "Coffee Shop", "Restroom"]
        
        for loc in locations:
            rfid_code = "RFID/{}".format(loc.replace(' ', ''))
            self.locations.append(Location(loc, rfid_code))


    def gate_rfid_reading(self, cardID, location):
        employee = ''
        for emp in self.employees:
            if emp.cardID == cardID:
                employee = emp
        
        current_location = ''
        for loc in self.locations:
            if loc.name == location:
                current_location = loc
        
        #print("{} ? {}".format(employee.name, current_location.name))
        self.register_rfid_event(employee, current_location)




    def register_rfid_event(self, employee, location):
        if employee.locations[location.name] == False: # If Leave
            employee.locations[location.name] = True
            location.employees.append(employee)
            
            print("{} has entered the {}".format(employee.name, location.name))

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO RFIDS (EMPLOYEE_NAME, RFID_CARD_ID, RFID_LOCATION, RFID_STATUS)
                           VALUES ('{}', '{}', '{}', 'Enter');'''.format( employee.name,
                                                                          employee.cardID,
                                                                          location.name))
                con.commit()

        else:
            employee.locations[location.name] = False
            location.employees.append(employee)

            print("{} has left the {}".format(employee.name, location.name))

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO RFIDS (EMPLOYEE_NAME, RFID_CARD_ID, RFID_LOCATION, RFID_STATUS)
                           VALUES ('{}', '{}', '{}', 'Leave');'''.format( employee.name,
                                                                          employee.cardID,
                                                                          location.name))
                con.commit()



class Location:
    def __init__(self, name, rfid_code):
        self.name = name
        self.rfid_code = rfid_code
        self.visitors = 0
        self.employees = []


class Employee:
    def __init__(self, name, status, cardID, location):
        self.name = name
        self.status = status
        self.cardID = cardID
        self.location = location
        self.locations = { # False = Leave , True = Enter
            "Gate": False,
            "Office": False,
            "MeetingRoom": False,
            "Mosque": False,
            "CoffeeShop": False,
            "Bathroom": False
        }

    


class Office:
    def __init__(self):
        pass
