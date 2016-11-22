import sys
import sqlite3

conn = None # global for db connection
c = None # global for cursor

# start sqlite database connection
def connectDB(path):
    global conn
    global c
    conn = sqlite3.connect(path)
    conn.row_factory = dict_factory
    c = conn.cursor()

# dict_factory turns query result into a dict with {col_name: value}
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# relation_info.py
def printTableNames():
	c.execute("SELECT name,sql FROM SQLITE_MASTER WHERE name NOT LIKE '%FDS%';")
	for table in c: 
		print("Table Name: " + str(table["name"]))
		print("Table Code: \n" + str(table["sql"]))
		print("\n")

# relation_info.py
def getFDSfor(table_name): 
	t = table_name.split("_")
	c.execute("SELECT * FROM ?".replace("?", t[0]+"_FDS_"+t[1]))
	for table in c: 
		print(str(table['LHS']) + " -> " + str(table['RHS']))
