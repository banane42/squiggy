from dotenv import load_dotenv
import os
import pymysql
import data_loaders
import data_loaders.datasheets

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
stratagem_loader = data_loaders.stratagems.StratagemsDataLoader()
abilities_loader = data_loaders.abilities.AbilitiesDataLoader()
enhancements_loader = data_loaders.enhancements.EnhancementsDataLoader()
detachement_abilities_loader = data_loaders.detachement_abilities.DetachementAbilitiesDataLoader()
last_updated_loader = data_loaders.last_updated.LastUpdatedDataLoader()
datasheets_loader = data_loaders.datasheets.DatasheetsDataLoader()
datasheets_keywords_loader = data_loaders.datasheets_keywords.DatasheetsKeywordsLoader()

verbose = True

with conn.cursor() as cursor:
	faction_loader.populate(cursor=cursor, verbose=verbose)
	source_loader.populate(cursor=cursor, verbose=verbose)
	stratagem_loader.populate(cursor=cursor, verbose=verbose)
	abilities_loader.populate(cursor=cursor, verbose=verbose)
	enhancements_loader.populate(cursor=cursor, verbose=verbose)
	detachement_abilities_loader.populate(cursor=cursor, verbose=verbose)
	last_updated_loader.populate(cursor=cursor, verbose=verbose)
	datasheets_loader.populate(cursor=cursor, verbose=verbose)
	datasheets_keywords_loader.populate(cursor=cursor, verbose=verbose)