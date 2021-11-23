from generator import generateWG


for i in range(10):
    filename = "temp/test_"  + str(i) + ".dot"
    c1, c2, c3, alph_size = generateWG(50,.1, False, filename)
    if not c1 or not c2 or not c2:
        print("FAILURE CASE " + str(i) +": "+ str(c1) + " " + str(c2) + " " + str(c3))
    else:
        print("Pass")
    # print(alph_size)
    # print('\n')