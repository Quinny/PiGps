from flask import Flask, render_template
from . import keys

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", maps_api_key=keys.google_maps_api_key)
