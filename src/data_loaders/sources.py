import requests
import csv
import pymysql
import pymysql.cursors
from dotenv import load_dotenv
import os
from datetime import datetime

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
	CREATE TABLE IF NOT EXISTS source (
		id INT UNSIGNED PRIMARY KEY,
		name TEXT NOT NULL,
		type TEXT NOT NULL,
		edition TEXT,
		version TEXT,
		errata_date DATE,
		errata_link TEXT
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Source.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		# Some datasheets do not have a source, insert blank source for foreign key
		row = (0, '', '', '', '', '1.01.1000 0:00:00', '')
	
	print(row)
	id = int(row[0])
	date = datetime.strptime(row[5], "%d.%m.%Y %H:%M:%S").strftime("%Y-%m-%d")

	cursor.execute(
	"""
		INSERT INTO source (
			id, name, type, edition, version, errata_date, errata_link
		) 
		VALUES (%s, %s, %s, %s, %s, %s, %s) 
		ON DUPLICATE KEY UPDATE 
		name = VALUES(name),
		type = VALUES(type),
		edition = VALUES(edition),
		version = VALUES(version),
		errata_date = VALUES(errata_date),
		errata_link = VALUES(errata_link);
	""",
		(id, row[1], row[2], row[3], row[4], date, row[6])
	)

cursor.close()
conn.close()