
from random import random, randint
from datetime import date, timedelta, datetime, time
import sqlite3 as sql


locations =  ["Office", "Meeting Room", "Mosque",
                "Coffee Shop", "Restroom"]
def rand_location():
    location = locations[randint(0,4)]
    return location


first_day = date.today()
year = first_day.year
days = 0

consumptions = []
#for i in number_of_days:
for i in range(30):
    
    today  = date(year, 1, first_day.day + days)
    today_str = today.strftime('%Y-%m-%d')
    total = 0

    while total < 8:


        start_time = '{}:00:00'.format(8 + total)

        hours = randint(1,8)

        if total + hours > 8:
            hours = -(total - 8)
            total = total + hours
        else:
            total += hours

        end_time = "{}:00:00".format(8 + total)

        location = rand_location()
        employee = None
        if location == 'Office' or location == 'Meeting Room':
            employee = 'Omar Bamarouf'

        consumptions.append('''('{0} {1}', '{0} {2}', 15, 900, 180, '{3}', '{4}'),'''.format(
                                                today_str, start_time, end_time, location, employee))
        if total >= 8:
            days = days + 1
            total_hours = 0
            break

datastring = '''INSERT INTO CONSUMPTIONS (START_DATE, END_DATE, LED_CONSUMPTION, AC_CONSUMPTION, 
                          PC_CONSUMPTION, LOCATION_NAME, EMPLOYEE_NAME) VALUES '''

for con in consumptions:
    #print(con)
    datastring  = datastring + con

datastring = datastring[:-1] + ';'

with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute(datastring)
    con.commit()