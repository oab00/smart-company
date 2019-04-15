PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
COMMIT;

CREATE TABLE EMPLOYEES (
    EMPLOYEE_NAME TEXT PRIMARY KEY UNIQUE,
    EMPLOYEE_STATUS TEXT check("EMPLOYEE_STATUS" in ('Available', 'Busy', 'OnCampus', 'OffCampus', 'OnBreak', 'InMeeting')),
    PREF_TEMPERATURE REAL,
    PREF_LIGHT REAL,
    RFID_CARD_ID TEXT,
    LOCATION_NAME TEXT,
    FOREIGN KEY(LOCATION_NAME) REFERENCES LOCATIONS(LOCATION_NAME)
);

CREATE TABLE RFIDS (
    RFID_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DATETIME DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    RFID_LOCATION TEXT check("RFID_LOCATION" in ('Gate', 'Meeting Room', 'Office', 'Mosque', 'Coffee Shop', 'Rest Room')),
    RFID_STATUS TEXT check("RFID_STATUS" in ('Enter', 'Leave')),
    RFID_CARD_ID TEXT,
    EMPLOYEE_NAME TEXT,
    LOCATION_NAME TEXT,
    FOREIGN KEY(EMPLOYEE_NAME) REFERENCES EMPLOYEE(EMPLOYEE_NAME),
    FOREIGN KEY(LOCATION_NAME) REFERENCES LOCATIONS(LOCATION_NAME)
);

CREATE TABLE LOCATIONS (
    LOCATION_NAME TEXT PRIMARY KEY UNIQUE,
    RFID_CODE TEXT UNQIUE,
    VISITORS INTEGER
);



CREATE TABLE SENSORS (
    SENSOR_NAME TEXT PRIMARY KEY UNIQUE,
    SENSOR_VALUE1 REAL,
    SENSOR_VALUE2 REAL
);