from generator import generateWG


for i in range(10):
    c1, c2, c3, alph_size = generateWG(10,.3, False)
    print(alph_size)