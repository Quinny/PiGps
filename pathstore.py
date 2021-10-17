import io
import pynmea2
import serial
import sqlite3
import sys
from datetime import datetime
from collections import namedtuple

Coordinate = namedtuple('Coordinate', ['longitude', 'latitude', 'time_recorded'])

class PathStore:
    def __init__(self):
        self.db = sqlite3.connect(
                'points.db',
                detect_types=sqlite3.PARSE_DECLTYPES
        )
        self.db.row_factory = sqlite3.Row
        self.db_cursor = self.db.cursor()
        self._execute_write_query("create_db.sql")

    # Runs a modifying SQL query locaated at `sql/{filename}` and commits the
    # result.
    def _execute_write_query(self, filename, variables = {}):
        self.db_cursor.execute(open("sql/" + filename, "r").read(), variables)
        self.db.commit()

    def _execute_read_query(self, query, variables={}, one=False):
        cur = self.db.execute(query, variables)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    def add_point(self, path_id, coordinate):
        self._execute_write_query("add_point.sql", {
            "path_id": path_id,
            "longitude": coordinate.longitude,
            "latitude": coordinate.latitude,
        })

    def get_latest_path_id(self):
        return self._execute_read_query(
                "SELECT max(path_id) as id FROM points",
                one=True
        )["id"] or 0

    def get_path(self, path_id):
        row_set = self._execute_read_query(("""
                SELECT
                    longitude, latitude, time_recorded
                FROM
                    points
                WHERE
                    path_id=:path_id
                ORDER BY
                    time_recorded
                ASC
            """), {"path_id": path_id})
        return [
            Coordinate(
                longitude=row["longitude"],
                latitude=row["latitude"],
                time_recorded=datetime.strptime(
                        row["time_recorded"],
                        '%Y-%m-%d %H:%M:%S'
                )
            )
            for row in row_set
        ]

    def close(self):
        self.db.commit()
        self.db_cursor.close()
        self.db.close()
