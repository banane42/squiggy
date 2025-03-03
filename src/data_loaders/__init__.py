# data_loaders __init__.py
import pymysql.cursors
import csv
import requests

class DataLoader():
	def __init__(self, url: str, table_name: str):
		self.url = url
		self.table_name = table_name

	def create_table(self, cursor: pymysql.cursors.DictCursor):
		raise NotImplementedError

	def fetch_csv(self) -> csv.reader:
		response = requests.get(url=self.url)
		decoded_content = response.content.decode('utf-8')
		return csv.reader(decoded_content.splitlines(), delimiter='|')

	def populate_table(self, cursor: pymysql.cursors.DictCursor, reader: csv.reader):
		raise NotImplemented

	def populate(self, cursor: pymysql.cursors.DictCursor, verbose: bool):
		if verbose:
			print(f"Creating table: {self.table_name}")
		self.create_table(cursor)

		if verbose:
			print(f"Fetching csv from {self.url}")
		reader = self.fetch_csv()

		if verbose:
			print(f"Populating {self.table_name}")

		self.populate_table(cursor=cursor, reader=reader)

from .factions import FactionsDataLoader
from .sources import SourcesDataLoader
from .stratagems import StratagemsDataLoader