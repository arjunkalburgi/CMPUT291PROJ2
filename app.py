import sqlite3
import os

from app_files import NF3_decomp
from app_files import BCNF_decomp
from app_files import attr_closure
from app_files import func_dep
from app_files import relation_info

from database_files import database

def connect_database():
	path = raw_input("Enter the path to database file (enter for default): ")
	if path == "":
		path = 'database_files/MiniProject2-InputExample.db'
	database.connectDB(path)
	print "Connected to database at " + path

def main():
	print "Welcome to the Normalization Application!"
	while True:
		print "---------------------------------------------------------------"
		print "Choose what to do:\n \
        	1. Relation Info\n \
        	2. Perform 3NF Decomposition\n \
        	3. Perform BCNF Decomposition\n \
        	4. Determine Attribute Closure\n \
        	5. Determine Functional Dependencies Equivalence\n \
        	6. Quit\n"

		action = raw_input("Enter a number: ")

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

if __name__  == "__main__":
	connect_database()
	main()
