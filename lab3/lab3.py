import sys
import numpy as np
import pickle
import matplotlib.pyplot as plt

class TreeNode:
    def __init__(self, question):
        self.question = question
        self.children = []

    def add_child(self, child_node):
        self.child_node = child_node

    def get_children(self):
        return self.children

    def get_question(self):
        return self.question

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
    outcomes_examples = [example.split('|') for example in examples]
    outcomes_examples = np.array(outcomes_examples)
    Y = outcomes_examples[:,0]
    examples = outcomes_examples[:,1]
    data = np.append(parse_data(examples, features), Y, 1)
    return data

def parse_data(examples, features):
    X_array = [[feature in example for feature in features] for example in examples]
    X = np.array(X_array)
    return X

def split_train_test(data, test_size = 0.3):
    split = int(test_size*data.shape[0])
    train_data = data[:split,:]
    test_data = data[split:,:]
    X_train = train_data[:,:-1]
    Y_train = train_data[:,-1]
    X_test = test_data[:,:-1]
    Y_test = test_data[:,-1]
    return X_train, X_test, Y_train, Y_test

# returns tuple (majority classification, count)
def majority_answer(examples):
    max((examples)) #replace
    return

def importance(attribute, examples):
    return

def decision_tree(examples, attributes, parent_examples):
    attributes = []
    if len(examples) == 0:
        return majority_answer(parent_examples)[0]
    if majority_answer(examples)[1] == len(examples):
        return majority_answer(examples)[0]
    if len(attributes) == 0:
        return majority_answer(examples)[0]
    importance_list = [importance(a,examples) for a in attributes]
    A = np.argmax(importance_list)
    tree = TreeNode(question=attributes(A))
    for value in attributes[A]: # looping through the possible values of attribute A
        examples_with_value = [e for e in examples if e[A] == value]
        tree.add_child(decision_tree(examples_with_value,attributes[0:A]+attributes[A+1:],examples))
    return tree

def train(data, hypothesis_filename, learning_type):
    X_train, X_test, Y_train, Y_test = split_train_test(data, test_size=0.3)
    with open(hypothesis_filename, 'w') as hypothesis_out:
        return
    entropy_tree = "Decision tree classifier"
    entropy_tree.fit(X_train, Y_train)
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
    tree = train(data, hypothesis_filename, learning_type)
else:
    data = parse_data(examples, features)
    prediction = predict(data, hypothesis_filename)

class_names = list(map(str, np.unique(Y)))

plot_decision_tree(tree, features, class_names)