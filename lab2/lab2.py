import sys

#py lab2.py testcases/functions/f1.cnf
# if len(sys.argv) < 2:
#     print("Usage: python3 lab2.py KB.cnf")
#     sys.exit(1)

function = sys.argv[1]
# function = "lab2/testcases/constants/c03.cnf"
# function = "lab2/testcases/functions/f1.cnf"
lines = []

with open(function, 'r') as file:
    lines = [line.split() for line in file]

predicates = set(lines[0][1:])
variables = set(lines[1][1:])
constants = set(lines[2][1:])
functions = set(lines[3][1:])
compounds = set()
clauses = lines[5:]

def parseTerm(term):
    if "(" not in term:
        return term
    
    name, args = term.split('(',1)
    args = args[:-1].split(',')
    parsed_args = tuple(parseTerm(arg) for arg in args)
    parsed_term = (name, parsed_args)
    compounds.add(parsed_term)

    return parsed_term


def parseClauses(clauses):
    knowledge_base = set()
    for clause in clauses:
        parsed_clause = set()
        for predicate in clause:
            not_negated = True
            if predicate.startswith("!"):
                predicate = predicate[1:]
                not_negated = False
            parsed_clause.add((parseTerm(predicate),not_negated))
        knowledge_base.add(tuple(parsed_clause))
    return knowledge_base

#knowledge_base in the form (clause, clause, ...)
#clause in the form tuple(predicate, predicate, ...)
#predicate in the form ((predicate_name, (term, term, ...)), true or false) or (predicate_name, true or false)
#term in the form: constant, variable, or (function, (term, term))
knowledge_base = parseClauses(clauses)

def unifyVar(var, x, theta):
    if var in theta:
        return unify(theta[var],x,theta)
    elif x in theta:
        return unify(var, theta[x],theta)
    elif x in compounds:
        if var in x[1]:
            return None
    else:
        theta[var] = x
        return theta
    
def unify(x,y,theta=None):
    if theta == None:
        theta = {}
    elif x == y:
        return theta
    elif x in variables:
        return unifyVar(x,y,theta)
    elif y in variables:
        return unifyVar(y,x,theta)
    elif x in compounds and y in compounds:
        return unify(x[1],y[1],unifyVar(x[0],y[0],theta))
    else:
        return None

def isComplementary(predicate1,predicate2):
    theta = unify(predicate1[0],predicate2[0])
    return theta is not None and predicate1[1]!=predicate2[1], theta

def apply_unification(term, theta):
    if term in variables or term in constants:
        return theta.get(term, term)
    else:
        name, args = term
        new_args = tuple(apply_unification(arg,theta) for arg in args)
        return (name, new_args)

def resolve(clause1, clause2):
    resolved_clauses = set()
    print("{0} {1}".format(clause1,clause2))
    for predicate1 in clause1:
        for predicate2 in clause2:
            complementary, theta = isComplementary(predicate1,predicate2)
            if complementary:
                new_clause = (set(clause1) - {predicate1}) | (set(clause2) - {predicate2})
                unified_clause = set()
                for predicate, not_negative in new_clause:
                    unified_predicate = apply_unification(predicate, theta)
                    unified_clause.add((unified_predicate,not_negative))
                resolved_clauses.add(tuple(unified_clause))
    print("{0}".format(resolved_clauses))
    return(resolved_clauses)
                
def resolution(knowledge_base):
    while True:
        new = set()

        clauses = list(knowledge_base)
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):

                resolved_clauses = resolve(clauses[i],clauses[j])

                if () in resolved_clauses:
                    return False
                
                new |= resolved_clauses

        if new.issubset(knowledge_base):
            return True
        knowledge_base |= new
        
print(resolution(knowledge_base))