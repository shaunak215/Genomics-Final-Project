from generator import generateWG
import os

dir = 'temp'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

for i in range(1):
    filename = "temp/test_"  + str(i) + ".dot"
    c1, c2, c3 = generateWG(50,.2, False, filename)
    if not c1 or not c2 or not c2:
        print("FAILURE CASE " + str(i) +": "+ str(c1) + " " + str(c2) + " " + str(c3))
    else:
        print("Pass")