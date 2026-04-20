import sys
import numpy as np
import pandas as pd
import pickle
import graphviz

max_depth = 3

class TreeNode:
    def __init__(self, question = '', entropy = '', counts = '', outcome = '', edge = ''):
        self.question = question
        self.entropy = entropy
        self.counts = counts
        self.outcome = outcome
        self.edge = edge
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __str__(self):
        return self.question + '\n' + str(self.entropy) + '\n' + str(self.counts) + '\n' + str(self.edge)
    def get_question(self):
        return self.question
    def get_edge(self):
        return self.edge
    def get_outcome(self):
        return self.outcome
    def get_children(self):
        return self.children
    def print_tree(self):
        print(self)
        for child in self.children:
            child.print_tree()

def entropy(Y):
    counts = Y.value_counts()
    total = counts.sum()
    entro = 0.0
    for count in counts:
        p = count/total
        entro += p * np.log2(1/p)
    return entro


def importance(examples, attribute):
    gain = entropy(examples['Y'])
    for value in pd.unique(examples[attribute]):
        examples_with_value = examples.loc[examples[attribute] == value]
        gain -= len(examples_with_value)/len(examples) * entropy(examples_with_value['Y'])
    return gain
    
def majority_answer(examples):
    return examples['Y'].mode()[0]
    
def decision_tree(examples, attributes, parent_examples=None,edge_label=None,depth=0):
    if depth == max_depth:
        return TreeNode(outcome=majority_answer(examples),edge=edge_label)

    if len(examples) == 0:
        return TreeNode(outcome=majority_answer(parent_examples,edge=edge_label))
    
    if len(pd.unique(examples['Y'])) == 1:
        return TreeNode(outcome=majority_answer(examples),edge=edge_label)

    if attributes == []:
        return TreeNode(outcome=majority_answer(examples),edge=edge_label)
    
    importance_list = pd.Series({a: importance(examples,a) for a in attributes})
    attribute = importance_list.idxmax()
    counts = examples['Y'].value_counts()
    tree = TreeNode(question=attribute,
                    entropy=importance_list[attribute],
                    counts=counts,
                    edge=edge_label,
                    outcome=majority_answer(examples))
    for value in pd.unique(examples[attribute]): # looping through the possible values of attribute A
        examples_with_value = examples.loc[examples[attribute] == value]
        tree.add_child(decision_tree(examples=examples_with_value.drop(columns=attribute),attributes=[a for a in attributes if a != attribute],parent_examples=examples,edge_label=value,depth=depth+1))
    return tree

def split_train_test(data, test_size = 0.3):
    split = int(test_size*data.shape[0])
    train_data = data.iloc[:split]
    test_data = data.iloc[split:]
    return train_data, test_data

def train(data, features, hypothesis_filename, learning_type):
    train_data, test_data = split_train_test(data, test_size=0.3)
    if learning_type == 'dt':
        return decision_tree(examples=train_data,attributes=features)
    elif learning_type == 'ada':
        return ada():

def predict_example(example, hypothesis):
    while True:
        if hypothesis.get_question() == '':
            return hypothesis.get_outcome()
        path = example[hypothesis.get_question()]
        children = hypothesis.get_children()
        for child in children:
            if str(child.get_edge()) == str(path):
                hypothesis = child

def predict(data,hypothesis_filename):
    with open(hypothesis_filename, 'rb') as hypothesis_file:
        hypothesis = pickle.load(hypothesis_file)
    for i, example in data.iterrows():
        print(predict_example(example,hypothesis))
            

# def build_tree(dot,node,prev_label=None):
#     node_label = ''
#     if node.get_question() == '':
#         node_label = node.get_edge()+prev_label+node.get_outcome()
#         dot.node(node_label, node.get_outcome())
#     else:
#         node_label = node.get_edge()+prev_label+node.get_question() if (node.get_edge()!=None) else node.get_question()
#         dot.node(node_label, str(node))
#     if prev_label != None:
#         dot.edge(prev_label,node_label,label = node.get_edge())
#     for child_node in node.get_children():
#         build_tree(dot,child_node,node_label)

# def plot_tree(node):
#     dot = graphviz.Digraph(comment="A graph", format="svg")
#     build_tree(dot,node)
#     dot.render('digraph.gv', view=True) 

def parse_training_data(examples, features):
    Y_examples = np.array([example.split('|') for example in examples])
    Y = Y_examples[:,0]
    examples = Y_examples[:,1]
    data = parse_data(examples, features)
    data['Y'] = Y
    return data

def parse_data(examples, features):
    X_array = [[feature in example for feature in features] for example in examples]
    X = pd.DataFrame(X_array,columns=features)
    return X

def parse_command():
    if len(sys.argv) < 5:
        print("Usage 1: python3 lab3.py train <examples> <features> <hypothesisOut> <learning-type>")
        print("Usage 2: python3 lab3.py predict <examples> <features> <hypothesis>")
        sys.exit(1)


    command = sys.argv[1]
    examples = get_lines(sys.argv[2])
    features = get_lines(sys.argv[3])
    hypothesis_filename = sys.argv[4]
    if len(sys.argv) == 5:
        learning_type = None
    else:
        learning_type = sys.argv[5]
    return command, examples, features, hypothesis_filename, learning_type

def get_lines(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

command, examples, features, hypothesis_filename, learning_type = parse_command()

if command == "train":
    data = parse_training_data(examples, features)
    tree = train(data, features, hypothesis_filename, learning_type)
    with open(hypothesis_filename, 'wb') as hypothesis_out:
        pickle.dump(tree,hypothesis_out)
    # plot_tree(tree)
else:
    data = parse_data(examples, features)
    prediction = predict(data, hypothesis_filename)