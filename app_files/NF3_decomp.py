from database_files import database as db
from app_files.attr_closure import compute_attribute_closure as at_cl
import itertools

def remove_lhs_redundancies(f):
	for fd in f: 
		for attr in list(fd['LHS']): 
			closure = at_cl(list(fd['LHS'].replace(attr,"")), f)
			if fd['RHS'] in closure or attr in closure: 
				fd["LHS"] = fd["LHS"].replace(attr, "")
	return f

def remove_fds(f): 
	# closure = []
	# alt_closure = []
	for fd in f: 
		
		f.remove(fd)
		closure = at_cl(list(fd['LHS']), f)
		if fd['RHS'] not in closure: 
			f.append(fd)

	return f

def minimal_cover(f): 
	# f = [{'LHS': 'ABH', 'RHS': 'CK'}, {'LHS': 'A', 'RHS': 'D'}, {'LHS': 'C', 'RHS': 'E'}, {'LHS': 'BGH', 'RHS': 'F'}, {'LHS': 'F', 'RHS': 'AD'}, {'LHS': 'E', 'RHS': 'F'}, {'LHS': 'BH', 'RHS': 'E'}]
	# t = {'name': 'Input_R1', 'sql': 'CREATE TABLE....', 'attributes': {'A':'INT','B':'INT',...}}

	# RHS to single element
	for fd in f: 
		if len(fd["RHS"])>1: 
			for attr in list(fd["RHS"]): 
				f.append({'LHS': fd['LHS'], 'RHS': attr})
			f.remove(fd)

	# remove redundancies from LHS and redundance FDs
	f = remove_lhs_redundancies(f)
	f = remove_fds(f)

	# combine similar fds
	for fd in f: 
		rhs = fd['RHS']
		lhs = fd['LHS']
		f.remove(fd)
		small_f = f
		for small_fd in small_f: 
			if small_fd['LHS'] == lhs: 
				fd['RHS'] = fd['RHS'] + small_fd['RHS']
				f.remove(small_fd)
		f.append(fd)

	# now f is minimal cover!
	return f

def start(): 
	table = db.chooseTable() # user chooses a table
	fds = db.getFDSfor(table['name']) # we get FDs 
	db.printFDSfor(table['name'])

	# minimal cover
	fds = minimal_cover(fds)

	# partition
	db.partition(fds, table)
