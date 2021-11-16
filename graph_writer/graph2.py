import networkx as nx

#TEST CASE 2
#Graph with two disconnected nodes is not a Wheeler Graph
G = nx.MultiDiGraph()
G.add_node(0)
G.add_node(1)

nx.drawing.nx_pydot.write_dot(G, 'test_graphs/graph2.dot')