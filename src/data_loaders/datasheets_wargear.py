import csv
import pymysql.cursors
import requests
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def parse_values_columns(val: str) -> tuple:
	value = val.lower()
	try:
		attacks = int(value)
		return ('static', attacks, None, None)
	except: pass

	d_index = value.find('d')
	dice_count = 0
	try:
		dice_count = int(value[d_index - 1])
	except:
		dice_count = 1

	attack_type = None
	if value[d_index + 1] == "3":
		attack_type = 'D3'
	elif value[d_index + 1] == "6":
		attack_type = 'D6'

	attacks_additional = None
	plus_index = value.find('+')

	if plus_index > -1:
		attacks_additional = int(value[plus_index + 1])

	return (attack_type, None, dice_count, attacks_additional)

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
	CREATE TABLE IF NOT EXISTS datasheets_wargear (
		datasheet_id INT UNSIGNED NOT NULL,
		line TINYINT UNSIGNED,
		line_in_wargear TINYINT UNSIGNED,
		dice TEXT,
		name TEXT,
		description TEXT,
		`range` SMALLINT UNSIGNED,
		range_type ENUM('ranged', 'melee'),
		attack_type ENUM('static', 'D3', 'D6'),
		attacks_value_static TINYINT UNSIGNED,
		attacks_dice_count TINYINT UNSIGNED,
		attacks_additional TINYINT UNSIGNED,
		bs_ws TINYINT UNSIGNED,
		strength_type ENUM('static', 'D3', 'D6'),
		strength_value_static TINYINT UNSIGNED,
		strength_dice_count TINYINT UNSIGNED,
		strength_additional TINYINT UNSIGNED,
		ap TINYINT UNSIGNED,
		damage_type ENUM('static', 'D3', 'D6'),
		damage_value_static TINYINT UNSIGNED,
		damage_dice_count TINYINT UNSIGNED,
		damage_additional TINYINT UNSIGNED,
		PRIMARY KEY (datasheet_id, line)
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Datasheets_wargear.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		continue

	try:
		datasheet_id = int(row[0])
		line = int(row[1])
	except: continue

	line_in_wargear = int(row[2])

	range = None
	try:
		range = int(row[6])
	except: pass

	range_type = None
	if row[7].lower() == "ranged":
		range_type = "ranged"
	elif row[7].lower() == "melee":
		range_type = 'melee'

	attack_columns = parse_values_columns(row[8])

	bs_ws = None
	try:
		bs_ws = int(row[9][0])
	except: pass

	strength_columns = parse_values_columns(row[10])
	ap = abs(int(row[11]))
	damage_columns = parse_values_columns(row[12])

	cursor.execute(
	"""
		INSERT INTO datasheets_wargear (
			datasheet_id, line, line_in_wargear, dice, name, description, `range`, range_type,
			attack_type, attacks_value_static, attacks_dice_count, attacks_additional,
			bs_ws, strength_type, strength_value_static, strength_dice_count, strength_additional,
			ap, damage_type, damage_value_static, damage_dice_count, damage_additional
		)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
		ON DUPLICATE KEY UPDATE
			line_in_wargear = VALUES(line_in_wargear),
			dice = VALUES(dice),
			name = VALUES(name),
			description = VALUES(description),
			`range` = VALUES(`range`),
			range_type = VALUES(range_type),
			attack_type = VALUES(attack_type),
			attacks_value_static = VALUES(attacks_value_static),
			attacks_dice_count = VALUES(attacks_dice_count),
			attacks_additional = VALUES(attacks_additional),
			bs_ws = VALUES(bs_ws),
			strength_type = VALUES(strength_type),
			strength_value_static = VALUES(strength_value_static),
			strength_dice_count = VALUES(strength_dice_count),
			strength_additional = VALUES(strength_additional),
			ap = VALUES(ap),
			damage_type = VALUES(damage_type),
			damage_value_static = VALUES(damage_value_static),
			damage_dice_count = VALUES(damage_dice_count),
			damage_additional = VALUES(damage_additional);
	""",
		(
			datasheet_id, line, line_in_wargear, row[3], row[4], row[5], range, range_type,
			attack_columns[0], attack_columns[1], attack_columns[2], attack_columns[3],
			bs_ws, strength_columns[0], strength_columns[1], strength_columns[2], strength_columns[3],
			ap, damage_columns[0], damage_columns[1], damage_columns[2], damage_columns[3]
		)
	)

cursor.close()
conn.close()