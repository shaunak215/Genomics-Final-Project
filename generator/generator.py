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

    if len(zerol) != 0: 
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
        G = nx.relabel_nodes(G, d, copy=True)
    return G 

def cond2(G, Gn):
    # Generate the alphabet for the labels
    alphabet_string = list(string.ascii_lowercase)

    edges = list(G.edges(data=True))
    num_chars = len(edges) / 4
    if num_chars < 1:
        num_chars = 1
    chars = alphabet_string[:int(num_chars)] 

    # Fix graph for condition 2
    # Add a check that # of edges is > than # of alphabet characters
    # Add edge labels randomly
    edges = list(Gn.edges())
    # print(edges)
    edges.sort(key=lambda x: x[1])

    # Find out the length for the partitions
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
    seen = set()
    for i in range(len(l)):
        # get the highest node for that partition
        for tuple in l[i]:
            if tuple not in seen:
                filtered_list[i].add(tuple)
                seen.add(tuple)
        max_out_node = l[i][-1][1]
        # check the subsequent partitions
        for j in range(i + 1, len(l)):
            for tuple in l[j]:
                # if the node matches, pull in down to the current partition
                if tuple[1] == max_out_node and tuple not in seen:
                    filtered_list[i].add(tuple)
                    seen.add(tuple)

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

def generateWG(num_nodes, edge_prob, visualize, output_file, randomize):

    #Create a random graph
    G = nx.gnp_random_graph(num_nodes, edge_prob, directed=True)
    Gn = cond1(G)
    lis = cond2(G,Gn)
    cond3(Gn)
    redoCondOne(Gn)

    output_file_samples = "samples" + output_file
    nx.drawing.nx_pydot.write_dot(Gn, output_file_samples)
    # con1, con2, con3 = checker(output_file)
    # print(str(con1) + str(con2) + str(con3))

    if visualize:
        s = Source.from_file(output_file)
        print(s.view())

    if randomize: 
        output_file_before = "before_shuffle"  + output_file
        nx.drawing.nx_pydot.write_dot(Gn, output_file_before)
        num_nodes = len(Gn.nodes())
        new_list = list(range(0,num_nodes))
        random.shuffle(new_list)
        
        string_list = []
        for i in new_list:
            val = "S" + str(i)
            string_list.append(val)

        new_labels = {}
        curr_nodes = list(Gn.nodes)
        for i in curr_nodes:
            new_labels[i] = string_list.pop(0)

        Gn = nx.relabel_nodes(Gn, new_labels)
        output_file_after = "after_shuffle" + output_file
        nx.drawing.nx_pydot.write_dot(Gn, output_file_after)


    # return con1, con2, con3, lis, num_nodes
    # return num_nodes