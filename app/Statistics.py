
import sqlite3 as sql

class Statistics:
    def __init__(self):
        self.consumption = Consumptions()
        self.performance = Performances()


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
                                          cons['START_DATE'],
                                          cons['END_DATE'],
                                          cons['LED_CONSUMPTION'],
                                          cons['AC_CONSUMPTION'],
                                          cons['PC_CONSUMPTION'],
                                          cons['LOCATION_NAME'],
                                          cons['EMPLOYEE_NAME'])

                self.consumptions.append(consumption)


    def get_consumptions(self):
        return self.consumptions
        

class Consumption:
    def __init__(self, CONSUMPTION_ID, START_DATE, END_DATE, LED_CONSUMPTION, 
                 AC_CONSUMPTION, PC_CONSUMPTION, LOCATION_NAME, EMPLOYEE_NAME):
        self.id = CONSUMPTION_ID

        date_start = START_DATE.split(' ')
        self.start_date = date_start[0]
        self.start_time = date_start[1]

        date_end = END_DATE.split(' ')
        self.end_date = date_end[0]
        self.end_time = date_end[1]
        
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
    def __init__(self):
        pass