

from random import random
from random import randint
from datetime import date
from datetime import timedelta
from datetime import datetime
from datetime import time


total_hours = 0
#number_of_days = ['Saturday','Sunday','Monday','Tuesday',
                #'wednesday','Thursday', 'Friday']
x = 1
#for i in number_of_days:
for j in range(100):
    for i in range(30):
        def rand_period():
            for x in [randint(0,8)]:
                hours_spent = 0
                global total_hours
                hours_spent = hours_spent + x
                total_hours = total_hours + hours_spent
                
            return hours_spent

        

        def rand_location():
            locations =  ["Office", "Meeting Room", "Mosque",
                            "Coffee Shop", "Restroom"]

            location = locations[randint(0,4)]
            return location
        


        def current_day():
            global x 
            today = date.today()
            current = date(today.year,1,x)
            return current
        print("today date is: ",current_day())
        print('Hours Spent: ', rand_period())
        print(rand_location())

        
        if total_hours >= 8:
            next_day = current_day() + timedelta(days=1)
            x = x + 1
            total_hours = 0
            break