import sys
from collections import defaultdict



# Using the F array we will construct a "skip dictionary"
# which given an input character outputs the range of positions
# in F where the character occurs.
def construct_skip_dict(F):
    ind = 0
    C = defaultdict(list)
    while(1):
        curr_c = F[ind]
        start = ind
        while(1):
            if(ind == len(F) - 1):
                C[curr_c] = [start, ind]
                return C
            if(curr_c != F[ind+1]):
                C[curr_c] = [start, ind]
                ind += 1
                break
            
            curr_c = F[ind]
            ind += 1
        
    return C


# Starting with rank_1, which will take an input bit vector and an integer 'i';
# and return the number of 1s UP TO BUT NOT INCLUDING offest i.
# Note that following this logic, the rank of the 3rd 1 in a bit array would equal to 2,
# the rank of the 4th 1 would equal to 3, etc.
# The rank_1 of any 0 in the bit vector would similarly equal to the number of 1s preceding its index.

def rank_1(i, bit_vector):
    rank_1 = 0
    for ind in range(0, i):
        if(bit_vector[ind] == 1):
            rank_1 += 1
    return rank_1




# Similarly, rank_0 will take an input bit vector and an integer 'i';
# and return the number of 0s UP TO BUT NOT INCLUDING offest i.
# Note that following this logic, the rank of the 3rd 0 in a bit array would equal to 2,
# the rank of the 4th 0 would equal to 3, etc.
# The rank_0 of any 1 in the bit vector would similarly equal to the number of 0s preceding its index.

def rank_0(i, bit_vector):
    rank_0 = 0
    for ind in range(0, i):
        if(bit_vector[ind] == 0):
            rank_0 += 1
    return rank_0
    
    
    
# Now using the rank queries we have implemented above we will define the select queries.
# Starting with select_1 query, which will take an input bit vector and an integer 'i';
# and return the maximum offset j in the bit vector such that the rank_1 at j is equal to i.
# In other words, select_1(i) will return the offset of the 'ith' 1 bit in the bit vector.


def select_1(i, bit_vector):
    j = 0
    while(j < len(bit_vector)):
        if(rank_1(j, bit_vector) > i):
            return j-1
        j += 1
    return j-1



# Similarly, select_0 query will take an input bit vector and an integer 'i';
# and return the maximum offset j in the bit vector such that the rank_0 at j is equal to i.
# In other words, select_0(i) will return the offset of the 'ith' 0 bit in the bit vector.


def select_0(i, bit_vector):
    j = 0
    while(j < len(bit_vector)):
        if(rank_0(j, bit_vector) > i):
            return j-1
        j += 1
    return j-1


# Finally, we implement rank_c query which will take an input character array
# (we will eventuallyinput the L vector) and an integer 'i'
# and return the rank of the character that is in offset i in that character array.


def rank_c(i, char_arr):
    char = char_arr[i]
    ind = 0
    rank = 0
    
    while(ind < i):
        if char_arr[ind] == char:
            rank +=1
        ind += 1
    return rank
    
    
# Following the logic outlined in the report, this function is a SINGLE ITERATION
# of the pattern matching algorithm and matches one character at a time:

def match_character(next_c_in_p, search_range_start, search_range_end, O, I, L, C):
    outgoing_range = []
    visited_nodes = []
    # INSIDE THE I BIT VECTOR:
    incoming_start_edge_in_I = select_0(search_range_start, I)
    incoming_end_edge_in_I = select_0(search_range_end, I)
    receiving_start_node_in_I = rank_1(incoming_start_edge_in_I, I)
    receiving_end_node_in_I = rank_1(incoming_end_edge_in_I, I)
     # INSIDE THE O BIT VECTOR:
    corresponding_start_node_in_O = select_1(receiving_start_node_in_I, O)
    corresponding_end_node_in_O = select_1(receiving_end_node_in_I, O)
    visited_nodes.append([rank_1(corresponding_start_node_in_O, O)+1, rank_1(corresponding_end_node_in_O, O)+1])
    
    outgoing_range = [rank_0(select_1(rank_1(corresponding_start_node_in_O, O)-1, O), O), rank_0(corresponding_end_node_in_O, O)-1]
        
    if(len(outgoing_range) == 0):
        return -1

    else:
        matching_chars = []
        for n in range(outgoing_range[0], outgoing_range[1]+1):
            if(L[n] == next_c_in_p):
                matching_chars.append(n)
                
        if(len(matching_chars) > 0):
            search_range_start = C[L[min(matching_chars)]][0] + rank_c(min(matching_chars), L)
            search_range_end = C[L[max(matching_chars)]][0] + rank_c(max(matching_chars), L)

            return search_range_start, search_range_end, visited_nodes
        
        return -1
       


