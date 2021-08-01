import io

import pynmea2
import serial
from time import sleep

ser = serial.Serial('/dev/ttyS0', 9600, timeout=5.0)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

def isclose(a, b):
    return abs(a-b) < 0.00001

class GpsPath:
    def __init__(self):
        self.points = []

    def add_point(self, lat, lon):
        last_lat, last_lon = (0, 0) if len(self.points) == 0 else self.points[-1]
        if isclose(lat, last_lat) and isclose(lon, last_lon):
            return
        self.points.append((lat, lon))

def nmea_to_decimal(nmea_str, direction):
    start_minutes = nmea_str.index('.') - 2
    minutes = float(nmea_str[start_minutes:])
    degrees = int(nmea_str[:start_minutes])
    multipler = -1 if direction in ['W', 'S'] else 1
    return (degrees + (minutes / 60.0)) * multipler

path = GpsPath()
while 1:
    try:
        line = sio.readline()
        msg = pynmea2.parse(line)
        if type(msg) is pynmea2.GGA:
            path.add_point(nmea_to_decimal(msg.lat, msg.lat_dir), nmea_to_decimal(msg.lon, msg.lon_dir))
        print path.points
    except serial.SerialException as e:
        print('Device error: {}'.format(e))
        break
    except pynmea2.ParseError as e:
        print('Parse error: {}'.format(e))
        continue

