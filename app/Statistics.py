
import sqlite3 as sql
from datetime import timedelta

class Statistics:
    def __init__(self):
        self.consumption = Consumptions()
        self.performance = Performances(self.consumption)


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


    def get_daily_consumptions(self, location, employee=None):
        daily_consumptions = {}

        # for each consumption period
        for con in self.consumptions:
            if con.date not in daily_consumptions:
                daily_consumptions[con.date] = {}
                daily_consumptions[con.date]['hours'] = 0

            if location == con.location and employee == con.employee:
                # add hours to dictionary
                daily_consumptions[con.date]['hours'] += con.get_hours()

        # for each date get kWh consumption and price
        for date, consumption in daily_consumptions.items():
            hours = consumption['hours']
            lights_wattage = 12 * 3 # make this based on preference
            ac_wattage = 900    # air conditioner
            pc_wattage = 180    # personal computer

            wattage = lights_wattage + ac_wattage + pc_wattage

            # Formula: *Wattage * Hours Used) / 1000 * Price per kWh
            kWh = (wattage * hours) / 1000.0
            price = kWh * 0.20

            #print(date + " -> ", hours, kWh, round(price, 2))
            daily_consumptions[date]['kWh'] = kWh
            daily_consumptions[date]['price'] = price

        return daily_consumptions
        

class Consumption:
    def __init__(self, CONSUMPTION_ID, START_DATE, END_DATE, LED_CONSUMPTION, 
                 AC_CONSUMPTION, PC_CONSUMPTION, LOCATION_NAME, EMPLOYEE_NAME):
        self.id = CONSUMPTION_ID

        date_start = START_DATE.split(' ')
        self.date = date_start[0]
        self.start_time = date_start[1]

        date_end = END_DATE.split(' ')
        self.end_time = date_end[1]
        
        self.LED = LED_CONSUMPTION
        self.AC = AC_CONSUMPTION
        self.PC = PC_CONSUMPTION
        self.location = LOCATION_NAME
        self.employee = EMPLOYEE_NAME
        
    def get_hours(self):
        t1 = self.start_time.split(':')
        start_time = timedelta(hours=int(t1[0])) #, minutes=t1[1], seconds=t1[2])

        t2 = self.end_time.split(':')
        end_time = timedelta(hours=int(t2[0]))

        time_difference = str(end_time - start_time).split(':')
        hours = 0

        try:
            hours = int(time_difference[0])
        except:
            time_difference = str(start_time - end_time).split(':')
            hours = int(time_difference[0])

        #print(self.date, end_time, start_time, 'time:', time_difference[0])

        return hours

class Performances:
    def __init__(self, consumptions):
        self.performances = []
        self.consumptions = consumptions.consumptions

    def get_daily_performances(self, employee):
        daily_performances = {}

        for con in self.consumptions:
            if con.date not in daily_performances:
                daily_performances[con.date] = {}
                daily_performances[con.date]['office_hours'] = 0
                daily_performances[con.date]['meeting_hours'] = 0

            if con.location == 'Office':
                daily_performances[con.date]['office_hours'] += con.get_hours()
            elif con.location == 'Meeting Room':
                daily_performances[con.date]['meeting_hours'] += con.get_hours()

        for date, perform in daily_performances.items():
            office_hours = perform['office_hours']
            meeting_hours = perform['meeting_hours']

            office_coefficient = 0.1125  # maximum 90%
            meeting_coefficient = 0.125  # maximum 100%

            performance = office_coefficient * office_hours + meeting_coefficient * meeting_hours
            
            daily_performances[date]['performance'] = performance

        return daily_performances