import networkx as nx
import matplotlib.pyplot as plt
import graphviz
from graphviz import Source
import string
import random
import numpy as np
from itertools import islice
from checker import checker
import math

con1, con2, con3 = False, False, False

# while not con1 or not con2 or not con3: 

G = nx.gnp_random_graph(10, .1, directed=True)

# Fix graph for condition 1: all zero in degree nodes come before others
zeroes = sorted(list(G.in_degree(G.nodes())))
zerol = []
nonzero = []
for node, indeg in zeroes:
    if indeg == 0:
        zerol.append(node)
    else:
        nonzero.append(node)

num = len(zerol)
d = dict()
count = 0
for i in zerol:
    d[i] = count
    count += 1

for i in range(len(nonzero)):
    d[nonzero[i]] = num
    num += 1

Gn = nx.relabel_nodes(G, d, copy = True)
alphabet_string = list(string.ascii_lowercase)
# Make this a user specified amount
chars = alphabet_string[:4]

# Fix graph for condition 2
# Add a check that # of edges is > than # of alphabet characters
# Add edge labels randomly
edges = list(Gn.edges())
edges.sort(key=lambda x: x[1])

print(len(edges))
num_edges = len(edges)
alp_size = len(chars)

step_size = math.floor(len(edges)/alp_size) 
leftover = (num_edges - step_size * (alp_size - 1))

length_to_split = []
for i in range(3):
    length_to_split.append(step_size)
length_to_split.append(leftover)

# print(length_to_split)


Inputt = iter(edges)
l = [list(islice(Inputt, elem))
          for elem in length_to_split]

print(l)
# print(edges)

labels = {}
count = 0
for i in l:
    for edge in i:
        u = edge[0]
        v = edge[1]
        tempmap = {"label": chars[count]}
        labels[(u,v)] = tempmap
    count += 1

nx.set_edge_attributes(Gn, labels)

nx.drawing.nx_pydot.write_dot(Gn, 'current.dot')
con1, con2, con3 = checker('current.dot')
# print(str(con1) + " " + str(con2) + " " + str(con3))

edges = list(Gn.edges(data=True))
edges.sort(key=lambda x: x[1])
print(edges)

# Fix graph for condition 3

print(str(con1) + " " + str(con2) + " " + str(con3))

dot = open("current.dot")
s = Source.from_file("./current.dot")
print(s.view())