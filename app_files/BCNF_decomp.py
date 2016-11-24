from database_files import database as db
from attr_closure import compute_attribute_closure

def compute_bcnf(attrs, fds):
	'''
	attrs: list of attribute names corresponding to the
	names of the columns
	fds: list of functional dependencies
	(e.g. [{'LHS': 'A,B,C', 'RHS': 'D,K'}, ...])
	Returns: list of dictionaries. Each dictionary has a
	field attributes and a field fds
	(e.g. [{'attributes': ['A','B','C'], {'fds': [{'LHS': 'A', 'RHS': 'B,C'}]}}])
	'''
	R = [{'attributes': attrs, 'fds': fds}]

	while True:
		found_violation = False

		for S in R:
			violation_fd = check_bcnf(S['attributes'], S['fds'])
			if violation_fd is not None:
				found_violation = True
				# remove offending FD and attributes from S1
				S['attributes'] = list(set(S['attributes']) - set(violation_fd['RHS'].split(',')))
				S1_FDs = []
				for fd in S['fds']: # compute all FDs of S after removal of violation FD's attributes
					lhs = set(fd['LHS'].split(','))
					rhs = set(fd['RHS'].split(','))
					violation_fd_lhs = set(violation_fd['LHS'].split(','))
					violation_fd_rhs = set(violation_fd['RHS'].split(','))
					if not violation_fd_rhs.isdisjoint(lhs):
						continue
					if lhs == violation_fd_lhs and rhs == violation_fd_rhs:
						continue
					rhs -= violation_fd_rhs
					if len(rhs) == 0:
						continue
					S1_FDs.append({'LHS': fd['LHS'], 'RHS': ','.join(rhs)})
				S['fds'] = S1_FDs
				# create S2 that is in BCNF
				S2_attributes = list(set(violation_fd['LHS'].split(',') + violation_fd['RHS'].split(',')))
				S2_FDs = [violation_fd]
				# add S2 to R
				R.append({'attributes': S2_attributes, 'fds': S2_FDs})

		if not found_violation:
			break

	return R

def check_bcnf(attrs, fds):
	'''
	Checks if the relation composed of attrs and fds is
	in BCNF. Returns the offending FD if not in BCNF,
	otherwise returns None
	'''
	attrs = set(attrs)
	for fd in fds:
		lhs = set(fd['LHS'].split(','))
		closure = compute_attribute_closure(lhs, fds)
		if closure != attrs:
			return fd
	return None

def start():
	table_name = raw_input("Enter the name of a table to decompose into BNCF: ")
	columns = db.getColumnNames(table_name)
	fds = db.getFDSforTables(['Input_FDS_' + table_name.split('_')[1]])
	bcnf = compute_bcnf(columns, fds)

	db.create_new_schemas(bcnf, table_name.split('_')[1])
	print "New schema created!"
	for idx, s in enumerate(bcnf):
		output_table_name = "Output_" + table_name.split('_')[1] + '_' + ''.join(s['attributes'])
		fd_table_name = 'Output_FDS_' + table_name.split('_')[1] + '_' + ''.join(s['attributes'])
		print "Table " + str(idx + 1) + ': ' + output_table_name + " | FDs: " + fd_table_name

	response = raw_input("Fill new tables with data from original table (y/n)?: ")
	if response == 'y':
		db.move_data(table_name, bcnf)
		print "Succesfully filled new tables with data!"

	raw_input("Press enter to continue...")
