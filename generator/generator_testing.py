from generator import generateWG
import os
import sys

import time

start = time.time()


dir = 'samples'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = 'testing'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

# y = 0.0243x^2 + 0.2231x + 7.3507
def calc_node_num(num):
    return (0.0243 * (num ** 2)) + (.2231 * num) + 7.3507


#uncomment out the code below for our final implementation
"""
if (len(sys.argv) != 3):
  print("Not enough arguments: provide input and output file names")
else: 
    num_graphs = int(sys.argv[1])
    node_count = int(sys.argv[2])

    for i in range(10):
        filename = "samples/test_"  + str(i) + ".dot"
        num_nodes = int(calc_node_num(node_count))
        c1, c2, c3, l, n = generateWG(num_nodes,.2, False, filename)
"""


for i in range(1000):
    filename = "samples/test_"  + str(i) + ".dot"
    c1, c2, c3, l, n = generateWG(30,.2, False, filename)

    if not c1 or not c2 or not c3:
        print("FAILURE CASE " + str(i) +": "+ str(c1) + " " + str(c2) + " " + str(c3))
        print(l)
    # else:
    #     print("Pass " + str(i))

end = time.time()
print(end - start)

# c1, c2, c3, l, n = generateWG(30,.2, False, filename) -> 1000 samples
# 452.26770997047424 seconds


#11 nodes, .2, seed=26
# [{(3, 1), (6, 1), (4, 1), (0, 1)}, 
# {(7, 3), (10, 3), (4, 2), (4, 3)}, 
# {(7, 4), (10, 5), (10, 4), (7, 6), (1, 6)}, 
# {(3, 8), (10, 8), (5, 8), (10, 7), (6, 7), (9, 8), (0, 8), (7, 8)}, 
# set(), 
# {(2, 9), (8, 9), (5, 9), (0, 8), (6, 9), (1, 9)}, 
# {(8, 10), (9, 10)}]
