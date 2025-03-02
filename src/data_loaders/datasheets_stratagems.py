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
	CREATE TABLE IF NOT EXISTS datasheets_stratagems (
		datasheet_id INT UNSIGNED,
		stratagem_id INT UNSIGNED,
		PRIMARY KEY (datasheet_id, stratagem_id),
		FOREIGN KEY (datasheet_id) REFERENCES datasheets(id),
		FOREIGN KEY (stratagem_id) REFERENCES stratagems(id)
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Datasheets_stratagems.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		continue
	
	datasheet_id = int(row[0])
	stratagem_id = int(row[1])

	cursor.execute(
	"""
		INSERT IGNORE INTO datasheets_stratagems (
			datasheet_id, stratagem_id
		)
		VALUES (%s, %s)
		ON DUPLICATE KEY UPDATE
			datasheet_id = VALUES(datasheet_id);
	""",
		(datasheet_id, stratagem_id)
	)

cursor.close()
conn.close()