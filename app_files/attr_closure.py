from database_files import database as db

def compute_attribute_closure(attrs, fds):
	'''
	attrs: list of strings corresponding to attribute names
	(e.g. ['A', 'B'])
	fds: list of dictionaries with a LHS and RHS field. LHS
	and RHS fields should be a comma separated string of
	attribute names
	(e.g. [{LHS: 'A,B,C', 'RHS': 'D,K'}])
	Returns the attribute closure of attrs with respect to
	the functional depedencies in fds
	'''
	closure = set(attrs)
	old = set()
	while closure != old:
		old = closure
		for fd in fds:
			lhs = set(fd['LHS'].split(','))
			rhs = set(fd['RHS'].split(','))
			if lhs.issubset(closure):
				closure = closure.union(rhs)
	return closure

def start():
	# get the tables containing FDs
	fd_table_names = []
	while True:
		table_name = raw_input("Enter a table name (or Q to finish entering): ")
		if table_name == 'Q' or table_name == '':
			break
		else:
			fd_table_names.append(table_name)
	if len(fd_table_names) == 0:
		print "Error: You did not enter any table names."
		return
	print "You have entered " + str(len(fd_table_names)) + " table(s): " + ', '.join(fd_table_names)
	fds = db.getFDSforTables(fd_table_names)

	# get the set of attributes
	attributes = raw_input('Enter the set of attributes separated by commas (e.g. A,B,C): ')
	attributes = attributes.split(',')

	#compute the attribute closure
	closure = compute_attribute_closure(attributes, fds)
	print "The attribute closure of X = {" + ','.join(attributes) + "} is {" + ','.join(closure) + "}"

	raw_input("Press enter to continue...")
