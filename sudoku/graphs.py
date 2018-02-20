import networkx

from sudoku.utils import cells, dependent_cells, graph_to_dict

####################################################################
# Graph models
####################################################################

def empty_puzzle_as_graph(boxsize):
    """empty_puzzle_as_graph(boxsize) -> networkx.Graph

    Returns the Sudoku graph of dimension 'boxsize'."""   
    g = networkx.Graph()
    g.add_nodes_from(cells(boxsize))
    g.add_edges_from(dependent_cells(boxsize))
    return g

def puzzle_as_graph(fixed, boxsize):
    """Graph model of Sudoku puzzle of dimension 'boxsize' with 'fixed'
    cells."""
    g = empty_puzzle_as_graph(boxsize)
    for cell in fixed:
        g.node[cell]['color'] = fixed[cell]
    return g

####################################################################
# Vertex coloring algorithms
####################################################################

def neighboring_colors(graph, node):
    """Returns list of colors used on neighbors of 'node' in 'graph'."""
    return filter(None, [graph.node[neighbor].get('color') for neighbor in graph.neighbors(node)])

def n_colors(graph):
    """The number of distinct colors used on vertices of 'graph'."""
    return len(set([graph.node[i]['color'] for i in graph.nodes()]))

def least_missing(colors):
    """The smallest integer not in 'colors'."""
    colors.sort()
    for color in colors:
        if color + 1 not in colors:
            return color + 1

def first_available_color(graph, node):
    """The first color not used on neighbors of 'node' in 'graph'."""
    used_colors = neighboring_colors(graph, node)
    if len(used_colors) == 0:
        return 1
    else:
        return least_missing(used_colors)

def saturation_degree(graph, node):
    """Saturation degree of 'node' in 'graph'."""
    return len(set(neighboring_colors(graph, node)))

class FirstAvailableColor():
    """First available color choice visitor."""

    def __call__(self, graph, node):
        return first_available_color(graph, node)

class InOrder():
    """Natural vertex ordering strategy."""

    def __init__(self, graph):
        self.graph = graph

    def __iter__(self):
        return self.graph.nodes_iter()

class RandomOrder():
    """Random vertex ordering strategy."""

    def __init__(self, graph):
        self.graph = graph
        self.nodes = self.graph.nodes()

    def __iter__(self):
        random.shuffle(self.nodes)
        return iter(self.nodes)

class DSATOrder():
    """Saturation degree vertex ordering strategy."""

    def __init__(self, graph):
        self.graph = graph
        self.nodes = self.graph.nodes()
        self.value = 0

    def dsatur(self, node):
        return saturation_degree(self.graph, node)

    def next(self):
        self.value += 1
        if self.value > self.graph.order(): raise StopIteration
        self.nodes.sort(key = self.dsatur)
        return self.nodes.pop()

    def __iter__(self):
        return self

def vertex_coloring(graph, nodes = InOrder, choose_color = FirstAvailableColor):
    """Generic vertex coloring algorithm. Node ordering specified by 'nodes'
    iterator. Color choice strategy specified by 'choose_color'."""
    for node in graph.nodes():
        if not graph.node[node].get('color'):
            graph.node[node]['color'] = choose_color()(graph, node)
    return graph

def solve_as_graph(fixed, boxsize):
    """Use vertex coloring to solve Sudoku puzzle of dimension 'boxsize'
    with 'fixed' cells."""
    g = puzzle_as_graph(fixed, boxsize)
    cg = vertex_coloring(g, DSATOrder)
    return graph_to_dict(cg)
