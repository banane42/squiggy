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
	CREATE TABLE IF NOT EXISTS datasheets_detachment_abilities (
		datasheet_id INT UNSIGNED,
		detachment_ability_id INT UNSIGNED,
		PRIMARY KEY (datasheet_id, detachment_ability_id),
		FOREIGN KEY (datasheet_id) REFERENCES datasheets(id),
		FOREIGN KEY (detachment_ability_id) REFERENCES detachment_abilities(id)
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Datasheets_detachment_abilities.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		continue

	datasheet_id = int(row[0])
	ability_id = int(row[1])

	cursor.execute(
	"""
		INSERT IGNORE INTO datasheets_detachment_abilities (
			datasheet_id, detachment_ability_id
		)
		VALUES (%s, %s)
		ON DUPLICATE KEY UPDATE
			datasheet_id = VALUES(datasheet_id);
	""",
		(datasheet_id, ability_id)
	)

cursor.close()
conn.close()