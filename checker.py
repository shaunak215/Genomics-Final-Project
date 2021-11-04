import networkx as nx
import matplotlib.pyplot as plt
import graphviz
from graphviz import Source

G = nx.MultiDiGraph()
G.add_edge(1, 2, label="a.")
G.add_edge(1,3, label="b.")
G.add_edge(2,1, label="c.")
G.add_edge(2,3, label="d.")
# pos = nx.spring_layout(G)
# nx.draw(G, pos, with_labels=True)
# nx.draw_networkx_edge_labels(G,pos,edge_labels=nx.get_edge_attributes(G,'label'))
# plt.show()
nx.drawing.nx_pydot.write_dot(G, 'multi.dot')

dot = open("multi.dot")
s = Source.from_file("./multi.dot")
print(s.view())

