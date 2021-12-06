from generator_test_version import generateWG_Testing
import os
import sys
import pandas as pd
import time

# y = 0.0252x^2 + 0.226x + 6.2819
def calc_node_num(num):
    return (0.0252 * (num ** 2)) + (.226 * num) + 6.2819

df = pd.DataFrame() #for storing node counts
w = open("timing_data.txt", 'w')

node_test_count = 5
for i in range(20): #will run for nodes 5 to 100
    node_list = []
    start = time.time()
    #remove any old testing samples
    dir = 'testing'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    for i in range(10): #number of graphs to generate for each node count
        filename = "/test_"  + str(i) + ".dot"
        c1, c2, c3, l, n = generateWG_Testing(node_test_count,.2, False, filename, False)
        node_list.append(n)
        #if any conditions were not met, output which ones and print the edge partition list
        if not c1 or not c2 or not c3:
            print("FAILURE CASE " + str(i) +": "+ str(c1) + " " + str(c2) + " " + str(c3))
            print(l)

    print("Done with " + str(node_test_count) + " nodes")
    df[str(node_test_count)] = node_list
    end = time.time()
    w.write("Time for 1000 samples of " + str(node_test_count) + ": " str(end-start) + " seconds\n")
    node_test_count = node_test_count + 5

df.to_csv("testing2.csv")
avg_col = df.mean(axis=0)
f = open("averages.txt", "w")
f.write(str(avg_col))
f.close()

w.close()
