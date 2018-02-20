import glpk
import itertools

from sudoku.utils import n_cells, n_symbols, flatten, cells_by_row, symbols, cells_by_col, cells_by_box, cells

####################################################################
# Linear program models
####################################################################

def lp_matrix_ncols(boxsize): return n_cells(boxsize) * n_symbols(boxsize)

def lp_matrix_nrows(boxsize): return 4*boxsize**4 # what is the origin of this number?

def lp_vars(boxsize):
    """Variables for Sudoku puzzle linear program model."""
    return list(itertools.product(cells(boxsize), symbols(boxsize)))

def lp_col_index(cell, symbol, boxsize):
    """The column of the coefficient matrix which corresponds to the variable
    representing the assignment of 'symbol' to 'cell'."""
    return (cell - 1)*n_symbols(boxsize) + symbol - 1

def lp_occ_eq(cells, symbol, boxsize):
    """Linear equation (as list of coefficients) which corresponds to the cells
    in 'cells' having one occurence of 'symbol'."""
    coeffs = lp_matrix_ncols(boxsize)*[0]
    for cell in cells:
        coeffs[lp_col_index(cell, symbol, boxsize)] = 1
    return coeffs

def lp_nonempty_eq(cell, boxsize):
    """Linear equation (as list of coefficients) which corresponds to 'cell' 
    being assigned a symbol from 'symbols'."""
    coeffs = lp_matrix_ncols(boxsize)*[0]
    for symbol in symbols(boxsize):
        coeffs[lp_col_index(cell, symbol, boxsize)] = 1
    return coeffs

def lp_occ_eqs(cells_r, boxsize):
    """Linear equations (as lists of coefficients) which correspond to the
    cells in cells_r having one occurence of every symbol."""
    return [lp_occ_eq(cells, symbol, boxsize) for cells in cells_r for symbol in symbols(boxsize)]

def lp_nonempty_eqs(boxsize):
    """Linear equations (as lists of coefficients) which correspond to 
    every cell having one symbol."""
    return [lp_nonempty_eq(cell, boxsize) for cell in cells(boxsize)]

def lp_coeffs(boxsize):
    """Linear equations (as lists of coefficients) which correspond to 
    the empty Sudoku puzzle."""
    return lp_occ_eqs(cells_by_row(boxsize), boxsize) + lp_occ_eqs(cells_by_col(boxsize), boxsize) + lp_occ_eqs(cells_by_box(boxsize), boxsize) + lp_nonempty_eqs(boxsize)

def lp_matrix(boxsize):
    """Linear equations (as list of coefficients) which correspond to 
    the empty Sudoku puzzle."""
    return list(flatten(lp_coeffs(boxsize)))

def empty_puzzle_as_lp(boxsize):
    """Linear program for empty Sudoku puzzle."""
    lp = glpk.LPX()
    lp.cols.add(lp_matrix_ncols(boxsize))
    lp.rows.add(lp_matrix_nrows(boxsize))
    for c in lp.cols:
        c.bounds = 0.0, 1.0
    for r in lp.rows:
        r.bounds = 1.0, 1.0
    lp.matrix = lp_matrix(boxsize)
    return lp

def add_clue_eqn(cell, symbol, boxsize, lp):
    """Add to 'lp' the linear equation representing the assignment of 'symbol'
    to 'cell'."""
    lp.rows.add(1)
    r = lp_matrix_ncols(boxsize)*[0]
    r[lp_col_index(cell, symbol, boxsize)] = 1
    lp.rows[-1].matrix = r
    lp.rows[-1].bounds = 1.0, 1.0

def puzzle_as_lp(fixed, boxsize):
    """Linear program for Sudoku with 'fixed' clues."""
    lp = empty_puzzle_as_lp(boxsize)
    for cell in fixed:
        symbol = fixed[cell]       
        add_clue_eqn(cell, symbol, boxsize, lp)
    return lp

def lp_to_dict(lp, boxsize):
    names = lp_vars(boxsize)
    sol = {}
    for c in lp.cols:
        if c.value == 1:
            sol[names[c.index][0]] = names[c.index][1]
    return sol

def solve_lp_puzzle(lp, boxsize):
    """Solve a linear program Sudoku and return puzzle dictionary."""
    lp.simplex()
    for col in lp.cols:
        col.kind = int
    lp.integer()
    return lp_to_dict(lp, boxsize)

def solve_as_lp(fixed, boxsize):
    """Use linear programming to solve Sudoku puzzle of dimension 'boxsize'
    with 'fixed' cells."""
    return solve_lp_puzzle(puzzle_as_lp(fixed, boxsize), boxsize)
