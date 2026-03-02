import sys

if len(sys.argv) < 2:
    print("Usage: python3 lab2.py KB.cnf")
    sys.exit(1)

function = sys.argv[1]
lines = []

with open(function, 'r') as file:
    lines = [line.split() for line in file]

predicates = set(lines[0][1:])
variables = set(lines[1][1:])
constants = set(lines[2][1:])
functions = set(lines[3][1:])
clauses = lines[5:]

clauses = [[predicate[0:-1].split('(',1) for predicate in clause] for clause in clauses]

print(clauses)
    