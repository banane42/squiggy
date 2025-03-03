import csv
import pymysql.cursors
import pymysql
from data_loaders import DataLoader

class AbilitiesDataLoader(DataLoader):
	def __init__(self):
		super().__init__(
			url='http://wahapedia.ru/wh40k10ed/Abilities.csv', 
			table_name='abilities'
		)

	
	def create_table(self, cursor: pymysql.cursors.DictCursor):
		cursor.execute(
		"""
			CREATE TABLE IF NOT EXISTS abilities (
				id INT UNSIGNED,
				name VARCHAR(64) NOT NULL,
				legend TEXT,
				faction_id VARCHAR(4),
				description TEXT,
				PRIMARY KEY (id, faction_id),
				FOREIGN KEY (faction_id) REFERENCES factions(id)
			);
		"""
		)


	def populate_table(self, cursor: pymysql.cursors.DictCursor, reader: csv.reader):
		for i, row in enumerate(reader):
			if i == 0:
				continue

			id = int(row[0])
			faction_id = row[3]
			if faction_id == "":
				faction_id = "CORE"

			cursor.execute(
			"""
				INSERT INTO Abilities (id, name, legend, faction_id, description)
				VALUES (%s, %s, %s, %s, %s)
				ON DUPLICATE KEY UPDATE
					name = VALUES(name),
					legend = VALUES(legend),
					description = VALUES(description);
			""",
				(id, row[1], row[2], faction_id, row[4])
			)