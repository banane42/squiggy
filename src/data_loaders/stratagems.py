import csv
import pymysql.cursors
import pymysql
from data_loaders import DataLoader

class StratagemsDataLoader(DataLoader):

	def __init__(self):
		super().__init__(
			url='http://wahapedia.ru/wh40k10ed/Stratagems.csv', 
			table_name='stratagems'
		)

	def create_table(self, cursor: pymysql.cursors.DictCursor):
		cursor.execute(
		"""
			CREATE TABLE IF NOT EXISTS stratagems (
				id INT UNSIGNED PRIMARY KEY,
				faction_id VARCHAR(4) NOT NULL,
				name TEXT,
				type TEXT,
				cp_cost TINYINT UNSIGNED,
				legend TEXT,
				turn TEXT,
				phase TEXT,
				description TEXT,
				detachment TEXT
			);
		"""
		)

	def populate_table(self, cursor: pymysql.cursors.DictCursor, reader: csv.reader):
		for i, row in enumerate(reader):
			if i == 0:
				continue

			id = int(row[1])

			cp_cost = 0
			try:
				cp_cost = int(row[4])
			except: pass

			faction_id = row[0]
			if faction_id == "":
				faction_id = "CORE"

			cursor.execute(
			"""
				INSERT INTO stratagems (
					id, faction_id, name, type, cp_cost, legend, turn, phase, description, detachment
				)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
				ON DUPLICATE KEY UPDATE
					faction_id = VALUES(faction_id),
					name = VALUES(name),
					type = VALUES(type),
					cp_cost = VALUES(cp_cost),
					legend = VALUES(legend),
					turn = VALUES(turn),
					phase = VALUES(phase),
					description = VALUES(description),
					detachment = VALUES(detachment);
			""",
				(id, faction_id, row[2], row[3], cp_cost, row[5], row[6], row[7], row[8], row[9])
			)