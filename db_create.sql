PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
COMMIT;

CREATE TABLE EMPLOYEES (
    EMPLOYEE_NAME TEXT PRIMARY KEY UNIQUE,
    EMPLOYEE_STATUS TEXT check("EMPLOYEE_STATUS" in ('Available', 'Busy', 'OnCampus', 'Outside', 'OnBreak', 'InMeeting')),
    PREF_TEMPERATURE REAL DEFAULT 24.0,
    PREF_LIGHT REAL DEFAULT "MED" check("PREF_LIGHT" in ("HIGH", "MED", "LOW", "OFF")),
    RFID_CARD_ID TEXT,
    LOCATION_NAME TEXT,
    FOREIGN KEY(LOCATION_NAME) REFERENCES LOCATIONS(LOCATION_NAME)
);

CREATE TABLE RFIDS (
    RFID_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DATETIME DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    RFID_LOCATION TEXT check("RFID_LOCATION" in ('Outside', 'On Campus', 'Gate', 'Meeting Room', 'Office', 'Mosque', 'Coffee Shop', 'Rest Room')),
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

CREATE TABLE CONSUMPTIONS (
    CONSUMPTION_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    START_DATE DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    END_DATE DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    LED_CONSUMPTION REAL,
    AC_CONSUMPTION REAL,
    PC_CONSUMPTION REAL,
    LOCATION_NAME TEXT,
    EMPLOYEE_NAME TEXT DEFAULT NULL,
    FOREIGN KEY(LOCATION_NAME) REFERENCES LOCATIONS(LOCATION_NAME),
    FOREIGN KEY(EMPLOYEE_NAME) REFERENCES EMPLOYEE(EMPLOYEE_NAME)
);
