import networkx as nx
import matplotlib.pyplot as plt
import graphviz
from graphviz import Source

G = nx.MultiDiGraph()
G.add_edge(0, 1, label="b")
G.add_edge(2, 1, label="b")
G.add_edge(0, 2, label="g")
G.add_edge(2, 2, label="g")
G.add_edge(4, 3, label="g")
G.add_edge(5, 3, label="g")
G.add_edge(6, 4, label="g")
G.add_edge(2, 5, label="r")
G.add_edge(4, 5, label="r")
G.add_edge(5, 6, label="r")
G.add_edge(6, 6, label="r")

nx.drawing.nx_pydot.write_dot(G, 'multi.dot')
dot = open("multi.dot")
s = Source.from_file("./multi.dot")
print(s.view())


indegree = sorted(list(G.in_degree(G.nodes())))
flag = False
check0 = True
for node, indeg in indegree:
    if flag and indeg == 0:
        res = False
    if indeg != 0:
        flag = True
print(check0)

edges = list(G.edges(data=True))
d = {}
for u,v,edge in edges:
    label = edge['label']
    if label in d:
        l = d.get(label)
        l.append((u,v))
    else:
        d[label] = [(u,v)]

prev_max = 0
cond2 = True
for k,v in sorted(d.items()):
    cur_max = 0
    for (out,ind) in v:
        if (ind <= prev_max):
            cond2 = False
        if ind > cur_max:
            cur_max = ind
    prev_max = cur_max
print(cond2)


cond3 = True
for k,v in d.items():
    max = 0
    for out,ind in sorted(v):
        if ind < max:
            cond3 = False
        if ind > max:
            max = ind
print(cond3)

