from dotenv import load_dotenv
import os
import pymysql
from data_loaders.factions import FactionsDataLoader

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

faction_loader = FactionsDataLoader()

verbose = True

with conn.cursor() as cursor:
	faction_loader.populate(cursor=cursor, verbose=verbose)