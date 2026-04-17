import sys
from queue import Queue

# if len(sys.argv) < 4:
#     print("Usage: python3 hw1.py <dictionary file name> <start word> <target word>")
#     sys.exit(1)

# filename,start,target = sys.argv[1:]
filename,start,target = "words","ready","minds"
start,target = start.lower(), target.lower()

if len(start) != len(target):
    print("Length of start and target words must be equal")
    sys.exit(1)

def isGoal(word):
    return word == target

if isGoal(start):
    print(start+"\n"+target)
    sys.exit(1)

with open(filename, 'r', encoding='utf-8') as file:
    words = file.readlines()

word_set = {word.strip().lower() for word in words if len(word.strip()) == len(start)}
word_parent = {word: "" for word in word_set}

def find_neighbors(word):
    neighbors = []
    for i in range(len(word)):
        for c in "abcdefghijklmnopqrstuvwxyzàáâãäåæçèéêëìíîïðñòóôõö":
            if c != word[i]:
                possible_neighbor = word[:i] + c + word[i+1:]
                if possible_neighbor in word_set:
                    neighbors.append(possible_neighbor)
    return neighbors

neighbors = {word: find_neighbors(word) for word in word_set}

def update_parent(word, parent):
    word_parent[word] = parent

def path_to_top(word):
    current = word
    path = []
    path.append(current)
    while current != start:
        current = word_parent[current]
        path.append(current)
    return path

visited = set()
frontier_set = {start}
frontier = Queue()
frontier.put(start)
while not frontier.empty():
    current = frontier.get()
    visited.add(current)
    for neighbor in neighbors[current]:
        if neighbor not in visited and neighbor not in frontier_set:
            frontier.put(neighbor)
            frontier_set.add(neighbor)
            update_parent(neighbor,current)
            if isGoal(neighbor):
                path = path_to_top(neighbor)
                while path:
                    print(path.pop())
                sys.exit(1)
print("No solution")
sys.exit(1)