import json
import time

while True:
    path = json.load(open("./path.json"))
    points = path["features"][0]["geometry"]["coordinates"]
    last_long, last_lat = points[-1]
    points.append([last_long + 0.001, last_lat + 0.001])
    f = open("./path.json", "w")
    f.write(json.dumps(path))
    f.close()
    time.sleep(1)

