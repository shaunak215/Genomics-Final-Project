from generator import generateWG
import os
import sys

dir = 'temp'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

dir = 'testing'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

# y = 0.0243x^2 + 0.2231x + 7.3507
def calc_node_num(num):
    return (0.0243 * (num ** 2)) + (.2231 * num) + 7.3507



if (len(sys.argv) != 3):
  print("Not enough arguments: provide input and output file names")
else: 
    num_graphs = int(sys.argv[1])
    node_count = int(sys.argv[2])

    for i in range(10):
        filename = "temp/test_"  + str(i) + ".dot"
        num_nodes = int(calc_node_num(node_count))
        c1, c2, c3, l, n = generateWG(num_nodes,.2, False, filename)
        print(n)

# f = open("test_results.txt", 'w')
# num_nodes = 10
# for i in range(9):
#     # test_results = "testing/test_" + str(num_nodes) + "_nodes.txt"
    
#     for j in range(100):
#         filename = "temp/test_"  + str(i) + ".dot"
#         c1, c2, c3, l, n = generateWG(num_nodes,.2, False, filename)
#         f.write(str(n) + '\n')
#         # print(n)
#     f.write("Done with " + str(num_nodes) + " nodes\n")
#     num_nodes = num_nodes + 10

# f.flush()
# f.close()

    
    # if not c1 or not c2 or not c2:
        # print("FAILURE CASE " + str(i) +": "+ str(c1) + " " + str(c2) + " " + str(c3))
        # print(l)
    # else:
    #     print("\n")


    #EXAMPLE OF TEST CASE THAT FAILS
    # [{(1, 2), (8, 1), (9, 2), (7, 2), (13, 2), (14, 2), (5, 2)}, 
    # {(13, 3), (6, 3), (12, 3), (10, 3)}, 
    # {(7, 4), (2, 4), (14, 4), (6, 4), (9, 4)}, 
    # set(), 
    # {(8, 7), (4, 5), (7, 6), (10, 6)}, 
    # {(10, 8), (4, 9), (0, 9), (11, 9), (12, 9), (8, 9), (14, 9), (10, 9), (5, 9), (11, 8), (6, 9), (1, 9)}, 
    # set(), 
    # {(10, 9), (11, 9), (14, 9), (12, 9)}, 
    # {(9, 10), (12, 11), (0, 10), (1, 11), (1, 10), (4, 11), (14, 11)}, 
    # {(11, 12), (2, 12)}, {(9, 13), (0, 13), (14, 13), (3, 13)}, 
    # {(13, 14), (8, 14), (5, 14), (11, 14)}]