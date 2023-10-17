from __future__ import annotations
from time import time
from math import factorial
from enum import Enum, auto

###########
# CLASSES #
###########

class Node:
    def __init__(self, id: int):
        """Initializes an instance of Node

        Args:
            id (int): id number to keep track of which Nodes are which inside a Graph
        """        
        self.id = id
        self.value = 0
        self.connections = set()

    def __str__(self) -> str:
        """Returns a string to describe this Node

        Returns:
            str: String presentable on screen
        """
        return f'Value = {self.value}, Connections = {self.connections}'
    
    def set_value(self, value: int):
        """Assigns a value to the Node

        Args:
            value (int): the Value to assign.
        """
        self.value = value
    
    def copy(self) -> Node:
        """Produces an identical deep copy of this Node.

        Returns:
            Node: the new node
        """        
        new_node = Node(self.id)
        new_node.value = self.value
        new_node.connections = self.connections.copy()
        return new_node

class Graph:
    def __init__(self, adjacency_matrix: list[list[int]], initialize: bool = True) -> None:
        """Initializes the Graph instance.

        Args:
            adjacency_matrix (list[list[int]]): the adjacency matrix to be associated with this graph
                0's represent no shared edge, 1's represent a shared edge 
            initialize (bool, optional): Whether you want the graph to create the nodes or not. Defaults to True. You should always leave this as true!
        """        
        self.adjacency_matrix = adjacency_matrix
        self.reach = set()
        self.nodes = []
        self.delta = -1
        if initialize:
            self.nodes = [Node(_) for _ in range(len(adjacency_matrix))]
            for row in range(len(adjacency_matrix)):
                for column in range(len(adjacency_matrix[row])):
                    if adjacency_matrix[row][column]: self.nodes[row].connections.add(column)
        return
    
    def __str__(self) -> str:
        """Stringifies this Graph.

        Returns:
            str: string representation of the graph
        """        
        s = 'Graph\n-----\n'
        for node in self.nodes:
            s += f'{node}\n'
        return s
    
    def set_node_value(self, index: int, value: int) -> None:
        """Assign a particular value to a specific node within the Graph

        Args:
            index (int): index of the node to change the value, must be in the range of nodes list
            value (int): value to assign to the node
        """        
        self.nodes[index].set_value(value)
        self.reach = self.reach.union(self.nodes[index].connections)
        self.reach.discard(index)
        return
    
    def clear(self) -> None:
        """Completely wipes the Graph while retaining the Node structure
        """        
        for node in self.nodes:
            node.value = 0
        self.reach.clear()
        return
    
    def copy(self) -> Graph:
        """Produces a deep copy of this Graph

        Returns:
            Graph: the new copy
        """        
        new_graph = Graph(self.adjacency_matrix, False)
        for node in self.nodes:
            new_graph.nodes.append(node.copy())
        new_graph.delta = self.delta
        return new_graph
    
    def get_smallest_degree(self) -> int:
        """Returns the smallest degree that a vertex has in the graph

        Returns:
            int: smallest degree
        """             
        if self.delta == -1:
            self.delta = min([len(node.connections) for node in self.nodes])
        return self.delta
    
    def get_pinnacles(self, labeling: list) -> list:
        """Given a specific labeling for this graph, determine which values are pinnacles

        Args:
            labeling (list): list of the labels for the graph, must be the same size as the number of vertices/nodes

        Returns:
            set: list of pinnacles for this labeling in descending order
        """        
        pinnacles = []
        for i in range(len(self.nodes)):
            self.set_node_value(i, labeling[i])
        for node in self.nodes:
            if all([node.value > self.nodes[i].value for i in node.connections]):
                pinnacles.append(node.value)
        return sorted(pinnacles, reverse=True)

#########
# ENUMS #
#########

class GraphType(Enum):
    STAR = auto()
    COMPLETE = auto()
    CYCLE = auto()
    WHEEL = auto()
    BIPARTITE = auto()
    CUSTOM = auto()

