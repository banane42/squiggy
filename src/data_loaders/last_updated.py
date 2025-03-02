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

# Table is set up to only ever have one row
# That is what the UNIQUE enum is for
cursor.execute(
"""
	CREATE TABLE IF NOT EXISTS last_updated (
		date DATETIME NOT NULL DEFAULT '1970-01-01 00:00:00',
		unique_value ENUM('unique') NOT NULL,
		UNIQUE (unique_value)
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Last_update.csv'
)

decoded_content = response.content.decode('utf-8')
date = ""

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i != 1:
		continue

	date = row[0]
	break


cursor.execute(
"""
	SELECT count(*) from last_updated;
"""
)

row_count = cursor.fetchone()['count(*)']

if row_count == 0:
	cursor.execute(
	"""
		INSERT INTO last_updated(date, unique_value)
		VALUES (%s, 'unique');
	""",
		(date)
	)
else:
	cursor.execute(
	"""
		UPDATE last_updated
		SET date = (%s)
		WHERE unique_value = 'unique'
	""",
		(date)
	)

cursor.close()
conn.close()