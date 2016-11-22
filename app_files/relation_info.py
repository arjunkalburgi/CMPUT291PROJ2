from database_files import database as db

def show_fds(action):
	if action == "Q": 
		return;
	else: 
		db.getFDSfor(action)
		show_fds(raw_input("\nChoose a table-number or 'Q'\n"))

def start(): 
	# Display Table Mapping 
	db.printTableNames()

	# Display Functional Dependencies 
	show_fds(raw_input("\nEnter a table's name to see their Functional Dependencies\n \
        	Or type 'Q' to go back.\n"))
