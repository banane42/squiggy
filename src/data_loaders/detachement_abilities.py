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
	CREATE TABLE IF NOT EXISTS detachment_abilities (
		id INT UNSIGNED PRIMARY KEY,
		faction_id VARCHAR(4) NOT NULL,
		name TEXT,
		legend TEXT,
		description TEXT,
		detachment TEXT,
		FOREIGN KEY (faction_id) REFERENCES factions(id)
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Detachment_abilities.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		continue

	id = int(row[0])

	cursor.execute(
	"""
		INSERT INTO detachment_abilities (
			id, faction_id, name, legend, description, detachment
		)
		VALUES (%s, %s, %s, %s, %s, %s)
		ON DUPLICATE KEY UPDATE 
			faction_id = VALUES(faction_id),
			name = VALUES(name),
			legend = VALUES(legend),
			description = VALUES(description),
			detachment = VALUES(detachment);
	""",
		(id, row[1], row[2], row[3], row[4], row[5])
	)

cursor.close()
conn.close()