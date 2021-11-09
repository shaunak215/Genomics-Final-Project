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