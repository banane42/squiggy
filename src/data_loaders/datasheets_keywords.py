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
	CREATE TABLE IF NOT EXISTS datasheets_keywords (
		datasheet_id INT UNSIGNED NOT NULL,
		keyword VARCHAR(128) NOT NULL,
		model TEXT,
		is_faction_keyword BOOLEAN DEFAULT FALSE,
		PRIMARY KEY (datasheet_id, keyword),
		FOREIGN KEY (datasheet_id) REFERENCES datasheets(id)
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Datasheets_keywords.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		continue

	id = int(row[0])
	is_faction_keyword = row[3] == "true"

	cursor.execute(
	"""
		INSERT INTO datasheets_keywords (datasheet_id, keyword, model, is_faction_keyword)
		VALUES (%s, %s, %s, %s)
		ON DUPLICATE KEY UPDATE
			model = VALUES(model),
			is_faction_keyword = VALUES(is_faction_keyword);
	""",
		(id, row[1], row[2], is_faction_keyword)
	)

cursor.close()
conn.close()