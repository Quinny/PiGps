import io
import pynmea2
import serial
import sqlite3
import gpsdevice
import sys

if len(sys.argv) > 1 and sys.argv[1] == "mock":
    gps = gpsdevice.MockGpsDevice()
else:
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
        location.update({"path_id": 0})
        execute_write_query("add_point.sql", location)
    except Exception as e:
        print('Exception: {} {}'.format(type(e), e))
