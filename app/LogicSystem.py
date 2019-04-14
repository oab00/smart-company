
import sqlite3 as sql

class LogicSystem:
    def __init__(self):
        self.gate_rfid = False
        self.db = ''
        self.initialize_database()
        self.employees = []
        self.initialize_employees()

    def initialize_database(self):
        con = sql.connect("../database.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        self.db = cur

    def initialize_employees(self):
        self.db.execute("SELECT * FROM EMPLOYEES")
        empRows = self.db.fetchall()
        print(empRows)


    def gate_rfid_reading(self, cardID):
        self.gate_rfid = not self.gate_rfid
        print(self.gate_rfid)



class Office:
    def __init__(self):
        pass


class Employee:
    def __init__(self):
        pass