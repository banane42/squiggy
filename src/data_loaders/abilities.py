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
	CREATE TABLE IF NOT EXISTS abilities (
		id INT UNSIGNED,
		name VARCHAR(64) NOT NULL,
		legend TEXT,
		faction_id VARCHAR(4),
		description TEXT,
		PRIMARY KEY (id, faction_id),
		FOREIGN KEY (faction_id) REFERENCES factions(id)
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Abilities.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		continue

	id = int(row[0])
	faction_id = row[3]
	if faction_id == "":
		faction_id = "CORE"

	cursor.execute(
	"""
		INSERT INTO Abilities (id, name, legend, faction_id, description)
		VALUES (%s, %s, %s, %s, %s)
		ON DUPLICATE KEY UPDATE
			name = VALUES(name),
			legend = VALUES(legend),
			description = VALUES(description);
	""",
		(id, row[1], row[2], faction_id, row[4])
	)

cursor.close()
conn.close()