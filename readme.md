# Wheeler Graph Toolkit

Final Project for Computational Genomics: Sequences (EN.601.647) at JHU by 
* Eduardo Aguila (eaguila6)
* Shaunak Shah (shaunak215)
* Kuan-Hao Chao (Kuanhao-Chao)
* Beril Erdogdu (berilerdogdu) 

Our suite of tools for Wheeler Graphs contains functionality for the following features: visualization of graphs in .DOT format, checker for WGs given node and edge labels, random generation of WGs, recognizer for WGs given only edge labels, and pattern detection within a WG. 

## Configuration 
In order to run the following, be sure to have installed/ updated the following:
* `pip3 install networkx`
* `pip3 install graphviz `


# Repository Structure
The various features of this toolkit are packaged into the following folders: 

## Visualizer

Within the visualizer folder, any dot file can be visualized by providing the file path as a command line argument to `visualize.py`. For example, to visualize a sample that was created by the generator

```python
python3 visualize.py ../generator/samples/test_0.dot 
```

## Checker

Within the checker folder, any dot file can be passed as the command line argument, and the checker will verify if the graph meets the conditions to be a WG. If it is not a WG, it will output the properties that were violated. Note the current functionality supports only graphs that contain only integer node labels. 

Example 1: A valid WG would produce the following output: 
```
>>> python3 checker.py ../samples/valid.dot
Inputed graph is a Wheeler Graph
```
Example 2: A WG that violates all three conditions would produce the following output:
```
>>> python3 checker.py ../samples/invalid.dot
Inputted graph is not a Wheeler Graph - the following condition(s) not met:
   * 0-indegree nodes come before others
   * a ≺ a′⟹  v < v′
   * (a = a′) ∧ (u < u′) ⟹  v ≤ v′
```

## Generator

Within the generator folder, WG samples can be generated by providing the number of samples desired as the first argument, and the approximate node count for the graph as the second argument. 

Note that the samples will be generated into a `samples` directory, so you must create this folder within the generator directory.

Example 1: `python3 generate_WG_samples.py 10 15 ` will generate 10 samples of graphs with approximately 15 nodes within the `/samples` directory. 

Example 2: `python3 generate_WG_samples.py 20 50 ` will generate 20 samples of graphs with approximately 50 nodes within the `/samples` directory. 

Note that there are various generator files within this directory. The vast majority of these were used for internal testing. For example, running `python3 generate_WG_RandomNodes.py 10 10` will generate 10 samples of graphs with approximately 10 nodes, where the overall structure of the graph is valid, but the nodes are in shuffled/random order. The purpose of this is to further test our recognizer. Other generators that were used for testing include: 

`generator_testing.py` and `generator_test_version.py` which are analagous to `generate_WG_samples.py` and `generator.py` respectively. Note that in order to run these you will need to create a `testing` directory for the samples to be stored in. `generator_testing.py` takes no command line arguments, and can be run with:
```python
python3 generator_testing.py
```
It was used to validate random samples through our checker, perform some timing analysis, and to determine a formula for node count generation.


## Recognizer

WG recognizing problem is hard. It is proved NP-complete by Gibney and Thankachan in 2019, and the time complexity of the pseudocode algorithm is <img src="https://render.githubusercontent.com/render/math?math=2^{e \cdot log\sigma  %2B O(n  %2B e)}">.
We implemented a faster recognizer in C++, and it is a factorial algorithm doing minimum permutations. Given a directed graph G with edge labels and random node labels in DOT format, the recognizer answers whether G is a wheeler graph or not and outputs the WG data structure proposed by Gagie (2017). 


### 1. Building the latest version from `src/`

```
cd ./recognizer/src/

make
```

### 2. Running recognizer


```
Usage:

   recognizer  <in.dot>  [wg_recognizer_method]  [stop_condition]  [print_invalid]
```

```
Options:

   wg_recognizer_method : the recognizer algorithm. 'm1' is the exponential algorithm; 
                          'm2' is the one scan through algorithm (still under development)
                          'm1' or 'm2'. The default is 'm1'.
  
   stop_condition       : whether to find one set of node labels and stop or all sets of correct node labels.
                          'early_stop' or 'normal'. The default is 'early_stop'.
                         
   print_invalid        : whether to print out the invalid wheeler graph log during node labels permutation. 
                          '0' or '1'. The default is '0'.
```

### 3. Inputs and outputs:
The recognizer takes any DOT file as the input and test whether at least one set of correct node labels can be generated. In this WG suite of tools, it takes the DOT file generated by generator. If it is not a WG, program halts and nothing is outputted; if it is a wheeler, then five files are generated. Following are the description:

