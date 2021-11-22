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
highest_zero_node = num - 1
# print("num " + str(num-1))
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
for i in range(alp_size - 1):
    length_to_split.append(step_size)
length_to_split.append(leftover)

Inputt = iter(edges)
l = [list(islice(Inputt, elem))
          for elem in length_to_split]

#Create a new filtered list that will shift items based on
#if they violate condition 2 
filtered_list = [set() for i in range(len(l))]
#by default the first partition won't violate anything bc no prev partition
for tuple in l[0]: 
    filtered_list[0].add(tuple)

# print(l)
#SOMETHING IS WRONG HERE
for i in range(len(l)-1):
    #get the highest node for that partition
    max_out_node = l[i][-1][1]
    # print(max_out_node)
    #check the subsequent partitions
    for j in range(i+1, len(l)): 
        # print("j: " + str(j))
        for tuple in l[j]:
            #if the node matches, pull in down to the current parition
            if tuple[1] == max_out_node:
                filtered_list[i].add(tuple)
            #otherwise add it to where it to next partition
            else: 
                filtered_list[j].add(tuple) #actually should this be j idk ? was i+1 before
    # print(filtered_list)
    # print('\n')

#original partitions 
# for item in l:
#     print(item)

# print(filtered_list)
# print('\n')
#if you comment this out it doesnt work 
#this basically fixes the mistake im making above
for i in range(len(filtered_list) - 1):
    for tuple in filtered_list[i]:
        if tuple in filtered_list[i+1]:
            filtered_list[i+1].remove(tuple)
        
# print(filtered_list)

#fixed partitions
# for item in filtered_list:
#     print(item)
#EXAMPLE OF CASE THAT FAILS CONDITION 2
#original partitions
# [(5, 2), (7, 3)]
# [(1, 3), (3, 4)]
# [(6, 4), (8, 5)]
# [(3, 6), (2, 7), (3, 8), (0, 8), (8, 9)]

#new partitions
# {(1, 3), (7, 3), (5, 2)}
# {(6, 4), (3, 4)}
# {(6, 4), (8, 5)}
# {(3, 8), (2, 7), (8, 9), (3, 6), (0, 8)}


#ANOTHER CASE THAT ISNT TOTALLY CORRECT BUT WORKS?
# [(0, 1), (2, 1), (6, 1)]
# [(1, 2), (6, 3), (0, 4)]
# [(5, 4), (8, 4), (4, 5)]
# [(2, 6), (3, 7), (9, 8), (1, 9), (0, 9)]


# {(0, 1), (6, 1), (2, 1)}
# {(1, 2), (8, 4), (0, 4), (5, 4), (6, 3)}
# {(4, 5), (5, 4), (8, 4)}                  the ones ending in 4 shouldnt be in this partition bc they were moved up 
# {(3, 7), (0, 9), (2, 6), (9, 8), (1, 9)}


#Assign labels to edges based on partitions we defined
# print(l)
# print(filtered_list)
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



#commenting this out is buggy
nx.drawing.nx_pydot.write_dot(Gn, 'current.dot')
G = nx.drawing.nx_pydot.read_dot('current.dot')

edges = list(G.edges(data=True))
print(edges)

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

#FIXING NEW CASES OF ZERO IN DEGREE
zeroes = sorted(list(G.in_degree(G.nodes())))
zerol = []
# nonzero = []
for node, indeg in zeroes:
    if indeg == 0:
        zerol.append(int(node)) 
    # else:
    #     nonzero.append(node)
# print(highest_zero_node)
# print(zerol)

# filtered = filter(lambda score: score >= 70, scores)
to_delete = list(filter(lambda high: high > highest_zero_node, zerol))

while(len(to_delete) > 0):
# print(to_delete)
# G.remove_nodes_from(list(to_delete)) this should work but idk why it doesnt 

# print(to_delete)
    for node in to_delete:
        G.remove_node(str(node))
    
    zeroes = sorted(list(G.in_degree(G.nodes())))
    zerol = []
    # nonzero = []
    for node, indeg in zeroes:
        if indeg == 0:
            zerol.append(int(node)) 

    to_delete = list(filter(lambda high: high > highest_zero_node, zerol))
    

# for node in to_delete:
#     G.remove_node(str(node))

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