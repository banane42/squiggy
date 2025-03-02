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
	CREATE TABLE IF NOT EXISTS datasheets_models (
		datasheet_id INT UNSIGNED NOT NULL,
		line INT NOT NULL,
		name TEXT,
		movement TINYINT UNSIGNED,
		is_minimum_move BOOLEAN DEFAULT FALSE,
		toughness TINYINT UNSIGNED,
		armor_save TINYINT UNSIGNED,
		invuln_save TINYINT UNSIGNED,
		invuln_save_descr TEXT,
		wounds TINYINT,
		leadership TINYINT,
		objective_control TINYINT,
		base_size TEXT,
		base_size_descr TEXT,
		PRIMARY KEY (datasheet_id, line)
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Datasheets_models.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		continue

	id = int(row[0])
	line = int(row[1])

	movement_str = ""
	is_minimum_move = False
	for c in row[3]:
		if c.isdigit():
			movement_str += c
		if c == "+":
			is_minimum_move = True

	movement = None
	if len(movement_str) != 0:
		movement = int(movement_str)

	toughness_str = ""
	for c in row[4]:
		if c.isdigit():
			toughness_str += c
	toughness = int(toughness_str)

	armor_save = int(row[5][0])

	invuln_save = None
	if row[6] != "-":
		invuln_save = int(row[6][0])

	wounds = int(row[8])
	leadership = int(row[9][0])
	oc = int(row[10])

	cursor.execute(
	"""
		INSERT INTO datasheets_models (
			datasheet_id, line, name, movement, is_minimum_move, 
			toughness, armor_save, invuln_save, invuln_save_descr,
			wounds, leadership, objective_control, base_size, base_size_descr
		)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
		ON DUPLICATE KEY UPDATE
			name = VALUES(name),
			movement = VALUES(movement),
			is_minimum_move = VALUES(is_minimum_move),
			toughness = VALUES(toughness),
			armor_save = VALUES(armor_save),
			invuln_save = VALUES(invuln_save),
			invuln_save_descr = VALUES(invuln_save_descr),
			wounds = VALUES(wounds),
			leadership = VALUES(leadership),
			objective_control = VALUES(objective_control),
			base_size = VALUES(base_size),
			base_size_descr = VALUES(base_size_descr);
	""",
		(id, line, row[2], movement, is_minimum_move, toughness, armor_save, invuln_save, row[7], wounds, leadership, oc, row[11], row[12])
	)

cursor.close()
conn.close()