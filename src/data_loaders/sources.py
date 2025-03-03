import csv
import pymysql
import pymysql.cursors
from datetime import datetime

from data_loaders import DataLoader

class SourcesDataLoader(DataLoader):

	def __init__(self):
		super().__init__(
			url='http://wahapedia.ru/wh40k10ed/Source.csv', 
			table_name='sources'
		)

	def create_table(self, cursor: pymysql.cursors.DictCursor):
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

	def populate_table(self, cursor: pymysql.cursors.DictCursor, reader: csv.reader):
		for i, row in enumerate(reader):
			if i == 0:
				# Some datasheets do not have a source, insert blank source for foreign key
				row = (0, '', '', '', '', '1.01.1000 0:00:00', '')
			
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