##################
# GRAPH CREATION #
##################

def get_digits(s: str) -> int:
    """Takes a string and returns an integer for the digits in string."""
    i = ''
    for d in [char for char in s if char.isdigit()]:
        i += d
    return int(i)

def create_graph(node_amount: int, style: str = 'star-1') -> Graph:
    """Creates a Graph based on a number of nodes/vertices and a style code.

    Args:
        node_amount (int): Total number of nodes/vertices in Graph
        style (str, optional): Style of Graph to create. See below. Defaults to 'star-1'.

    Styles:
        " star-'amount of stars' ": Style format for creating a Star graph.\n
        " bipartite-'amount of vertices on one side' ": Style format for creating a Complete Bipartite Graph.\n
        " wheel ": Style format for creating a Wheel Graph\n
        " cycle ": Style format for creating a Cycle Graph\n
        " complete ": Style format for creating a Complete Graph

    Raises:
        NotImplementedError: Raised when a requested style has not been implemented.

    Returns:
        Graph: _description_
    """    
    if style[0:4] == 'star':
        return _star(node_amount=node_amount, star_amount=get_digits(style))
    elif style[0:9] == 'bipartite':
        return _bipartite(node_amount=node_amount, left_amount=get_digits(style))
    elif style[0:5] == 'wheel':
        return _wheel(node_amount=node_amount)
    elif style[0:5] == 'cycle':
        return _cycle(node_amount=node_amount)
    elif style[0:8] == 'complete':
        return _complete(node_amount=node_amount)
    elif style[0:4] == 'line':
        return _line(node_amount=node_amount)
    else:
        raise NotImplementedError(f'style=\'{style}\' does not correspond to an implemented style.')

def create_graph_custom(adjacency_matrix: list) -> Graph:
    """Produces a Graph based entirely on a supplied adjacency matrix.

    Args:
        adjacency_matrix (list): adjacency matrix to build the graph from

    Returns:
        Graph: created Graph
    """    
    return Graph(adjacency_matrix)

def _star(node_amount: int, star_amount: int) -> Graph:
    """Builds the Adjacency Matrix for the desired star graph and creates the graph from it.

    Args:
        node_amount (int): the total number of nodes/vertices in the graph
        star_amount (int): the desired number of central stars in the graph

    Returns:
        Graph: created Star Graph
    """    
    adjacency_matrix = []
    for i in range(node_amount):
        if i < star_amount:
            node = [1]*node_amount
            node[i] = 0
        else: node = [1]*star_amount + [0]*(node_amount-star_amount)
        adjacency_matrix.append(node)
    return Graph(adjacency_matrix) 

def _bipartite(node_amount: int, left_amount: int) -> Graph:
    """Creates a specificed complete bipartite graph.

    Args:
        node_amount (int): total number of nodes/vertices
        left_amount (int): number of vertices on the left side of graph

    Returns:
        Graph: create complete bipartite Graph
    """    
    adjacency_matrix = []
    for i in range(left_amount):
        adjacency_matrix.append([0]*left_amount + [1]*(node_amount-left_amount))   
    for i in range(node_amount-left_amount):
        adjacency_matrix.append([1]*left_amount + [0]*(node_amount-left_amount))
    return Graph(adjacency_matrix)

def _wheel(node_amount: int) -> Graph:
    """Creates a Wheel Graph.

    Args:
        node_amount (int): The total number of nodes/vertices in the Graph

    Returns:
        Graph: created Wheel Graph
    """
    adjacency_matrix = []
    for i in range(node_amount-1):
        node = [0]*node_amount
        node[(i-1)%(node_amount-1)] = 1
        node[(i+1)%(node_amount-1)] = 1
        node[-1] = 1
        adjacency_matrix.append(node)
    adjacency_matrix.append([1]*(node_amount-1) + [0])
    return Graph(adjacency_matrix)

