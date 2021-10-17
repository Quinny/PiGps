import math

def degrees_to_radians(degree):
  return degree * (math.pi/180)

# https://en.wikipedia.org/wiki/Haversine_formula
def get_distance_in_km(lon1, lat1, lon2, lat2):
    R = 6371; # Radius of the earth in km
    d_lat = degrees_to_radians(lat2 - lat1)
    d_lon = degrees_to_radians(lon2 - lon1)
    a = (
        math.sin(d_lat/2) * math.sin(d_lat/2) +
        math.cos(degrees_to_radians(lat1)) * math.cos(degrees_to_radians(lat2)) *
        math.sin(d_lon/2) * math.sin(d_lon/2)
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a));
    d = R * c
    return d

class PathStats:
    def __init__(self, path):
        self.total_distance_km = self._get_total_distance_km(path)

    def _get_total_distance_km(self, path):
        distance = 0
        last_point = path[0]
        for point in path[1:]:
            distance += get_distance_in_km(
                    last_point.longitude, last_point.latitude,
                    point.longitude, point.latitude
            )
            last_point = point
        return distance

    def json(self):
        return [{
            "name": "Total Distance (Kilometers)",
            "value": round(self.total_distance_km, 2),
        }]
