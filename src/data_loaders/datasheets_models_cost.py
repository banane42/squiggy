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
	CREATE TABLE IF NOT EXISTS datasheets_models_cost (
		datasheet_id INT UNSIGNED NOT NULL,
		line TINYINT UNSIGNED,
		description TEXT,
		cost SMALLINT UNSIGNED,
		PRIMARY KEY (datasheet_id, line)
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Datasheets_models_cost.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		continue

	id = int(row[0])
	line = int(row[1])
	cost = int(row[3])

	cursor.execute(
	"""
		INSERT INTO datasheets_models_cost (
			datasheet_id, line, description, cost
		)
		VALUES (%s, %s, %s, %s)
		ON DUPLICATE KEY UPDATE
			description = VALUES(description),
			cost = VALUES(cost);
	""",
		(id, line, row[2], cost)
	)

cursor.close()
conn.close()