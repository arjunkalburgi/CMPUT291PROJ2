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
def printFDSfor(table_name): 
	t = table_name.split("_")
	c.execute("SELECT * FROM ?".replace("?", t[0]+"_FDS_"+t[1]))
	for line in c: 
		print(str(line['LHS']) + " -> " + str(line['RHS']))

# NF3_decomp
def chooseTable(): 
	c.execute("SELECT name,sql FROM SQLITE_MASTER WHERE name NOT LIKE '%FDS%';")
	tables = {}
	for table in c: 
		print("Table Name: " + str(table["name"]))
		tables[table["name"]] = table["sql"]
		print("\n")

	table = raw_input("Choose a table (type table's name)")
	if table in tables: 
		print("This is the table you've chosen: \n \
			" + tables[table])
		return {table: tables[table]}
	else: 
		print("This is not a valid table name, please choose again.")

	chooseTable()

# NF3_decomp
def getFDSfor(table_name): 
	t = table_name.split("_")
	c.execute("SELECT * FROM ?".replace("?", t[0]+"_FDS_"+t[1]))
	fds = []
	for line in c: 
		fds.append(str(line['LHS']) + " -> " + str(line['RHS']))
	return fds