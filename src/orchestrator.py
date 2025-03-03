from dotenv import load_dotenv
import os
import pymysql
import data_loaders

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

faction_loader = data_loaders.factions.FactionsDataLoader()
source_loader = data_loaders.sources.SourcesDataLoader()

verbose = True

with conn.cursor() as cursor:
	faction_loader.populate(cursor=cursor, verbose=verbose)
	source_loader.populate(cursor=cursor, verbose=verbose)