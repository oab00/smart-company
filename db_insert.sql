DELETE FROM EMPLOYEES;
DELETE FROM RFIDS;
DELETE FROM LOCATIONS;
DELETE FROM CONSUMPTIONS;

/* SQL Table Display:
    .mode column
    .headers on
*/

INSERT INTO EMPLOYEES (EMPLOYEE_NAME, EMPLOYEE_STATUS, RFID_CARD_ID, LOCATION_NAME) 
            VALUES ('Omar Bamarouf', 'Available', '41 24 9B 66', 'Outside'),
                   ('Baraa Ismail', 'Available', 'B9 B5 69 05', 'Outside'),
                   ('Raed Al-Harthi', 'Available', '90 A2 42 83', 'Outside'),
                   ('Ibrahim Hasan', 'Available', '?? ?? ?? ??', 'Outside'),
                   ('Mohanned Asiri', 'Available', '?? ?? ?? ??', 'Outside');


INSERT INTO LOCATIONS (LOCATION_NAME, RFID_CODE)
            VALUES ('Outside', NULL),
                   ('On Campus', NULL),
                   ('Gate', 'RFID/cardID'),
                   ('Office', 'Remote_RFID/cardID'),
                   ('Mosque', 'Mosque'),
                   ('Coffee Shop', 'CoffeeShop'),
                   ('Rest Room', 'RestRoom'),
                   ('Meeting Room', 'MeetingRoom');


INSERT INTO CONSUMPTIONS (START_DATE, END_DATE, LED_CONSUMPTION, AC_CONSUMPTION, 
                          PC_CONSUMPTION, LOCATION_NAME, EMPLOYEE_NAME)
            VALUES ('2019-04-29 8:00:00', '2019-04-29 10:00:00', 15, 900, 180, 'Office', 'Omar Bamarouf'),
                   ('2019-04-29 10:00:00', '2019-04-29 12:00:00', 15, 900, 180, 'Meeting Room', NULL),
                   ('2019-04-29 13:00:00', '2019-04-29 16:00:00', 15, 900, 180, 'Office', 'Omar Bamarouf'),

                   ('2019-04-30 8:00:00', '2019-04-30 11:00:00', 15, 900, 180, 'Office', 'Omar Bamarouf'),
                   ('2019-04-30 12:00:00', '2019-04-30 13:00:00', 15, 900, 180, 'Office', 'Omar Bamarouf'),
                   ('2019-04-30 13:00:00', '2019-04-30 16:00:00', 15, 900, 180, 'Meeting Room', NULL),

                   ('2019-05-1 8:00:00', '2019-05-1 9:00:00', 15, 900, 180, 'Office', 'Omar Bamarouf'),
                   ('2019-05-1 10:00:00', '2019-05-1 12:00:00', 15, 900, 180, 'Meeting Room', NULL),
                   ('2019-05-1 13:00:00', '2019-05-1 14:00:00', 15, 900, 180, 'Office', 'Omar Bamarouf'),
                   ('2019-05-1 15:00:00', '2019-05-1 16:00:00', 15, 900, 180, 'Office', 'Omar Bamarouf');
