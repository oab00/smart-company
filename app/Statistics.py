
import sqlite3 as sql

class Statistics:
    def __init__(self):
        self.consumption = Consumption()
        self.performance = Performance()


class Consumptions:
    def __init__(self):
        self.consumptions = []
        self.initialize_consumptions()

    def initialize_consumptions(self):
        with sql.connect("database.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM CONSUMPTIONS")
            consumptions = cur.fetchall()
            
            for cons in consumptions:
                consumption = Consumption(cons['CONSUMPTION_ID'], 
                                          cons['DATE'],
                                          cons['LED_CONSUMPTION'],
                                          cons['AC_CONSUMPTION'],
                                          cons['PC_CONSUMPTION'],
                                          cons['LOCATION_NAME'],
                                          cons['EMPLOYEE_NAME'])

                self.consumptions.append(cons)

class Consumption:
    def __init__(CONSUMPTION_ID, DATE, LED_CONSUMPTION, AC_CONSUMPTION,
                 PC_CONSUMPTION, LOCATION_NAME, EMPLOYEE_NAME):
        self.id = CONSUMPTION_ID
        date = DATE.split(' ')
        self.date = date[0]
        self.time = date[1]
        self.LED = LED_CONSUMPTION
        self.AC = AC_CONSUMPTION
        self.PC = PC_CONSUMPTION
        self.location = LOCATION_NAME
        self.employee = EMPLOYEE_NAME
        

class Performances:
    def __init__(self):
        self.performances = []
        self.initialize_performances()

    def initialize_performances(self):
        pass

class Performance:
    def __init__()
        pass