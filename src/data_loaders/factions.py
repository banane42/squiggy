import csv
import pymysql
import pymysql.cursors
from data_loaders import DataLoader

class FactionsDataLoader(DataLoader):

	def __init__(self):
		super().__init__(
			url='http://wahapedia.ru/wh40k10ed/Factions.csv', 
			table_name='factions'
		)
	
	def create_table(self, cursor: pymysql.cursors.DictCursor):
		cursor.execute(
		"""
			CREATE TABLE IF NOT EXISTS factions (
				id VARCHAR(4) PRIMARY KEY,
				name TEXT NOT NULL,
				link TEXT
			);
		"""
		)

	def populate_table(self, cursor: pymysql.cursors.DictCursor, reader: csv.reader):
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