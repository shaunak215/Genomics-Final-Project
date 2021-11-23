from generator import generateWG


for i in range(10):
    filename = "temp/test_"  + str(i) + ".dot"
    c1, c2, c3, alph_size = generateWG(10,.2, False, filename)
    print(alph_size)