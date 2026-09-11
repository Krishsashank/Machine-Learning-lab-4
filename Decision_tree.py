
import math
import csv
import pandas as pd

file_path = r"C:\Users\CSE Lab\Downloads\Studentdata.csv"

df = pd.read_csv(file_path)

def entropy(data):
    count = {}
    total = len(data)

    for row in data:
        label = row[-1]
        count[label] = count.get(label, 0) + 1

    ent = 0
    for c in count.values():
        p = c / total
        ent -= p * math.log2(p)

    return ent

def split_data(data, feature_index, value):
    subset = []

    for row in data:
        if row[feature_index] == value:
            new_row = row[:feature_index] + row[feature_index+1:]
            subset.append(new_row)

    return subset

def information_gain(data, feature_index):
    total_entropy = entropy(data)

    values = []
    for row in data:
        if row[feature_index] not in values:
            values.append(row[feature_index])

    weighted_entropy = 0

    for value in values:
        subset = split_data(data, feature_index, value)
        weighted_entropy += (len(subset)/len(data)) * entropy(subset)

    return total_entropy - weighted_entropy


def build_tree(data, feature_names):

    labels = [row[-1] for row in data]

    if labels.count(labels[0]) == len(labels):
        return labels[0]

    if len(feature_names) == 0:
        return majority_class(data)

    best_gain = -1
    best_feature = -1

    for i in range(len(feature_names)):
        gain = information_gain(data, i)
        if gain > best_gain:
            best_gain = gain
            best_feature = i

    tree = {feature_names[best_feature]: {}}

    values = []

    for row in data:
        if row[best_feature] not in values:
            values.append(row[best_feature])

    for value in values:
        subset = split_data(data, best_feature, value)
        new_features = feature_names[:best_feature] + feature_names[best_feature+1:]
        subtree = build_tree(subset, new_features)
        tree[feature_names[best_feature]][value] = subtree

    return tree

def print_tree(tree, indent=""):

    if not isinstance(tree, dict):
        print(indent + "── Leaf :", tree)
        return

    for feature, branches in tree.items():
        print(indent + "Root -> " + feature)

        for value, subtree in branches.items():
            print(indent + "── " + value)
            print_tree(subtree, indent + "│   ")

decision_tree = build_tree(dataset, features)

print("Decision Tree Information Gain\n")
print_tree(decision_tree)