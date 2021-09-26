import io
import pynmea2
import serial
from collections import namedtuple

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

Coordinate = namedtuple('Coordinate', ['longitude', 'latitude'])

class GpsDevice:
    def __init__(self):
        ser = serial.Serial('/dev/ttyS0', 9600, timeout=5.0)
        self.serial_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

    def poll_location(self):
        while True:
            line = self.serial_io.readline()
            msg = pynmea2.parse(line)
            if type(msg) is pynmea2.GGA:
                return Coordinate(
                        longitude=nmea_to_decimal(msg.lon, msg.lon_dir),
                        latitude=nmea_to_decimal(msg.lat, msg.lat_dir)
                )

class MockGpsDevice:
    def __init__(self):
        self.current_latitude = 48.8584
        self.current_longitude = 2.2945

    def poll_location(self):
        self.current_longitude += 0.0001
        self.current_latitude += 0.0001
        return Coordinate(
            longitude=self.current_longitude,
            latitude=self.current_latitude
        )