def _cycle(node_amount: int) -> Graph:
    """Creates a Cycle Graph

    Args:
        node_amount (int): Total number of nodes/vertices in the Graph

    Returns:
        Graph: created Cycle Graph
    """    
    adjacency_matrix = []
    for i in range(node_amount):
        n = [0]*node_amount
        n[(i-1)%node_amount] = 1
        n[(i+1)%node_amount] = 1
        adjacency_matrix.append(n)
    return Graph(adjacency_matrix)

def _complete(node_amount: int) -> Graph:
    """Creates a Complete Graph

    Args:
        node_amount (int): Total number of nodes/vertices in the Graph

    Returns:
        Graph: created Complete Graph
    """    
    adjacency_matrix = []
    for i in range(node_amount):
        n = [1]*node_amount
        n[i] = 0
        adjacency_matrix.append(n)
    return Graph(adjacency_matrix)

def _line(node_amount: int) -> Graph:
    adjacency_matrix = []
    for i in range(node_amount):
        n = [0]*node_amount
        if i > 0: n[i-1] = 1
        if i < node_amount-1: n[i+1] = 1
        adjacency_matrix.append(n)
    return Graph(adjacency_matrix)
################
# PERMUTATIONS #
################

def generate_permutations(size: int) -> list:
    """Generates a list of all permutations of desired size.

    Args:
        size (int): Number of elements to permute.

    Returns:
        list: List containing all permutations.

    Example:
        generate_permutations(3) ->
        [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,2,1], [3,1,2]]
    """    
    S = []
    _generate_permutations(S, [i+1 for i in range(size)], size)
    return S

def _generate_permutations(S: list, a: list, size: int):
    """Generate the permutations of list a onto external list S. Use with Caution.

    Args:
        S (list): List to store all permutations of list a.
        a (list): List to permute.
        size (int): Number of elements in list a. Do not touch!
    """    
    if (size == 1):
        S.append(a.copy())
        return
    for i in range(size):
        _generate_permutations(S, a, size-1)
        if (size & 1):
            a[0], a[size-1] = a[size-1], a[0]
        else: a[i], a[size-1] = a[size-1], a[i]   

########################
# THE BREAD AND BUTTER #
########################

def distinct_pinnacle_placement(G: Graph, n: int, timeit: bool = False) -> list:
    """Retrieves a List of all Possible placements of n distinct pinnacles such that
    no two are adjacent on the Graph G. You should not have to ever call this function!

    Args:
        G (Graph): Graph we are labeling.
        n (int): Number of vertices that must not be touching.
        timeit (bool, optional): If you want to print out the runtime. Defaults to False.

    Raises:
        ValueError: Raised when number of vertices is less than 1

    Returns:
        list: list of all possible pinnacle placemenets in form [{set of pinnacle nodes indeces}, {reach of said pinnacles}]
    """    
    if timeit: t = time()
    if n < 1: raise ValueError(f'n={n} must be larger than or equal to 1')
    if n == 1:
        return [[{i}, G.nodes[i].connections] for i in range(len(G.nodes))]
    L = distinct_pinnacle_placement(G, n-1)
    p = []
    for l in L:
        for v in range(len(G.nodes)):
            if not v in l[1] and not v in l[0]:
                l_v = [l[0] | {v}, l[1] | G.nodes[v].connections]
                if not any([l_v[0] == n[0] for n in p]):
                    p.append(l_v)
    if timeit: print(f'distinct_pinnacle_placement runtime = {time()-t}secs')
    return p

