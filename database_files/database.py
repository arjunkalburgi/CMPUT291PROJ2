import sys
import sqlite3

conn = None # global for db connection
c = None # global for cursor

# start sqlite database connection
def connectDB(path):
	global conn
	global c
	if path == "":
		path = 'database_files/MiniProject2-InputExample.db'
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
		# print("\n")

# relation_info.py
def printFDSfor(table_name):
	t = table_name.split("_")
	c.execute("SELECT * FROM ?".replace("?", t[0]+"_FDS_"+t[1]))
	for line in c:
		print(str(line['LHS']) + " -> " + str(line['RHS']))

def attributesFromSql(sql):
	att_arr = sql.split("\n")
	att_arr.pop(0)
	att_arr.pop(len(att_arr)-1)

	att = {}
	for a in att_arr:
		a = a.strip()
		a = a.replace(",", "")
		a = a.split(" ")
		# att.append({a[0]: a[1]})
		att[a[0]] = a[1]

	return att

# NF3_decomp
def chooseTable():
	c.execute("SELECT name,sql FROM SQLITE_MASTER WHERE name NOT LIKE '%FDS%';")
	tables = {}
	for table in c:
		print("Table Name: " + str(table["name"]))
		tables[table["name"]] = table["sql"]
		# print("\n")

	table = raw_input("Choose a table (type table's name)")
	if table in tables:
		print("This is the table (and its FDs) you've chosen: \n"+ tables[table])
		return {'name': table, 'sql': tables[table], 'attributes': attributesFromSql(tables[table])}
	else:
		print("This is not a valid table name, please choose again.")

	chooseTable()

# NF3_decomp
# returns fd sets in a table -> [{'LHS': 'AB', 'RHS': 'CD'}]
def getFDSfor(table_name):
	t = table_name.split("_")
	tlast = t[len(t)-1]
	t.remove(tlast)
	c.execute("SELECT * FROM ?".replace("?", "_".join(t)+"_FDS_"+tlast))
	fds = []
	for line in c:
		fds.append({'LHS': str(line['LHS']).replace(",",""), 'RHS': str(line['RHS']).replace(",","")})
	return fds

def printFDSfor(table_name):
	t = table_name.split("_")
	tlast = t[len(t)-1]
	t.remove(tlast)
	c.execute("SELECT * FROM ?".replace("?", "_".join(t)+"_FDS_"+tlast))
	for table in c:
		print(str(table['LHS']) + " -> " + str(table['RHS']))

def getFDSforTables(table_names):
	fds = []
	for table_name in table_names:
		c.execute("SELECT * FROM ?".replace("?", table_name))
		fds += c.fetchall()
	return fds

# connectDB('database_files/MiniProject2-InputExample.db')
# getFDSforTables('Input_FDs_R1')


def partition(f,t):
	'''
		t: {name: "...", sql: '...', attributes: {'A': 'INT',...}}
		f: [{LHS: '..', RHS:'..'}, {..}]
	'''
	name = "NF3_" + t['name'].replace("Input", "Output")

	# each fd needs 1.Partition Table, 2.FDs Table
	for fd in f:
		fd_att = fd['LHS'] + fd['RHS'] # attributes of fd
		t_name = name + "_" + fd_att
		# print(t_name)
		c.execute("DROP TABLE IF EXISTS " + t_name)

		# 1. Partition Table
		partition_sql = "CREATE TABLE " + t_name + "(\n" # bs i found online: + " AS SELECT " + ','.join(list(fd_att)) + " FROM " + t['name']
		for at in list(fd_att):
			partition_sql += "  " + at + " " + t['attributes'][at] + ",\n"
		partition_sql += "  PRIMARY KEY("+",".join(fd["LHS"])+"))"

		c.execute(partition_sql)


		# 2. FDs Table
		c.execute("DROP TABLE IF EXISTS " + name+"_FDS_"+fd_att)
		partition_createtable = "CREATE TABLE "+name+"_FDS_"+fd_att+" (LHS TEXT,RHS TEXT);"
		partition_insertdata = "INSERT INTO "+name+"_FDS_"+fd_att+" VALUES ('"+fd['LHS']+"','"+fd['RHS']+"');"

		print(partition_insertdata)

		c.execute(partition_createtable)
		c.execute(partition_insertdata)

		conn.commit()

	print ("Decomposition Finished")

def getColumnNames(table_name):
	res = c.execute("SELECT * FROM ?".replace("?", table_name))
	names = list(map(lambda x: x[0], res.description))
	return names

def create_new_schemas(schemas, name):
	'''
	schemas: e.g. [{'attributes': ['F', 'A'], 'fds': [{'LHS': 'F', 'RHS': 'A'}]}]
	Creates schemas for each schema corresponding to the format above.
	The above schema would create two tables:
	Output_R1_FA
	Output_FDS_R1_FA
	'''
	for s in schemas:
		table_name = "Output_" + name + '_' + ''.join(s['attributes'])
		c.execute("DROP TABLE IF EXISTS " + table_name)
		c.execute("CREATE TABLE " + table_name + '(' + ','.join(s['attributes']) + ')')
		fd_table_name = 'Output_FDS_' + name + '_' + ''.join(s['attributes'])
		c.execute("DROP TABLE IF EXISTS " + fd_table_name)
		c.execute("CREATE TABLE " + fd_table_name + '(LHS, RHS)')
		for fd in s['fds']:
			c.execute("INSERT INTO " + fd_table_name + " VALUES('" + fd['LHS'] + "','" + fd['RHS'] + "')")
	conn.commit()

def move_data(table_name, schemas):
	'''
	table_name: e.g. Input_R1
	schemas: e.g. [{'attributes': ['F', 'A'], 'fds': [{'LHS': 'F', 'RHS': 'A'}]}]
	Moves data from the original table (table_name) into
	the schemas specified.
	'''
	for s in schemas:
		output_table_name = "Output_" + table_name.split('_')[1] + '_' + ''.join(s['attributes'])
		c.execute("INSERT INTO " + output_table_name + " SELECT " + ','.join(s['attributes']) + " FROM " + table_name)
	conn.commit()
