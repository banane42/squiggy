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
	CREATE TABLE IF NOT EXISTS datasheets_options (
		datasheet_id INT UNSIGNED NOT NULL,
		line TINYINT UNSIGNED,
		button ENUM('star', 'bullet'),
		description TEXT,
		PRIMARY KEY (datasheet_id, line)
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Datasheets_options.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		continue

	id = int(row[0])
	line = int(row[1])
	button = ""
	if row[2] == "*":
		button = "star"
	elif row[2] == "•":
		button = "bullet"

	description = row[3]
	if row[3] == "None":
		description = ""


	cursor.execute(
	"""
		INSERT INTO datasheets_options (
			datasheet_id, line, button, description
		)
		VALUES (%s, %s, %s, %s)
		ON DUPLICATE KEY UPDATE
			button = VALUES(button),
			description = VALUES(description);
	""",
		(id, line, button, description)
	)

cursor.close()
conn.close()