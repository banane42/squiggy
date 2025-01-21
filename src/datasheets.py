import csv
import requests
import psycopg2

conn = psycopg2.connect(
	database="wahapedia",
	host="localhost",
	user="gjmorris",
	port="5432"
)

cur = conn.cursor()

# create table if not exist
cur.execute(
"""
CREATE TABLE IF NOT EXISTS datasheets (
	id VARCHAR PRIMARY KEY,
	name VARCHAR NOT NULL,
	faction_id VARCHAR,
	source_id VARCHAR,
	legend TEXT,
	role VARCHAR,
	loadout TEXT,
	transport VARCHAR,
	virtual BOOLEAN,
	leader_head TEXT,
	leader_footer TEXT,
	damaged_w VARCHAR,
	damaged_description TEXT,
	link VARCHAR
);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Datasheets.csv'
)


decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		continue

	cur.execute(
			"""
			INSERT INTO datasheets (
				id, name, faction_id, source_id, legend, role, loadout, 
				transport, virtual, leader_head, leader_footer, 
				damaged_w, damaged_description, link
			)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
			ON CONFLICT (id)
			DO UPDATE SET
				name = EXCLUDED.name,
				faction_id = EXCLUDED.faction_id,
				source_id = EXCLUDED.source_id,
				legend = EXCLUDED.legend,
				role = EXCLUDED.role,
				loadout = EXCLUDED.loadout,
				transport = EXCLUDED.transport,
				virtual = EXCLUDED.virtual,
				leader_head = EXCLUDED.leader_head,
				leader_footer = EXCLUDED.leader_footer,
				damaged_w = EXCLUDED.damaged_w,
				damaged_description = EXCLUDED.damaged_description,
				link = EXCLUDED.link;
			""",
			(
				row[0], row[1], row[2], row[3], row[4], row[5], row[6],
				row[7], row[8].lower() == 'true', row[9], row[10],
				row[11], row[12], row[13]
			)
	)

conn.commit()
conn.close()