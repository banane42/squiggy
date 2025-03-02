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
	CREATE TABLE IF NOT EXISTS datasheets_abilities (
		datasheet_id INT UNSIGNED NOT NULL,
		line INT NOT NULL,
		ability_id INT UNSIGNED,
		model TEXT,
		name TEXT,
		description TEXT,
		type TEXT,
		parameter TEXT,
		PRIMARY KEY (datasheet_id, line),
		FOREIGN KEY (datasheet_id) REFERENCES datasheets(id)
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Datasheets_abilities.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		continue

	datasheet_id = int(row[0])
	line = int(row[1])
	ability_id = None
	if row[2] != "":
		ability_id = int(row[2])

	ability_type = ""
	inside_parens = False
	for c in row[6]:
		if c == "(":
			inside_parens = True
		elif c == ")":
			inside_parens = False
		elif not inside_parens:
			ability_type += c

	cursor.execute(
	"""
		INSERT INTO datasheets_abilities (
			datasheet_id, line, ability_id, model, name, description, type, parameter
		)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
		ON DUPLICATE KEY UPDATE 
			ability_id = VALUES(ability_id),
			model = VALUES(model),
			name = VALUES(name),
			description = VALUES(description),
			type = VALUES(type),
			parameter = VALUES(parameter);
	""",
		(datasheet_id, line, ability_id, row[3], row[4], row[5], ability_type, row[7])
	)

cursor.close()
conn.close()