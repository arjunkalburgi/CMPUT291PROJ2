import sqlite3
import os
import NF3_decomp
import BCNF_decomp
import attr_closure
import func_dep
import relation_info

def connect_database():
	path = raw_input("path (and file) of database: ")
    if path == "":
        conn = sqlite3.connect('MiniProject2-InputExample.db')
    else:
        conn = sqlite3.connect(path)

def main():
	while True:
		action = raw_input("\nOptions\n \
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