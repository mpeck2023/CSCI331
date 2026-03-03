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

temp_clauses = []
for clause in clauses:
    temp_clause=[]
    for predicate in clause:
        temp_predicate = []
        predicate = predicate[0:-1].split('(',1)
        if predicate[0][0] == "!":
            predicate[0] = predicate[0][1:]
            predicate.append(False)
        else:
            predicate.append(True)
        predicate[1] = predicate[1].split(',')
        for argument in predicate[1]:
            if argument.startswith("SKF"):
                argument = argument[0:-1].split('(',1)
            temp_predicate.append(argument)
        predicate[1] = temp_predicate
        temp_clause.append(predicate)
    temp_clauses.append(temp_clause)
clauses = temp_clauses

print(clauses)
    