def match_pattern(p, O, I, L, C, F):
    
    all_visited_nodes = []
    for el in p:
        if(el not in C):
            print("THE PATTERN WAS NOT FOUND IN THE INPUT WHEELER GRAPH")
            return -1
    curr_ind = len(p)-1
    curr_c = p[curr_ind]
    search_range_start = C[curr_c][0]
    search_range_end = C[curr_c][1]
    while(1):
        if(curr_ind == 0):
            for s in  range(search_range_start, search_range_end+1):
                print("MATCH FOUND:")
                print("CHARACTER", F[s], "of RANK ", rank_c(s, F))
            return all_visited_nodes, p[-1], F[s]
        
        curr_c = p[curr_ind]
        
        c_match = match_character(p[curr_ind - 1], search_range_start, search_range_end, O, I, L, C)
        if(c_match != -1):
            search_range_start, search_range_end, visited_nodes = c_match
            all_visited_nodes.append(visited_nodes[0])
        else:
            print("THE PATTERN WAS NOT FOUND IN THE INPUT WHEELER GRAPH")
            return -1
        curr_ind -= 1


def find_match_edges_in_graph(path_to_graph, all_visited_nodes, first_c, last_c):
    ex_g = open(path_to_graph, 'r')
    ex_g_edges = [i.strip('\n | ; | \t') for i in ex_g.readlines()[1:-1]]
    path = defaultdict(list)
    node_edge_arr = []
    for i in range(len(ex_g_edges)):
        source_node = int(ex_g_edges[i].split(' ')[0])
        receiving_node = int(ex_g_edges[i].split(' ')[2])
        edge = ex_g_edges[i].split(' ')[3].replace('[label=', '').strip("]'")
        node_edge_arr.append([source_node, receiving_node, edge])
    
    
    # POPULATE PATH:
    for j in node_edge_arr:
        if(j[2] == first_c):
            path[0].append(j)
 
    ind = 0
    while(1):
        if(ind == len(all_visited_nodes)):
            break
        for n_e in node_edge_arr:
            if(n_e[1] in range(all_visited_nodes[ind][0], all_visited_nodes[ind][1]+1)):
                path[ind].append(n_e)
        ind += 1
    
    for l in node_edge_arr:
        prev = []
        for p in path[ind-1]:
            prev.append(p[1])
        if(l[2] == last_c and l[0] in prev):
            path[ind].append(l)
    
    # CLEAN PATH:
    ind = len(path)-1
    clean_path = defaultdict(list)
    clean_path[ind] = path[ind]
    for ind in range(ind-1, -1, -1):
        receiving = set()
        for el_n in clean_path[ind + 1]:
            receiving.add(el_n[0])
        for el_p in path[ind]:

            if(el_p[1] in receiving):
                clean_path[ind].append(el_p)
                
    clean_path_2 = defaultdict(list)
    clean_path_2[0] = clean_path[0]
    for ind_2 in range(1, len(clean_path)):
        leaving = set()
        for el_p in clean_path_2[ind_2-1]:
            leaving.add(el_p[1])
        for el_n in clean_path[ind_2]:
            if(el_n[0] in leaving):
                clean_path_2[ind_2].append(el_n)

    
    edges_to_highlight = []
    for i in list(clean_path_2.values()):
        for j in i:
            edges_to_highlight.append(j)
    
    return node_edge_arr, edges_to_highlight
    


def write_highlighted_graph(node_edge_arr, edges_to_highlight, output_file):
    with open(output_file, 'w', encoding = 'utf-8') as o:
        o.write("strict digraph  {")
        
        for i in node_edge_arr:
            if i in edges_to_highlight:
                line = '\t' + str(i[0]) + ' -> ' + str(i[1]) + ' [label =' + i[2] + '][penwidth = 2.5][color = purple];' + '\n'
                o.write(line)
                
            else:
                line = '\t' + str(i[0]) + ' -> ' + str(i[1]) + ' [label =' + i[2] + '];' + '\n'
                o.write(line)
        o.write('}')
        o.close()
    return





def main(argv):

    program_name = sys.argv[0]
    arguments = sys.argv[1:]
    
    
    if len (sys.argv) < 4 :
        print ("Usage: python pattern_matcher.py O.txt I.txt L.txt p WG.dot(optional) output_graph.dot(optional)")
        sys.exit (1)
    
    
    O_f = open(arguments[0], "r")
    O = list(map(int, list(O_f.read())))


    I_f = open(arguments[1], "r")
    I = list(map(int, list(I_f.read())))

    L_f = open(arguments[2], "r")
    L = list(L_f.read())
    
    p = open(arguments[3], "r").read().strip()
        
    # For keeping track of the iterations and checking our logic,
    # we will reconstruct the "F" array which can be thought of as the
    # corresponding first-column in a BWT matrix if the BWT-transform was the L vector plus the $.

    F = sorted(L)

    C = construct_skip_dict(F)
    
    pattern_match = match_pattern(p, O, I, L, C, F)
    
    if(pattern_match == -1):
        return -1
    
    all_visited_nodes, starting_edge, ending_edge = match_pattern(p, O, I, L, C, F)
    
    
    if(len (sys.argv) > 4):
    
        input_wg = arguments[4]
        output_wg = arguments[5]
        
        node_edge_arr, edges_to_highlight = find_match_edges_in_graph(input_wg, all_visited_nodes, starting_edge, ending_edge)
        write_highlighted_graph(node_edge_arr, edges_to_highlight, output_wg)
    
    
    return
    

if __name__ == "__main__":
   main(sys.argv[1:])

