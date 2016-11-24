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
	for table in c:
		print(str(table['LHS']) + " -> " + str(table['RHS']))

def getFDSforTables(table_names):
    fds = []
    for table_name in table_names:
        c.execute("SELECT * FROM ?".replace("?", table_name))
        fds += c.fetchall()
    return fds

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
        print "INSERT INTO " + output_table_name + " SELECT " + ','.join(s['attributes']) + " FROM " + table_name
        c.execute("INSERT INTO " + output_table_name + " SELECT " + ','.join(s['attributes']) + " FROM " + table_name)
    conn.commit()

# connectDB('database_files/MiniProject2-InputOutputExampleBCNF.db')
# create_new_schemas([{'attributes': ['F', 'A'], 'fds': [{'LHS': 'F', 'RHS': 'A'}]}], 'Kevin')
