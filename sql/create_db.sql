CREATE TABLE IF NOT EXISTS points (
	point_id INTEGER PRIMARY KEY,
	path_id INTEGER,
	longitude REAL,
	latitude REAL,
	time_recorded DATETIME DEFAULT CURRENT_TIMESTAMP
)
