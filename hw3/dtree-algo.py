import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

def importdata():
    balance_data = pd.read_csv("dtree-data.dat",sep=r"\s+", engine="python")
    print("Dataset Length:", len(balance_data))
    print("Dataset Shape:", balance_data.shape)
    print("Dataset Head:\n", balance_data.head())
    balance_data = balance_data.replace({'T': 1, 'F': -1})
    return balance_data

def splitdataset(balance_data):
    X = balance_data.iloc[:, :-1].values
    Y = balance_data.iloc[:, -1].values
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=100)
    return X, Y, X_train, X_test, y_train, y_test

def train_using_entropy(X_train, y_train):
    clf_entropy = DecisionTreeClassifier(criterion="entropy", max_depth=2, min_samples_leaf=5)
    clf_entropy.fit(X_train, y_train)
    return clf_entropy

def plot_decision_tree(clf_object, feature_names, class_names):
    plt.figure(figsize=(10, 7))
    plot_tree(clf_object, filled=True, feature_names=feature_names, class_names=class_names, rounded=True)
    plt.show()

if __name__ == "__main__":
 
    data = importdata()
    X, Y, X_train, X_test, y_train, y_test = splitdataset(data)
    feature_names = list(data.columns[:-1])
    class_names = list(map(str, np.unique(Y)))
    
    print("\n----- Training Using Entropy -----")
    clf_entropy = train_using_entropy(X_train, y_train)
    plot_decision_tree(clf_entropy, feature_names, class_names)