import io
import pynmea2
import serial
import sqlite3
from . import gpsdevice

gps = gpsdevice.GpsDevice()
db = sqlite3.connect('points.db')
db_cursor = db.cursor()

# Runs a modifying SQL query locaated at `sql/{filename}` and commits the
# result.
def execute_write_query(filename, variables = {}):
    db_cursor.execute(open("sql/" + filename, "r").read(), variables)
    db.commit()

execute_write_query("create_db.sql")

while 1:
    try:
        location = gps.poll_location()
        execute_write_query("add_point.sql", {
            "path_id": 0,
        } + location)
    except serial.SerialException as e:
        print('Device error: {}'.format(e))
        break
    except pynmea2.ParseError as e:
        print('Parse error: {}'.format(e))
        continue
