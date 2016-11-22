import sqlite3
import os

from app_files import NF3_decomp
from app_files import BCNF_decomp
from app_files import attr_closure
from app_files import func_dep
from app_files import relation_info

from database_files import database

def connect_database():
	path = raw_input("path (and file) of database: ")
    if path == "":
        database.connectDB('database_files/MiniProject2-InputExample.db')
    else:
        database.connectDB(path)

def main():
	while True:
		action = raw_input("\Choose what to do\n \
        	1. Relation Info\n \
        	2. Perform 3NF Decomposition\n \
        	3. Perform BCNF Decomposition\n \
        	4. Determine Attribute Closure\n \
        	5. Determine Functional Dependencies Equivalence\n \
        	6. Quit\n")
        
		if action == "1":
				relation_info.start()
		elif action == "2":
			NF3_decomp.start()
		elif action == "3":
			BCNF_decomp.start()
		elif action == "4":
			attr_closure.start()
		elif action == "5":
			func_dep.start()
		elif action == "6":
			break;
		else:
	    		print("Unknown input, please type a number")

	print("Bye")

if __name__  == "__app__":
	connect_database()
	main()

	
