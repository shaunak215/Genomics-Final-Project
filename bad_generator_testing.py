from bad_generator import generateBadWG
import os
import sys

# dir = 'temp'
# for f in os.listdir(dir):
#     os.remove(os.path.join(dir, f))

# dir = 'testing'
# for f in os.listdir(dir):
#     os.remove(os.path.join(dir, f))

# y = 0.0243x^2 + 0.2231x + 7.3507
# def calc_node_num(num):
#     return (0.0243 * (num ** 2)) + (.2231 * num) + 7.3507

#uncomment out the code below for our final implementation
"""
if (len(sys.argv) != 3):
  print("Not enough arguments: provide input and output file names")
else: 
    num_graphs = int(sys.argv[1])
    node_count = int(sys.argv[2])

    for i in range(10):
        filename = "temp/test_"  + str(i) + ".dot"
        num_nodes = int(calc_node_num(node_count))
        c1, c2, c3, l, n = generateBadWG(num_nodes,.2, False, filename)
"""

for i in range(10):
    filename = "bad_samples/test_"  + str(i) + ".dot"
    c1, c2, c3 = generateBadWG(10,.2, False, filename)

    if not c1 or not c2 or not c2:
        print("FAILURE CASE " + str(i) +": "+ str(c1) + " " + str(c2) + " " + str(c3))
        # print(l)
    else:
        print("Pass " + str(i))