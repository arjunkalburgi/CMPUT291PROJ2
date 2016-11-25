from database_files import database as db

def show_fds(action):
	if action == "Q":
		return;
	db.printFDSfor(action)
	# show_fds(raw_input("\nChoose a table-name or 'Q'\n"))

def start():
	# Display Table Mapping
	db.printTableNames()

	# Display Functional Dependencies
	show_fds(raw_input("\nEnter a table's name to see their Functional Dependencies\nOr type 'Q' to go back.\n"))