def fill_pinnacle_placement(G: Graph, dpp: list, p_set: list, timeit: bool = False) -> int | list:
    """Calculate all possible labelings of G give a distinct pinnacle placement and a pinnacle set.
    You should never have to call this!

    Args:
        G (Graph): Graph to label.
        dpp (list): Exactly 1 distinct pinnacle placement
        p_set (list): pinnacle set to use, must be same size as dpp[0]
        timeit (bool, optional): Prints the runtime for the method. Defaults to False.

    Returns:
        int | list: returns the total number of possible labelings as well as all distinct graphs, down until the smallest degree. Beyond that are just permutations.
    """    
    if timeit: t = time()
    for i, n in enumerate(dpp[0]):
        G.nodes[n].set_value(p_set[i])
    G.reach = dpp[0].union(dpp[1])
    not_pinnacle = [i for i in range(len(G.nodes), 0, -1) if not i in p_set and i >= G.get_smallest_degree()]
    graphs = [G]
    graphs_final = []
    total = 0
    for val in not_pinnacle:
        new_graphs = []
        for graph in graphs:
            if val == graph.get_smallest_degree():
                total += factorial(val)
                graphs_final.append(graph.copy())
            else:
                for i in range(len(graph.nodes)):
                    if graph.nodes[i].value == 0 and all([val < graph.nodes[adj].value for adj in graph.nodes[i].connections if graph.nodes[adj].value in p_set]) and any([val < graph.nodes[adj].value for adj in graph.nodes[i].connections]):
                        new_graph = graph.copy()
                        new_graph.set_node_value(i,val)
                        if len(new_graph.reach) == len(new_graph.nodes) and val < min(p_set):
                            total += factorial(sum([1 for node in new_graph.nodes if node.value == 0]))
                            graphs_final.append(new_graph)
                        else: new_graphs.append(new_graph)
        graphs = new_graphs
    if timeit: print(f'distict_pinnacle_fill rutime = {time()-t}secs')
    return total, graphs_final

def distinct_graph_labelings(G: Graph, p_set: list, timeit: bool = False) -> int | list:
    """Generates the total number of distinct labelings of G with a given pinnacle set.

    Args:
        G (Graph): Graph to label.
        p_set (list): Pinnacle set to use.
        timeit (bool, optional): Prints a runtime of the method. Defaults to False.

    Returns:
        int | list: Returns the total number of labelings and each distinct graph down to the smallest degree.
    """    
    if timeit: t = time()
    dpp = distinct_pinnacle_placement(G, len(p_set))
    permutations = []
    _generate_permutations(permutations, p_set, len(p_set))
    total_final = 0
    graphs_final = []
    for pinnacle_placement in dpp:
        for p in permutations:
            total, l = fill_pinnacle_placement(G, pinnacle_placement, p)
            total_final += total
            graphs_final.extend(l)
            G.clear()
    if timeit: print(f'distinct_graph_labelings runtime = {time()-t}secs')
    return total_final, graphs_final

###############
# BRUTE FORCE #
###############

def get_all_pinnacle_data(G: Graph, timeit: bool = False) -> dict:
    """Tests every possible permutation and logs all the occurences of each pinnacle set. This is very slow! Be warned.

    Args:
        G (Graph): Graph to get all labelings for
        timeit (bool, optional): Prints the runtime for the method. Defaults to False.

    Returns:
        dict: dictionary containing all pinnacle sets mapped to the number of occurences
    """    
    if timeit: t = time()
    permutations = generate_permutations(len(G.nodes))
    d = {}
    for p in permutations:
        pinnacles = G.get_pinnacles(p)
        if d.get(str(pinnacles)) == None:
            d[str(pinnacles)] = 1
        else:
            d[str(pinnacles)] += 1
    if timeit: print(f'get_all_pinnacle_data runtime = {time()-t}secs')
    d = sorted(d.items(), key=lambda x:x[1], reverse=True)
    return d 

############
# FORMULAS #
############

def enumerate_star(k: int, n: int, i: int) -> int:
    if i == 0:
        return k*(factorial(n-1)+(n-k)*factorial(n-2))
    elif i > 0 and i < n-k:
        return int(k*(factorial(n-k)/factorial(n-k-i-1))*factorial(n-i-2))
    else:
        return 0

#####################
# IF NAME THEN MAIN #
#####################

def main():
    G = create_graph(9, 'star-2')
    print(distinct_graph_labelings(G, [9,8])[0])
    print(enumerate_star(2,9,1))


if __name__ == "__main__":
    main()