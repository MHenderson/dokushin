# Sean Davis, Matthew Henderson, Andrew Smith (Berea) 4.1.2010

import random, itertools, string, operator, copy

import networkx

####################################################################
# Basic parameters
####################################################################

def n_rows(boxsize): return boxsize**2
def n_cols(boxsize): return boxsize**2
def n_boxes(boxsize): return boxsize**2
def n_symbols(boxsize): return max(n_rows(boxsize), n_cols(boxsize))
def n_cells(boxsize): return n_rows(boxsize)*n_cols(boxsize)

####################################################################
# Cell label functions
####################################################################

def cell(row, column, boxsize): return (row - 1) * n_rows(boxsize) + column
def column(cell, boxsize): return (cell - 1) % n_rows(boxsize) + 1
def row(cell, boxsize): return (cell - 1) / n_cols(boxsize) + 1

def box_representative(box, boxsize):
    i = boxsize * ((box - 1) / boxsize)
    j = boxsize * ((box - 1) % boxsize) + 1
    return boxsize**2*i + j

####################################################################
# Convenient ranges
####################################################################

def cells(boxsize): return range(1, n_cells(boxsize) + 1)
def symbols(boxsize): return range(1, n_symbols(boxsize) + 1)
def rows(boxsize): return range(1, n_rows(boxsize) + 1)
def cols(boxsize): return range(1, n_cols(boxsize) + 1)
def boxes(boxsize): return range(1, n_boxes(boxsize) + 1)

def row_r(row, boxsize):
    """Cell labels in 'row' of Sudoku puzzle of dimension 'boxsize'."""
    nr = n_rows(boxsize)
    return range(nr * (row - 1) + 1, nr * row + 1)

def col_r(column, boxsize):
    """Cell labels in 'column' of Sudoku puzzle of dimension 'boxsize'."""
    nc = n_cols(boxsize)
    ncl = n_cells(boxsize)
    return range(column, ncl + 1 - (nc - column), nc)

def box_r(box, boxsize):
    """Cell labels in 'box' of Sudoku puzzle of dimension 'boxsize'."""
    return [box_representative(box, boxsize) + j + k - 1 for j in range(0, boxsize * n_rows(boxsize), n_cols(boxsize)) for k in range(1, boxsize + 1)]

def cells_by_row(boxsize):
    """cells_by_row(boxsize) -> list

    Returns a list of cell labels ordered by row for the given boxsize."""
    return [row_r(row, boxsize) for row in rows(boxsize)]

def cells_by_col(boxsize):
    """cells_by_col(boxsize) -> list

    Returns a list of cell labels ordered by column for the given boxsize."""
    return [col_r(column, boxsize) for column in cols(boxsize)]

def cells_by_box(boxsize):
    """cells_by_box(boxsize) -> list

    Returns a list of cell labels ordered by box for the given boxsize."""
    return [box_r(box, boxsize) for box in boxes(boxsize)]

def puzzle_rows(puzzle, boxsize):
    """Cell values, ordered by row."""
    return [map(puzzle.get, row_r(row, boxsize)) for row in rows(boxsize)]

def puzzle_columns(puzzle, boxsize):
    """Cell values, ordered by column."""
    return [map(puzzle.get, col_r(column, boxsize)) for column in cols(boxsize)]

def puzzle_boxes(puzzle, boxsize):
    """Cell values, ordered by box."""
    return [map(puzzle.get, box_r(box, boxsize)) for box in boxes(boxsize)]

####################################################################
# Convenient functions
####################################################################

def ordered_pairs(range):
    """All ordered pairs from objects in 'range'."""
    return itertools.combinations(range, 2)

def flatten(list_of_lists):
    "Flatten one level of nesting"
    return itertools.chain.from_iterable(list_of_lists)

def int_to_printable(i):
    """Convert an integer to a printable character."""
    return string.printable[i]

def printable_to_int(c):
    """Convert a printable character to a integer."""
    return string.printable.index(c)

def are_all_different(l):
    """Test whether all elements in range 'l' are different."""
    return all(itertools.starmap(operator.ne, ordered_pairs(l)))

def are_all_different_nested(l):
    """Test whether every range in range 'l' is a range of all different
    elements."""
    return all(map(are_all_different, l))

def strip_ws(puzzle_string):
    """Remove newline and space characters from a string."""
    return puzzle_string.replace('\n', '').replace(' ','')

def colorize(c, color = '1'):
    CSI = '\x1b['
    reset = CSI + 'm'
    return CSI + "3" + color + "m" + c + reset

def diff_s(s1, s2):
    s = ''
    for i in range(len(s1)):
        if s1[i]!=s2[i]:
            s += colorize(s2[i])
        else:
            s += s2[i]
    return s

####################################################################
# Cell dependencies
####################################################################

def dependent_cells(boxsize):
    """List of all pairs (x, y) with x < y such that x and y either lie in the 
    same row, same column or same box."""
    return list(set(flatten(map(list, map(ordered_pairs, cells_by_row(boxsize) + cells_by_col(boxsize) + cells_by_box(boxsize))))))

####################################################################
# String/dictionary conversions
####################################################################

def dict_to_string_(fixed, boxsize, padding = 0, rowend = "", row_sep = "", box_sep = "", col_sep = "", last_row_hack = ""):
    """Returns a puzzle string of dimension 'boxsize' from a dictionary of 
    'fixed' cells."""
    s = ''
    s += row_sep
    for row in rows(boxsize):
        s += box_sep
        for col in cols(boxsize):
            symbol = fixed.get(cell(row, col, boxsize))
            if symbol:
                s += int_to_printable(symbol) + " "*padding
            else:
                s += '.' + ' '*padding
            if col % boxsize == 0:
                s += box_sep
            if col < boxsize*boxsize:
               s += col_sep
        s += rowend               
        if (row % boxsize == 0 and row < boxsize*boxsize):
            s += row_sep
        elif row == boxsize*boxsize:
            s += last_row_hack
    return s

def dict_to_string(fixed, boxsize, padding = 0, rowend = ""):
    """Returns a puzzle string of dimension 'boxsize' from a dictionary of 
    'fixed' cells with some suitably chosen row/column seperators."""
    row_sep = boxsize*('+' + (2*boxsize + 1) * '-') + '+' + '\n'
    box_sep = '| '
    return dict_to_string_(fixed, boxsize, padding, rowend, row_sep, box_sep, "")

def string_to_dict(puzzle, boxsize):
    """Returns a dictionary based on a Sudoku puzzle string."""
    puzzle = strip_ws(puzzle)
    d = {}
    for cell in cells(boxsize):
        if puzzle[cell - 1] != '.':
            d[cell] = int(printable_to_int(puzzle[cell - 1]))
    return d

def graph_to_dict(graph):
    """Colored graph to dictionary conversion."""
    nodes = graph.node
    return dict([(vertex, nodes[vertex].get('color')) for vertex in nodes])

####################################################################
# Graph output
####################################################################

def dimacs_string(graph):
    """Returns a string in Dimacs-format representing 'graph'."""
    s = ""
    s += "p " + "edge " + str(graph.order()) + " " + str(graph.size()) + "\n"
    for edge in graph.edges():
        s += "e " + str(edge[0]) + " " + str(edge[1]) + "\n"
    return s
