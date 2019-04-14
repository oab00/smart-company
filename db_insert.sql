DELETE FROM EMPLOYEES;
DELETE FROM RFIDS;
DELETE FROM LOCATIONS;


INSERT INTO EMPLOYEES (EMPLOYEE_NAME, EMPLOYEE_STATUS, RFID_CARD_ID) 
            VALUES ('Omar Bamarouf', 'Available', '8A 86 B8 73'),
                   ('Mohanned Asiri', 'OffCampus', '91 D8 9E 66');


INSERT INTO RFIDS (EMPLOYEE_ID, RFID_CARD_ID, RFID_LOCATION, RFID_STATUS)
            VALUES (1, '8A 86 B8 73', 'Gate', 'Enter'),
                   (1, '8A 86 B8 73', 'Gate', 'Leave'),
                   (1, '91 D8 9E 66', 'Office', 'Enter'),
                   (1, '91 D8 9E 66', 'Office', 'Leave');


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