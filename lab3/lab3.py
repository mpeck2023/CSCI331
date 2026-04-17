import sys
import numpy as np
import pandas as pd
import pickle
import graphviz

# returns tuple (majority classification, count)

def entropy(outcomes):
    counts = outcomes.value_counts()
    total = counts.sum()
    entro = 0.0
    for count in counts:
        p = count/total
        entro += p * np.log2(1/p)
    return entro


def importance(examples, attribute):
    gain += entropy(examples["outcomes"])
    for value in pd.unique(examples[attribute]):
        examples_with_value = examples.loc[examples[attribute] == value]
        gain -= len(examples_with_value)/len(examples) * entropy(examples_with_value["outcomes"])
    return gain

def majority_answer(examples):
    return examples["output"].mode()[0]

class TreeNode:
    def __init__(self, question = '', entropy = '', counts = '', value = '', outcome = ''):
        self.question = question
        self.entropy = entropy
        self.counts = counts
        self.value = value
        self.outcome = outcome
        self.children = []

    def add_child(self, child_node):
        self.child_node = child_node

    def get_children(self):
        return self.children

    def get_question(self):
        return self.question
    
def decision_tree(examples, parent_examples, prev_value=''):
    if len(examples) == 0:
        return TreeNode(outcome=majority_answer(parent_examples))
    
    if len(pd.unique(examples["output"])) == 1:
        return TreeNode(outcome=majority_answer(examples))
    
    if len(examples.columns) == 0:
        return TreeNode(outcome=majority_answer(examples))
    
    importance_list = pd.Series({a: importance(a,examples) for a in examples.columns})
    attribute = importance_list.idxmax()
    counts = examples["outcomes"].value_counts()
    tree = TreeNode(question=attribute,
                    entropy=importance_list[attribute],
                    counts=counts,
                    value=prev_value)
    for value in pd.unique(examples[attribute]): # looping through the possible values of attribute A
        examples_with_value = examples.loc[examples[attribute] == value]
        tree.add_child(decision_tree(examples_with_value.drop(columns=attribute),examples,value))
    return tree

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
    with open(filename, 'r') as file:
        return file.readlines()
    
def parse_training_data(examples, features):
    outcomes, examples = [example.split('|') for example in examples]
    outcomes = np.array(outcomes)
    examples = np.array(examples)
    data = np.append(parse_data(examples, features), outcomes, 1)
    data = pd.DataFrame(data,columns=features+"outcome")
    return data

def parse_data(examples, features):
    X_array = [[feature in example for feature in features] for example in examples]
    X = np.array(X_array)
    return X

def split_train_test(data, test_size = 0.3):
    split = int(test_size*data.shape[0])
    train_data = data.iloc[:split]
    test_data = data.iloc[split:]
    return train_data, test_data

def train(data, hypothesis_filename, learning_type):
    train_data, test_data = split_train_test(data, test_size=0.3)
    with open(hypothesis_filename, 'w') as hypothesis_out:
        return
    entropy_tree = decision_tree(train_data)
    return entropy_tree

def predict(hypothesis_filename):
    with open(hypothesis_filename, 'r') as hypothesis_file:
        hypothesis = pickle.load(hypothesis_file)
    return

def plot_tree(node, ax, x_axis=0, y_axis=10, space=5):
    if node.label is not None:
        ax.text(x_axis, y_axis, node.label, 
                bbox=dict(boxstyle='round', facecolor='green', edgecolor='g'), 
                ha='center', va='center')
    else:
        ax.text(x_axis, y_axis, f'{node.value:.2f}\nidx:{node.feature_idx}', 
                bbox=dict(boxstyle='round', facecolor='red', edgecolor='r'), 
                ha='center', va='center')
    
    if node.left:
        plot_tree(node.left, ax, x_axis - space, y_axis - space)
    if node.right:
        plot_tree(node.right, ax, x_axis + space, y_axis - space)

def plot_decision_tree(entropy_tree, feature_names, class_names):
    fig, ax = plt.subplots(1, 1)
    ax.axis('off')
    ax.set_aspect('equal')
    plot_tree(entropy_tree, ax)
    plt.show()

command, examples, features, hypothesis_filename, learning_type = parse_command()

if command == "train":
    data = parse_training_data(examples, features)
    tree = train(data, features, hypothesis_filename, learning_type)
else:
    data = parse_data(examples, features)
    prediction = predict(data, hypothesis_filename)

class_names = list(map(str, np.unique(Y)))

plot_decision_tree(tree, features, class_names)