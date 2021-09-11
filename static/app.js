let map;

function initMap() {
  // set up the map
  map = new google.maps.Map(document.getElementById("map"), {
    center: new google.maps.LatLng(0, 0),
    zoom: 4,
  });
}

function loadGeoJsonString(geoString) {
  const geojson = JSON.parse(geoString);
  map.data.addGeoJson(geojson);
  zoom(map);
}

/**
 * Update a map's viewport to fit each geometry in a dataset
 */
function zoom(map) {
  const bounds = new google.maps.LatLngBounds();
  map.data.forEach((feature) => {
    const geometry = feature.getGeometry();
    if (geometry) {
      processPoints(geometry, bounds.extend, bounds);
    }
  });
  map.fitBounds(bounds);
}

/**
 * Process each point in a Geometry, regardless of how deep the points may lie.
 */
function processPoints(geometry, callback, thisArg) {
  if (geometry instanceof google.maps.LatLng) {
    callback.call(thisArg, geometry);
  } else if (geometry instanceof google.maps.Data.Point) {
    callback.call(thisArg, geometry.get());
  } else {
    geometry.getArray().forEach((g) => {
      processPoints(g, callback, thisArg);
    });
  }
}

function updateMap() {
    fetch("./static/path.json")
      .then(response => response.text())
      .then(loadGeoJsonString);
}

function initialize() {
  initMap();
  updateMap();
  setInterval(updateMap, 3000);
}