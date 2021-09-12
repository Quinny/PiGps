from . import keys
from flask import Flask, render_template, g, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("points.db")
        db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template("index.html", maps_api_key=keys.google_maps_api_key)

@app.route("/points")
def points():
    points = [
        [row["longitude"], row["latitude"]]
        for row in query_db(
            "SELECT longitude, latitude FROM points ORDER BY time_recorded ASC")
    ]
    geo_json = {
        "type": "FeatureCollection",
        "features": [{
            "geometry": {
                "type": "LineString",
                "coordinates": points,
            },
            "type": "Feature",
            "properties": {},
        }]
    }
    return jsonify(geo_json)
