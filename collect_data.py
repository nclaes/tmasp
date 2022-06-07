import pandas as pd 
import sqlite3
import csv


conn = sqlite3.connect("hyperparamter_serarch.db")
# df = pd.read_sql_query("select * from TM_SETTINGS", conn)

# To view table data in table format
cur = conn.cursor()
cur.execute('''SELECT * FROM TM_SETTINGS''')
rows = cur.fetchall()

for row in rows:
  print(row)

# Export data into CSV file
# print "Exporting data into CSV............"
cursor = conn.cursor()
cursor.execute("select * from TM_SETTINGS")
with open("search_results.csv", "w") as csv_file:
  csv_writer = csv.writer(csv_file, delimiter=",")
  csv_writer.writerow([i[0] for i in cursor.description])
  csv_writer.writerows(cursor)


