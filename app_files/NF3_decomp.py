from database_files import database as db

def start(): 
	table = db.chooseTable() # user chooses a table
	fds = db.getFdsFor(table) # we get FDs 
	db.printFDSfor(table)

	# get 3NF dependencies 

	# perform decomposition
