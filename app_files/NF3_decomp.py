from database_files import database as db
from app_files.attr_closure import compute_attribute_closure as at_cl
import itertools

def check_redundency(LHS, RHS, f): 
	if len(LHS) > 1:
		lhs_combos = itertools.combinations(LHS, len(LHS)-1)
		
		for lhs_combo in lhs_combos:
			lhs_combo = list(lhs_combo)
			closure = at_cl(lhs_combo,f)

			if set(RHS).issubset(closure):
				f.remove({'LHS': LHS, 'RHS': RHS})
				f.append({'LHS': "".join(lhs_combo), 'RHS': RHS})
				return check_redundency("".join(lhs_combo), RHS, f)
		return f
	else:
		return f

def remove_redundancies(f): 
	trimmed_f = f
	for fd in f: 
		print(fd['LHS'])
		print(fd['RHS'])
		print(f)
		trimmed_f = check_redundency(fd['LHS'], fd['RHS'], f)
		print(trimmed_f)
		print("")
		print("")
		if trimmed_f is not f: 
			break; 
	if trimmed_f is not f: 
		trimmed_f = remove_redundancies(trimmed_f)
	return trimmed_f 

def remove_fds(f): 
	closure = []
	alt_closure = []
	for fd in f: 
		LHS = fd['LHS']

		# is closure for LHS the same as closure without FD
		closure = at_cl(list(LHS), f)
		f.remove(fd)
		alt_closure = at_cl(list(LHS), f)

		if closure == alt_closure: 
			break; 
		else: 
			f.append(fd)

	if alt_closure == closure: 
		f = remove_fds(f)

	return f

def minimal_cover(f): 
	# f = [{'LHS': 'ABH', 'RHS': 'CK'}, {'LHS': 'A', 'RHS': 'D'}, {'LHS': 'C', 'RHS': 'E'}, {'LHS': 'BGH', 'RHS': 'F'}, {'LHS': 'F', 'RHS': 'AD'}, {'LHS': 'E', 'RHS': 'F'}, {'LHS': 'BH', 'RHS': 'E'}]
	# t = {'name': 'Input_R1', 'sql': 'CREATE TABLE....', 'attributes': {'A':'INT','B':'INT',...}}
	# old_f = f # preserve f

	# RHS to single element
	for fd in f: 
		if len(fd["RHS"])>1: 
			for attr in fd["RHS"].split(","): 
				f.append({'LHS': fd['LHS'], 'RHS': attr})
			f.remove(fd)

	# remove redundancies from LHS and redundance FDs
	f = remove_redundancies(f)
	f = remove_redundancies(f)
	f = remove_fds(f)

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
