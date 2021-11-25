import networkx as nx
from graphviz import Source
import string
import random
from itertools import islice
import sys
sys.path.append("..")
from checker.checker import checker
import math


def cond1(G):
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

    # map the old nodes to the new ones
    return nx.relabel_nodes(G, d, copy=True)


def cond2(G, Gn):
    # Generate the alphabet for the labels
    alphabet_string = list(string.ascii_lowercase)

    edges = list(G.edges(data=True))
    num_chars = len(edges) / 4
    chars = alphabet_string[:int(num_chars)]  # Make this a user specified amount

    # Fix graph for condition 2
    # Add a check that # of edges is > than # of alphabet characters
    # Add edge labels randomly
    edges = list(Gn.edges())
    edges.sort(key=lambda x: x[1])

    # Find out the length for the partitions
    # Should change to be random, but also this works I guess
    num_edges = len(edges)
    alp_size = len(chars)
    step_size = math.floor(len(edges) / alp_size)
    leftover = (num_edges - step_size * (alp_size - 1))

    # Create the partitions for assigning labels
    length_to_split = []
    for i in range(alp_size - 1):
        length_to_split.append(step_size)
    length_to_split.append(leftover)

    Inputt = iter(edges)
    l = [list(islice(Inputt, elem))
         for elem in length_to_split]

    # Create a new filtered list that will shift items based on
    # if they violate condition 2
    filtered_list = [set() for i in range(len(l))]
    # by default the first partition won't violate anything bc no prev partition
    for tuple in l[0]:
        filtered_list[0].add(tuple)

    # SOMETHING IS WRONG HERE
    for i in range(len(l) - 1):
        # get the highest node for that partition
        max_out_node = l[i][-1][1]
        # check the subsequent partitions
        for j in range(i + 1, len(l)):
            # print("j: " + str(j))
            for tuple in l[j]:
                # if the node matches, pull in down to the current parition
                if tuple[1] == max_out_node:
                    filtered_list[i].add(tuple)
                # otherwise add it to where it to next partition
                else:
                    filtered_list[j].add(tuple)  # actually should this be j idk ? was i+1 before

    # if you comment this out it doesnt work
    # this basically fixes the mistake im making above
    for i in range(len(filtered_list) - 1):
        for tuple in filtered_list[i]:
            if tuple in filtered_list[i + 1]:
                filtered_list[i + 1].remove(tuple)

    # Assign labels to edges based on partitions we defined
    l = filtered_list
    labels = {}
    count = 0
    for i in l:
        for edge in i:
            u = edge[0]
            v = edge[1]
            tempmap = {"label": chars[count]}
            labels[(u, v)] = tempmap
        count += 1
    nx.set_edge_attributes(Gn, labels)


    return l


def cond3(G):
    # Fix graph for condition 3. Remove any edge that violates condition 3
    edges = list(G.edges(data=True))
    d = {}
    for u, v, edge in edges:
        label = edge["label"]
        if label in d:
            l = d.get(label)
            l.append((u, v))
        else:
            d[label] = [(u, v)]

    for k, v in d.items():
        max = 0
        for out, ind in sorted(v):
            if int(ind) < int(max):
                G.remove_edge(out, ind)
            if int(ind) > int(max):
                max = ind

def redoCondOne(G):
    # FIXING NEW CASES OF ZERO IN DEGREE
    highest_zero_node = -1
    zeroes = sorted(list(G.in_degree(G.nodes())))
    zerol = []
    stop = False
    for node, indeg in zeroes:
        if indeg == 0 and not stop:
            zerol.append(int(node))
            highest_zero_node = node
        elif indeg == 0:
            zerol.append(int(node))
        else:
            stop = True

    to_delete = list(filter(lambda high: high > highest_zero_node, zerol))

    while (len(to_delete) > 0):
        for node in to_delete:
            G.remove_node(node)

        zeroes = sorted(list(G.in_degree(G.nodes())))
        zerol = []
        stop = False
        for node, indeg in zeroes:
            if indeg == 0 and not stop:
                zerol.append(int(node))
                highest_zero_node = node
            elif indeg == 0:
                zerol.append(int(node))
            else:
                stop = True

        to_delete = list(filter(lambda high: high > highest_zero_node, zerol))

def generateWG(num_nodes, edge_prob, visualize, output_file):

    con1 = False
    con2 = False 
    con3 = False 

    # while not con1 or not con2 or not con3:
    #Create a random graph
    G = nx.gnp_random_graph(num_nodes, edge_prob, directed=True)
    Gn = cond1(G)
    lis = cond2(G,Gn)
    cond3(Gn)
    redoCondOne(Gn)

    nx.drawing.nx_pydot.write_dot(Gn, output_file)
    con1, con2, con3 = checker(output_file)
    # print(str(con1) + str(con2) + str(con3))

    if visualize:
        s = Source.from_file(output_file)
        print(s.view())

    num_nodes = len(Gn.nodes())
    # print(num_nodes)

    return con1, con2, con3, lis, num_nodes