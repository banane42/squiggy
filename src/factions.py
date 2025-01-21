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

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Factions.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		continue

	cur.execute(
		"""
		INSERT INTO factions (id, name, link)
		VALUES (%s, %s, %s)
		ON CONFLICT (id)
		DO UPDATE SET
			name = EXCLUDED.name,
			link = EXCLUDED.link;
		""",
		(row[0], row[1], row[2])
	)

# cur.execute("SELECT * FROM factions;")
# print(cur.fetchall())
conn.commit()

conn.close()