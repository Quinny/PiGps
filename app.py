from . import keys
from flask import Flask, render_template, g, jsonify
import sqlite3
from . import pathstore

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
    points = get_store().get_path(path_id)
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
