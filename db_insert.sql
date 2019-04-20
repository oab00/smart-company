DELETE FROM EMPLOYEES;
DELETE FROM RFIDS;
DELETE FROM LOCATIONS;


INSERT INTO EMPLOYEES (EMPLOYEE_NAME, EMPLOYEE_STATUS, RFID_CARD_ID) 
            VALUES ('Omar Bamarouf', 'Available', '41 24 9B 66'),
                   ('Baraa Ismail', 'OffCampus', 'B9 B5 69 5');

/*
INSERT INTO RFIDS (EMPLOYEE_NAME, RFID_CARD_ID, RFID_LOCATION, RFID_STATUS)
            VALUES ('Omar Bamarouf', '41 24 9B 66', 'Gate', 'Enter'),
                   ('Omar Bamarouf', '41 24 9B 66', 'Gate', 'Leave'),
                   ('Baraa Ismail', 'B9 B5 69 5', 'Office', 'Enter'),
                   ('Baraa Ismail', 'B9 B5 69 5', 'Office', 'Leave');
*/

INSERT INTO LOCATIONS (LOCATION_NAME, RFID_CODE)
            VALUES ('Gate', 'RFID/cardID'),
                   ('Office', 'Remote_RFID/cardID'),
                   ('Mosque', 'Mosque'),
                   ('Coffee Shop', 'CoffeeShop'),
                   ('Rest Room', 'RestRoom'),
                   ('Meeting Room', 'MeetingRoom');

/* SQL Table Display:
    .mode column
    .headers on
*/