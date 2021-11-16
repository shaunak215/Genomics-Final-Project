import networkx as nx

#TEST CASE 1
#Graph with only one node is vacuosly a Wheeler Graph
G = nx.MultiDiGraph()
G.add_node(0)

nx.drawing.nx_pydot.write_dot(G, 'test_graphs/graph1.dot')