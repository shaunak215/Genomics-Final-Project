from graphviz import Source
import sys

if len(sys.argv) != 2:
    print("Please provide only the dot file as a command line argument")
else:
    file_name = sys.argv[1]
    s = Source.from_file(file_name)
    print(s.view())
