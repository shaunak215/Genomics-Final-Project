import networkx as nx
import matplotlib.pyplot as plt
import graphviz
from graphviz import Source
import sys
sys.path.append("..")
from checker.checker import checker

G = nx.MultiDiGraph()
# G = nx.gnp_random_graph(10, .2, directed=True)
# indegree = sorted(list(G.in_degree(G.nodes())))
# print(indegree)


G.add_node(0)
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)
G.add_node(6)
G.add_node(7)
G.add_node(8)


# G.add_edge(0, 1, label="b")
# G.add_edge(2, 1, label="b")
# G.add_edge(0, 2, label="g")
# G.add_edge(2, 2, label="g")
# G.add_edge(4, 3, label="g")
# G.add_edge(5, 3, label="g")
# G.add_edge(6, 4, label="g")
# G.add_edge(2, 5, label="r")
# G.add_edge(4, 5, label="r")
# G.add_edge(5, 6, label="r")
# G.add_edge(6, 6, label="r")

# G.add_edge(2, 1, label="b")
# G.add_edge(0, 2, label="g")
# G.add_edge(2, 2, label="g")
# G.add_edge(4, 3, label="g")
# G.add_edge(5, 3, label="g")
# G.add_edge(6, 4, label="g")
# G.add_edge(2, 5, label="r")
# G.add_edge(4, 5, label="r")
# G.add_edge(5, 6, label="r")
# G.add_edge(6, 6, label="r")

nx.drawing.nx_pydot.write_dot(G, 'multi.dot')

dot = open("multi.dot")
s = Source.from_file("./multi.dot")
print(s.view())