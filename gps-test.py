import io
import pynmea2
import serial
import sqlite3

db = sqlite3.connect('points.db')
db_cursor = db.cursor()
ser = serial.Serial('/dev/ttyS0', 9600, timeout=5.0)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

def execute_write_query(filename, variables = {}):
    db_cursor.execute(open("sql/" + filename, "r").read(), variables)
    db.commit()

def nmea_to_decimal(nmea_str, direction):
    start_minutes = nmea_str.index('.') - 2
    minutes = float(nmea_str[start_minutes:])
    degrees = int(nmea_str[:start_minutes])
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
