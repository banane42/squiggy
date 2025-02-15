import csv
import requests

b = "false"
con_b = bool(b)
print(con_b)

# print("\n\n\n+++++++++++++++++++++++++\nBegin Local CSV process\n+++++++++++++++++++++++++\n\n\n")

# with open('/Users/gjmorris/Downloads/wahapedia_export/Datasheets_models.csv', 'r') as csvfile:
# 	reader = csv.reader(csvfile, delimiter='|')
# 	for row in reader:
# 		print("--------------------------")
# 		col_str = ""
# 		for column in row:
# 			col_str += str(column) + "+"
# 		print(col_str)

# print("\n\n\n+++++++++++++++++++++++++\nBegin HTTP Request CSV Process\n+++++++++++++++++++++++++\n\n\n")

# response = requests.get(
# 	url='http://wahapedia.ru/wh40k10ed/Datasheets_models.csv'
# )

# decoded_content = response.content.decode('utf-8')

# reader = csv.reader(decoded_content.splitlines(), delimiter='|')
# for row in reader:
# 	print("--------------------------")
# 	col_str = ""
# 	for column in row:
# 		col_str += str(column) + "+"
# 	print(col_str)