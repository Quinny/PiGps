from flask import Flask, render_template, g, jsonify
import sqlite3
from . import pathstore
from . import keys
from . import stats

app = Flask(__name__)

def get_store():
    store = getattr(g, '_store', None)
    if store is None:
        store = pathstore.PathStore()
    return store

@app.teardown_appcontext
def close_connection(exception):
    store = getattr(g, '_store', None)
    if store is not None:
        store.close()

@app.route("/")
def index():
    return render_template("index.html", maps_api_key=keys.google_maps_api_key)

@app.route("/points")
@app.route("/points/<path_id>")
def points(path_id=None):
    path_id = path_id or get_store().get_latest_path_id()
    path = get_store().get_path(path_id)
    points = [
            [coordinate.longitude, coordinate.latitude]
            for coordinate in path
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
