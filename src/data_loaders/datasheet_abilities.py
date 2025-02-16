import csv
import pymysql.cursors
import requests
import pymysql
from dotenv import load_dotenv
import os
# TODO DO this later, it's real funky
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

"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Datasheets_abilities.csv'
)