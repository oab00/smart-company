
import sqlite3 as sql

class LogicSystem:
    def __init__(self):
        self.db = ''
        self.initialize_database()
        self.employees = []
        self.initialize_employees()

    def initialize_database(self):
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        self.db = cur

    def initialize_employees(self):
        self.db.execute("SELECT * FROM EMPLOYEES")
        employees = self.db.fetchall()
        for emp in employees:
            #print(emp['EMPLOYEE_NAME'])
            print(emp)
            self.employees = Employee(emp['EMPLOYEE_NAME'], 
                                      emp['EMPLOYEE_STATUS'],
                                      emp['RFID_CARD_ID'],
                                      emp['LOCATION_NAME'])



    def gate_rfid_reading(self, cardID):
        pass



class Office:
    def __init__(self):
        pass


class Employee:
    def __init__(self, name, status, cardID, location):
        self.name = name
        self.status = status
        self.cardID = cardID
        self.location = location

    
    def RFID_reading(self, cardID):
        pass