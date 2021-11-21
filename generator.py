import networkx as nx
import matplotlib.pyplot as plt
import graphviz
from graphviz import Source
import string
import random
from itertools import islice
from checker import checker
import math


#Create a random graph
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

#map the old nodes to the new ones 
Gn = nx.relabel_nodes(G, d, copy = True)

#Generate the alphabet for the labels
alphabet_string = list(string.ascii_lowercase)
chars = alphabet_string[:4] # Make this a user specified amount 

# Fix graph for condition 2
# Add a check that # of edges is > than # of alphabet characters
# Add edge labels randomly
edges = list(Gn.edges())
edges.sort(key=lambda x: x[1])

#Find out the length for the partitions 
#Should change to be random, but also this works I guess
num_edges = len(edges)
alp_size = len(chars)
step_size = math.floor(len(edges)/alp_size) 
leftover = (num_edges - step_size * (alp_size - 1))

#Create the partitions for assigning labels
length_to_split = []
for i in range(3):
    length_to_split.append(step_size)
length_to_split.append(leftover)

Inputt = iter(edges)
l = [list(islice(Inputt, elem))
          for elem in length_to_split]


#Create a new filtered list that will shift items based on
#if they violate condition 2 
filtered_list = [[] for i in range(len(l))]
#by default the first partition won't violate anything bc no prev partition
for tuple in l[0]: 
    filtered_list[0].append(tuple)

#SOMETHING IS WRONG HERE
for i in range(len(l)-1):
    #get the highest node for that partition
    max_out_node = l[i][-1][1]
    #check the subsequent partitions
    for j in range(i+1, len(l)): 
        for tuple in l[j]:
            #if the node matches, pull in down to the current parition
            if tuple[1] == max_out_node:
                filtered_list[i].append(tuple)
            #otherwise add it to where it to next partition
            else: 
                filtered_list[i+1].append(tuple) #actually should this be j idk ?

#Assign labels to edges based on partitions we defined
print(l)
print(filtered_list)
l = filtered_list
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


#Fix graph for condition 3 
#I don't know why but I had to write it the file and then 
#reread it in for the dictionary to then have the labels to 
#be able to key on them 
nx.drawing.nx_pydot.write_dot(Gn, 'current.dot')
G = nx.drawing.nx_pydot.read_dot('current.dot')

edges = list(G.edges(data=True))
d = {}
for u,v,edge in edges:
    label = edge["label"]
    if label in d:
        l = d.get(label)
        l.append((u,v))
    else:
        d[label] = [(u,v)]

for k,v in d.items():
    max = 0
    for out,ind in sorted(v):
        if int(ind) < int(max):
            G.remove_edge(out, ind)
        if int(ind) > int(max): 
            max = ind

nx.drawing.nx_pydot.write_dot(G, 'current.dot')

con1, con2, con3 = checker('current.dot')
# print(str(con1) + " " + str(con2) + " " + str(con3))

# edges = list(Gn.edges(data=True))
# edges.sort(key=lambda x: x[1])
# print(edges)


print(str(con1) + " " + str(con2) + " " + str(con3))

dot = open("current.dot")
s = Source.from_file("./current.dot")
print(s.view())