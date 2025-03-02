import requests
import csv
import pymysql
import pymysql.cursors
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
	CREATE TABLE IF NOT EXISTS factions (
		id VARCHAR(4) PRIMARY KEY,
		name TEXT NOT NULL,
		link TEXT
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Factions.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		row=("CORE", "Core", "")

	cursor.execute(
	"""
		INSERT INTO factions (id, name, link) 
		VALUES (%s, %s, %s) 
		ON DUPLICATE KEY UPDATE 
		name = VALUES(name), 
		link = VALUES(link);
	""",
		(row[0], row[1], row[2])
	)

cursor.close()
conn.close()