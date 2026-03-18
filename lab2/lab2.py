import sys

#py lab2.py testcases/functions/f1.cnf
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

def parseClauses(clauses):
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
            for term in predicate[1]:
                if term.startswith("SKF"):
                    term = term[0:-1].split('(',1)
                temp_predicate.append(term)
            predicate[1] = temp_predicate
            temp_clause.append(predicate)
        temp_clauses.append(temp_clause)
    return temp_clauses

#knowledge_base in the form [clause, clause, ...]
#clause in the form [predicate, predicate, ...]
#predicate in the form [predicate_name, [term, term, ...], true or false]
#term in the form: constant, variable, or [function, term]
knowledge_base = parseClauses(clauses) 

def resolve(clause1, clause2):
    resolved_clause = []
    for predicate1 in clause1:
        for predicate2 in clause2:
            if predicate1[0:2] != predicate2[0:2] or predicate1[2] == predicate1[2]:
                resolved_clause.append(predicate1)
    return resolved_clause
                
def resolution(knowledge_base):
    new = []
    knowledge_base = []
    while len(knowledge_base):
        for clause1 in knowledge_base:
            for clause2 in knowledge_base[1:]:
                resolve(clause1,clause2)