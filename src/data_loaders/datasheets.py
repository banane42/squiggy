import csv
import pymysql.cursors
import requests
import pymysql
from dotenv import load_dotenv
import os

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
	CREATE TABLE IF NOT EXISTS datasheets (
		id INT UNSIGNED PRIMARY KEY,
		name TEXT NOT NULL,
		faction_id VARCHAR(4) NOT NULL,
		source_id INT UNSIGNED NOT NULL,
		legend TEXT,
		role TEXT,
		loadout TEXT,
		transport TEXT,
		virtual BOOLEAN DEFAULT FALSE,
		leader_head TEXT,
		leader_footer TEXT,
		damaged_w TEXT,
		damaged_description TEXT,
		link TEXT,
		FOREIGN KEY (faction_id) REFERENCES factions(id),
		FOREIGN KEY (source_id) REFERENCES source(id)
	);
"""
)