import csv
import pymysql.cursors
import requests
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

conn = pymysql.connect(
	host=os.getenv("MYSQL_HOST"),
	port=int(os.getenv("MYSQL_PORT")),
	user=os.getenv("MYSQL_USER"),
	password=os.getenv("MYSQL_PASSWORD"),
	database="squiggy",
	cursorclass=pymysql.cursors.DictCursor,
	autocommit=True
)

cursor: pymysql.cursors.DictCursor = conn.cursor()
cursor.execute(
"""
	CREATE TABLE IF NOT EXISTS Enhancements (
		id INT UNSIGNED PRIMARY KEY,
		faction_id VARCHAR(4),
		name TEXT,
		cost SMALLINT UNSIGNED,
		detachment TEXT,
		legend TEXT,
		description TEXT
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Enhancements.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		continue

	id = int(row[0])
	cost = int(row[3])

	cursor.execute(
	"""
	INSERT INTO Enhancements (
		id, faction_id, name, cost, detachment, legend, description
	)
	VALUES (%s, %s, %s, %s, %s, %s, %s)
	ON DUPLICATE KEY UPDATE 
		faction_id = VALUES(faction_id),
		name = VALUES(name),
		cost = VALUES(cost),
		detachment = VALUES(detachment),
		legend = VALUES(legend),
		description = VALUES(description);
	""",
		(id, row[1], row[2], cost, row[4], row[5], row[6])
	)

cursor.close()
conn.close()