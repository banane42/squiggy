from data_loaders import DataLoader

class LastUpdatedDataLoader(DataLoader):
	def __init__(self):
		super().__init__(
			'http://wahapedia.ru/wh40k10ed/Last_update.csv', 
			'last_updated'
		)

	def create_table(self, cursor):
		# Table is set up to only ever have one row
		# That is what the UNIQUE enum is for
		cursor.execute(
		"""
			CREATE TABLE IF NOT EXISTS last_updated (
				date DATETIME NOT NULL DEFAULT '1970-01-01 00:00:00',
				unique_value ENUM('unique') NOT NULL,
				UNIQUE (unique_value)
			);
		"""
		)

	def populate_table(self, cursor, reader):
		for i, row in enumerate(reader):
			if i != 1:
				continue

			date = row[0]
			break


		cursor.execute(
		"""
			SELECT count(*) from last_updated;
		"""
		)

		row_count = cursor.fetchone()['count(*)']

		if row_count == 0:
			cursor.execute(
			"""
				INSERT INTO last_updated(date, unique_value)
				VALUES (%s, 'unique');
			""",
				(date)
			)
		else:
			cursor.execute(
			"""
				UPDATE last_updated
				SET date = (%s)
				WHERE unique_value = 'unique'
			""",
				(date)
			)