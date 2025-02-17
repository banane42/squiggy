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
	CREATE TABLE IF NOT EXISTS Abilities (
		id INT UNSIGNED,
		name VARCHAR(64) NOT NULL,
		legend TEXT,
		faction_id VARCHAR(4),
		description TEXT,
		PRIMARY KEY (id, name, faction_id),
		FOREIGN KEY (faction_id) REFERENCES Factions(id)
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/{FILL IN HERE}.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		continue

	cursor.execute(
	"""
	""",
		()
	)

cursor.close()
conn.close()