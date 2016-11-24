import sqlite3
import os

from app_files import NF3_decomp
from app_files import BCNF_decomp
from app_files import attr_closure
from app_files import func_dep
from app_files import relation_info

attrs = ['A','B','C','D','E','F','G','H']
fds = [{'LHS': 'A,B,H', 'RHS': 'C'}, {'LHS': 'A', 'RHS': 'D,E'}, {'LHS': 'B,G,H', 'RHS': 'F'}, {'LHS': 'F', 'RHS': 'A,D,H'}, {'LHS': 'B,H', 'RHS': 'G,E'}]
print BCNF_decomp.compute_bcnf(attrs,fds)

attrs = ['A','B','C','D','E','F','G','H', 'K']
fds = [{'LHS': 'A,B,H', 'RHS': 'C,K'}, {'LHS': 'A', 'RHS': 'D'}, {'LHS': 'C', 'RHS': 'E'}, {'LHS': 'B,G,H', 'RHS': 'F'}, {'LHS': 'F', 'RHS': 'A,D'}, {'LHS': 'E', 'RHS': 'F'}, {'LHS': 'B,H', 'RHS': 'E'}]
print BCNF_decomp.compute_bcnf(attrs,fds)
