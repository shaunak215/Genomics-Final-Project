import networkx as nx
from checker import checker

con1, con2, con3 = checker('test_graphs/graph1.dot')
if con1 and con2 and con3: 
    print("Test Case 1 passed")
else:
    print("Test Case 1 failed")

con1, con2, con3 = checker('test_graphs/graph2.dot')
if con1 and con2 and con3: 
    print("Test Case 2 passed")
else:
    print("Test Case 2 failed")
