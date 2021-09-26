import io
import pynmea2
import serial
import sqlite3
import gpsdevice
import sys
import pathstore

if len(sys.argv) > 1 and sys.argv[1] == "mock":
    gps = gpsdevice.MockGpsDevice()
else:
    gps = gpsdevice.GpsDevice()

store = pathstore.PathStore()
path_id = store.get_latest_path_id() + 1
while 1:
    try:
        location = gps.poll_location()
        store.add_point(path_id, location)
    except Exception as e:
        print('Exception: {} {}'.format(type(e), e))
