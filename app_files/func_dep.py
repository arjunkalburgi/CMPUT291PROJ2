from database_files import database as db
from attr_closure import compute_attribute_closure

def functional_depedencies_equivalent(f1, f2):
	'''
	f1 and f2: list of dictionaries with a LHS and RHS field. LHS
	and RHS fields should be a comma separated string of
	attribute names
	(e.g. [{LHS: 'A,B,C', 'RHS': 'D,K'}])
	Returns true if f1 and f2 are equivalent sets of functional
	dependencies
	'''
	for fd in f1:
		lhs = set(fd['LHS'].split(','))
		rhs = set(fd['RHS'].split(','))
		closure = compute_attribute_closure(lhs, f2)
		if not rhs.issubset(closure):
			return False
	for fd in f2:
		lhs = set(fd['LHS'].split(','))
		rhs = set(fd['RHS'].split(','))
		closure = compute_attribute_closure(lhs, f1)
		if not rhs.issubset(closure):
			return False
	return True

def start():
	# get F1 functional depedencies
	f1_table_names = []
	while True:
		table_name = raw_input("Enter a table name for F1 (or Q to finish entering): ")
		if table_name == 'Q' or table_name == '':
			break
		else:
			f1_table_names.append(table_name)
	if len(f1_table_names) == 0:
		print "Error: You did not enter any table names."
		return
	f1 = db.getFDSforTables(f1_table_names)
	print "F1) You have entered " + str(len(f1_table_names)) + " table(s): " + ', '.join(f1_table_names)

	# get F2 functional dependancies
	f2_table_names = []
	while True:
		table_name = raw_input("Enter a table name for F2 (or Q to finish entering): ")
		if table_name == 'Q' or table_name == '':
			break
		else:
			f2_table_names.append(table_name)
	if len(f2_table_names) == 0:
		print "Error: You did not enter any table names."
		return
	f2 = db.getFDSforTables(f2_table_names)
	print "F2) You have entered " + str(len(f2_table_names)) + " table(s): " + ', '.join(f2_table_names)

	if functional_depedencies_equivalent(f1, f2):
		print "The two sets of functional dependencies are equivalent."
	else:
		print "The two sets of functional dependencies are not equivalent"
	raw_input("Press enter to continue...")
