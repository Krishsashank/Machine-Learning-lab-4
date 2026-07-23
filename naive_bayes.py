import numpy as np
import pandas as pd

def prob(df, Cl, fea, var, cond, z):
    dff = df[df[Cl] == cond]
    n = len(dff)
    k = len(dff[dff[fea] == var])

    if z == 1:
        m = df[fea].nunique()      
        return (k + 1) / (n + m)

    return k/n

def validate(df, Cl, X):

    labels = df.columns[:-1]

    if len(X) != len(df.columns) - 1:
        return False, 0

    for i in range(len(labels)):
        if X[i] not in df[labels[i]].unique():
            return False, 0

    for c in df[Cl].unique():
        for i in range(len(labels)):
            if prob(df, Cl, labels[i], X[i], c, 0) == 0:
                return True, 1

    return True, 0

def form2(df, Cl, X, z):
    k, inti= 1, 0
    labels = df.columns.tolist()
    label = ""
    arr = []
    for i in df[Cl].unique():
        for j in range(len(labels) - 1):
            k = k * prob(df, Cl, labels[j], X[j], i, z)
        k = k * (len(df[df[Cl] == i]) / len(df))
        arr.append(k)
        if (k > inti):
            inti = k
            label = i
        k = 1
    j = 0
    for i in arr:
        j = j + i
    print("The Label will be: '", label, "' with probability: ", inti, "Its normalized value is: ", inti/j)

df = pd.read_csv("Id3data.csv")
df = df.drop(columns=["rid"])
Cl = "class"
Cl = input("Enter Class Label: ")

X = ["youth","low", "yes", "fair"]

print("Enter features: ")
X = []
for i in range(len(df.columns) - 1):
    ele = str(input())
    X.append(ele)
v, z = validate(df, Cl, X)
if v:
    form2(df, Cl, X, z)
else:
    print("The Input is wrong")