1. `I.txt`:  the I bitarray (indegree) of Gagie's WG data structure.
2. `O.txt`:  the O bitarray (outdegree) of Gagie's WG data structure.
3. `L.txt`:  the L array of Gagie's WG data structure.. It’s the concatenation of corresponding edges labels of nodes in O bit array.
4. `node.dot`: the mapping from old node labels to new node labels.  
5. `graph.dot`: the new, correct, and sorted dot file with new node labels. 


### 4. Reproducible example:

Take `../graph/generator_DOT/node_num_5/after_shuffle/test_1.dot` DOT file as an example. It is a random valid WG outputted by the generator, and recognizer takes it as the input.

```
DOT file path:  ./recognizer/graph/generator_DOT/node_num_5/after_shuffle/test_1.dot

   strict digraph  {
   S1;
   S0;
   S5;
   S3;
   S6;
   S2;
   S4;
   S5 -> S0  [label=a];
   S5 -> S6  [label=a];
   S5 -> S4  [label=b];
   S3 -> S4  [label=b];
   S4 -> S6  [label=a];
   }
 ```
  
Run the following command:

```
cd ./recognizer/src/

./recognizer  ../graph/generator_DOT/node_num_5/after_shuffle/test_1.dot m1 early_stop 1
```

You will get the following five output files:

1. ***I.txt***:
   ```
    1101001001
   ```
2. ***O.txt***:
   ```
    0100011101
   ```
3. ***L.txt***:
   ```
    baaba
   ```
4. ***node.txt***:
   ```
    S3	1
    S5	2
    S0	3
    S6	4
    S4	5
   ```
5. ***graph.dot***:
   ```
    strict digraph  {
      2 -> 3 [label=a];
      2 -> 4 [label=a];
      5 -> 4 [label=a];
      1 -> 5 [label=b];
      2 -> 5 [label=b];
    }
   ```

## Pattern Detection

Upon receiving a directed edge labeled graph that can be a proper Wheeler Graph, the Wheeler Graph recognizer described above outputs updated O, I and L vectors with appropriate node labels. The Wheeler Graph Pattern Matcher takes these three vectors as input and queries the graph to find occurrences of any given pattern p. For any found occurrence of p, the program writes out the character and rank of the first character of p in the WG.

The Wheeler Graph Pattern Matcher we implemented takes as an optional argument the original graph structure -in .dot format- outputted by the Wheeler Graph Recognizer. If this option is taken and the inputted pattern p is found in the Wheeler graph, the pattern matcher will output the same Wheeler Graph with all the occurrences of p in the graph being highlighted.

### How to run Pattern Matcher
```
cd ./pattern_matcher
python pattern_matcher.py O.txt I.txt L.txt p.txt path_to_output_file WG.dot(optional) path_to_output_graph.dot(optional)
```

### Required Input Format

1. ***O.txt***:
   ```
    01010010101011010101
   ```
2. ***I.txt***:
   ```
    10010101010101010101
   ```
3. ***L.txt***:
   ```
    ttcggaaata
   ```
    These vector files are in the same format as the Wheeler Recognizer output.
4. ***p.txt***:
   ```
    aga
    ```
5. ***WG.dot***  ***IMPORTANT ***:
   Please make sure that your node labels start with '1' and not '0'. This is the format the Recognizer indexes its node labels and the pattern matcher is implemented to parse them accordingly. If your node labels start with '0', the graph will not be parsed correctly.

   ```
    strict digraph  {
	1 -> 8 [label=t];
	8 -> 3 [label=a];
	3 -> 5 [label=c];
	3 -> 6 [label=g];
	5 -> 2 [label=a];
	6 -> 2 [label=a];
	2 -> 9 [label=t];
	9 -> 10 [label=t];
	10 -> 4 [label=a];
	4 -> 7 [label=g];
}
    ```







### Reproducible example

Again in the ./pattern_matcher directory, run the following:

```
python pattern_matcher.py O.txt I.txt L.txt p.txt results.txt ex_wg.dot updated_wg.dot
```

This example contains the example Wheeler Graph found in the paper by Gibney and Thankachan. Feel free to input any pattern p and visualize the path taken by the Pattern Matcher.

The input files already provided in the directory will try to match p = 'cbbc' on the input graph and output the following path:

![alt text](https://github.com/shaunak215/Genomics-Final-Project/blob/17f167ecf063c637e48e83b104f47574871571a6/pattern_matcher/example_path.png)


The directory "wg_pattern_matcher_examples/recognizer_output" contains 50+ other example Wheeler Graph outputted by the recognizer that we tested our pattern matcher with. Feel free to experiment!

## Group member contribution
|            | Eduardo Aguila and Shaunak Shah | Kuan-Hao Chao | Beril Erdogdu |
------------ | -------------------------- | ------------- |-------------- |
Coding       | Visualizer, Checker, Recognizer | recognizer | Pattern matcher |
Deliverables | Visualizer, Checker, Recognizer | recognizer | Pattern matcher |
