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

cur.execute(
"""
	CREATE TABLE IF NOT EXISTS datasheets_models (
		datasheet_id VARCHAR NOT NULL,
		line VARCHAR NOT NULL,
		name VARCHAR NOT NULL,
		M VARCHAR NOT NULL,
		T VARCHAR NOT NULL,
		Sv VARCHAR NOT NULL,
		inv_sv VARCHAR,
		inv_sv_descr TEXT,
		W VARCHAR NOT NULL,
		Ld VARCHAR NOT NULL,
		OC VARCHAR NOT NULL,
		base_size VARCHAR,
		base_size_descr TEXT,
		PRIMARY KEY (datasheet_id, line)
	);
"""
)

response = requests.get(
	url='http://wahapedia.ru/wh40k10ed/Datasheets_models.csv'
)

decoded_content = response.content.decode('utf-8')

reader = csv.reader(decoded_content.splitlines(), delimiter='|')
for i, row in enumerate(reader):
	if i == 0:
		continue

	cur.execute(
		"""
		INSERT INTO datasheets_models (
			datasheet_id, line, name, M, T, Sv, inv_sv, inv_sv_descr, W, Ld, OC, base_size, base_size_descr
		)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
		ON CONFLICT (datasheet_id, line)
		DO UPDATE SET
			name = EXCLUDED.name,
			M = EXCLUDED.M,
			T = EXCLUDED.T,
			Sv = EXCLUDED.Sv,
			inv_sv = EXCLUDED.inv_sv,
			inv_sv_descr = EXCLUDED.inv_sv_descr,
			W = EXCLUDED.W,
			Ld = EXCLUDED.Ld,
			OC = EXCLUDED.OC,
			base_size = EXCLUDED.base_size,
			base_size_descr = EXCLUDED.base_size_descr;
		""",
		(
			row[0], int(row[1]), row[2], row[3], row[4], row[5], row[6], row[7],
			row[8], row[9], row[10], row[11], row[12]
		)
	)

conn.commit()
conn.close()