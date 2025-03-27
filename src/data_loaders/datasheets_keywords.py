from data_loaders import DataLoader

class DatasheetsKeywordsLoader(DataLoader):
	def __init__(self):
		super().__init__(
			'http://wahapedia.ru/wh40k10ed/Datasheets_keywords.csv',
			'datasheets_keywords'
		)

	def create_table(self, cursor):
		cursor.execute(
		"""
			CREATE TABLE IF NOT EXISTS datasheets_keywords (
				datasheet_id INT UNSIGNED NOT NULL,
				keyword VARCHAR(128) NOT NULL,
				model TEXT,
				is_faction_keyword BOOLEAN DEFAULT FALSE,
				PRIMARY KEY (datasheet_id, keyword),
				FOREIGN KEY (datasheet_id) REFERENCES datasheets(id)
			);
		"""
		)

	def populate_table(self, cursor, reader):
		for i, row in enumerate(reader):
			if i == 0:
				continue

			id = int(row[0])
			is_faction_keyword = row[3] == "true"

			cursor.execute(
			"""
				INSERT INTO datasheets_keywords (datasheet_id, keyword, model, is_faction_keyword)
				VALUES (%s, %s, %s, %s)
				ON DUPLICATE KEY UPDATE
					model = VALUES(model),
					is_faction_keyword = VALUES(is_faction_keyword);
			""",
				(id, row[1], row[2], is_faction_keyword)
			)