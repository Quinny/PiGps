import io
import pynmea2
import serial
import sqlite3

db = sqlite3.connect('points.db')
db_cursor = db.cursor()
ser = serial.Serial('/dev/ttyS0', 9600, timeout=5.0)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

# Runs a modifying SQL query locaated at `sql/{filename}` and commits the
# result.
def execute_write_query(filename, variables = {}):
    db_cursor.execute(open("sql/" + filename, "r").read(), variables)
    db.commit()

# The format for NMEA coordinates is (d)ddmm.mmmm
# where d=degrees and m=minutes (http://aprs.gids.nl/nmea/#latlong)
#
# There are 60 minutes in a degree, so divide the minutes by 60 and add that to
# the degrees in order to get the standard decmial format.
def nmea_to_decimal(nmea_str, direction):
    start_minutes = nmea_str.index('.') - 2
    minutes = float(nmea_str[start_minutes:])
    degrees = int(nmea_str[:start_minutes])
    # South and West are considered negative coordinates.
    multipler = -1 if direction in ['W', 'S'] else 1
    return (degrees + (minutes / 60.0)) * multipler

execute_write_query("create_db.sql")

while 1:
    try:
        line = sio.readline()
        msg = pynmea2.parse(line)
        if type(msg) is pynmea2.GGA:
            execute_write_query("add_point.sql", {
                "path_id": 0,
                "longitude": nmea_to_decimal(msg.lon, msg.lon_dir),
                "latitude": nmea_to_decimal(msg.lat, msg.lat_dir),
            })
    except serial.SerialException as e:
        print('Device error: {}'.format(e))
        break
    except pynmea2.ParseError as e:
        print('Parse error: {}'.format(e))
        continue