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
	CREATE TABLE IF NOT EXISTS datasheets (
		id INT UNSIGNED PRIMARY KEY,
		name TEXT NOT NULL,
		faction_id VARCHAR(4) NOT NULL,
		source_id INT UNSIGNED NOT NULL DEFAULT 0,
		legend TEXT,
		role TEXT,
		loadout TEXT,
		transport TEXT,
		is_virtual BOOLEAN DEFAULT FALSE,
		leader_head TEXT,
		leader_footer TEXT,
		damaged_w TEXT,
		damaged_description TEXT,
		link TEXT,
		FOREIGN KEY (faction_id) REFERENCES factions(id),
		FOREIGN KEY (source_id) REFERENCES source(id)
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Datasheets.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		continue

	print("Inserting\n", row)

	id = int(row[0])

	source_id = 0
	if row[3] != "":
		source_id = int(row[3])

	virtual = row[8] == "true"

	cursor.execute(
	"""
		INSERT INTO datasheets (
			id, name, faction_id, source_id, legend, role, loadout, transport, is_virtual, 
			leader_head, leader_footer, damaged_w, damaged_description, link
		) 
		VALUES (
			%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
		) 
		ON DUPLICATE KEY UPDATE
			name = VALUES(name),
			faction_id = VALUES(faction_id),
			source_id = VALUES(source_id),
			legend = VALUES(legend),
			role = VALUES(role),
			loadout = VALUES(loadout),
			transport = VALUES(transport),
			is_virtual = VALUES(is_virtual),
			leader_head = VALUES(leader_head),
			leader_footer = VALUES(leader_footer),
			damaged_w = VALUES(damaged_w),
			damaged_description = VALUES(damaged_description),
			link = VALUES(link);
	""",
		(id, row[1], row[2], source_id, row[4], row[5], row[6], row[7], virtual, row[9], row[10], row[11], row[12], row[13])
	)

cursor.close()
conn.close()