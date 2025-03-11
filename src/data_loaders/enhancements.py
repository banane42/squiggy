import csv
import pymysql.cursors
import requests
import pymysql
from dotenv import load_dotenv
from data_loaders import DataLoader
import os

class EnhancementsDataLoader(DataLoader):
	def __init__(self):
		super().__init__(
			'http://wahapedia.ru/wh40k10ed/Enhancements.csv', 
			'enhancements'
		)

	def create_table(self, cursor: pymysql.cursors.DictCursor):
		cursor.execute(
		"""
			CREATE TABLE IF NOT EXISTS enhancements (
				id INT UNSIGNED PRIMARY KEY,
				faction_id VARCHAR(4),
				name TEXT,
				cost SMALLINT UNSIGNED,
				detachment TEXT,
				legend TEXT,
				description TEXT
			);
		"""
		)

	def populate_table(self, cursor: pymysql.cursors.DictCursor, reader: csv.reader):
		for i, row in enumerate(reader):
			if i == 0:
				continue

			id = int(row[0])
			cost = int(row[3])

			cursor.execute(
			"""
			INSERT INTO enhancements (
				id, faction_id, name, cost, detachment, legend, description
			)
			VALUES (%s, %s, %s, %s, %s, %s, %s)
			ON DUPLICATE KEY UPDATE 
				faction_id = VALUES(faction_id),
				name = VALUES(name),
				cost = VALUES(cost),
				detachment = VALUES(detachment),
				legend = VALUES(legend),
				description = VALUES(description);
			""",
				(id, row[1], row[2], cost, row[4], row[5], row[6])
			)