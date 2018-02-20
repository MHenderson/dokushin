import constraint
import sudoku

def add_row_constraints(problem, boxsize):
    """add_row_constraints(problem, boxsize)

    Adds to constraint problem 'problem', all_different constraints on rows."""
    for row in sudoku.utils.cells_by_row(boxsize):
        problem.addConstraint(constraint.AllDifferentConstraint(), row)

def add_col_constraints(problem, boxsize):
    """add_col_constraints(problem, boxsize)

    Adds to constraint problem 'problem', all_different constraints on columns."""
    for col in sudoku.utils.cells_by_col(boxsize):    
       problem.addConstraint(constraint.AllDifferentConstraint(), col)

def add_box_constraints(problem, boxsize):
    """add_box_constraints(problem, boxsize)

    Adds to constraint problem 'problem', all_different constraints on boxes."""
    for box in sudoku.utils.cells_by_box(boxsize):
        problem.addConstraint(constraint.AllDifferentConstraint(), box)

def empty_puzzle_as_CP(boxsize):
    """empty_puzzle(boxsize) -> constraint.Problem

    Returns a constraint problem representing an empty Sudoku puzzle of 
    box-dimension 'boxsize'."""
    p = constraint.Problem()
    p.addVariables(sudoku.utils.cells(boxsize), sudoku.utils.symbols(boxsize)) 
    add_row_constraints(p, boxsize)
    add_col_constraints(p, boxsize)
    add_box_constraints(p, boxsize)
    return p

def puzzle_as_CP(fixed, boxsize):
    """puzzle_as_CP(fixed, boxsize) -> constraint.Problem

    Returns a constraint problem representing a Sudoku puzzle, based on 
    'fixed' cell dictionary."""
    p = empty_puzzle_as_CP(boxsize)
    for cell in fixed:
        p.addConstraint(constraint.ExactSumConstraint(fixed[cell]), [cell])
    return p

def to_minion_3_string_s(fixed, boxsize):
    n = n_rows(boxsize)
    s = n_symbols(boxsize)
    def header():
        return "MINION 3\n"
    def variables():
        return "**VARIABLES**\nDISCRETE l[" + str(n) + "," + str(n) +"] {1.." + str(s) +"}\n"
    def search():
        return "**SEARCH**\nPRINT ALL\n"
    def row_constraint(row):
        return "alldiff(l[" + str(row - 1) + ",_])\n"
    def column_constraint(col):
        return "alldiff(l[_," + str(col - 1) + "])\n"
    def box_constraint(box):
       return 'alldiff([' + string.strip(reduce(operator.add, ['l[' + str(row(cell, boxsize) - 1) + ',' + str(column(cell, boxsize) - 1)+'],' for cell in box]),',') + '])\n'
    def clue_constraint(clue):
        return "eq(l[" + str(row(clue, boxsize) - 1) + "," + str(column(clue, boxsize) - 1) + "]," + str(fixed[clue]) +")\n"
    def row_constraints():
        return reduce(operator.add, [row_constraint(row) for row in rows(boxsize)])
    def column_constraints():
        return reduce(operator.add, [column_constraint(col) for col in cols(boxsize)])
    def box_constraints():
        return reduce(operator.add, [box_constraint(box) for box in cells_by_box(boxsize)])
    def clue_constraints():
        if len(fixed)==0:
            return ""
        else:
            return reduce(operator.add, flatten([clue_constraint(clue) for clue in fixed]))
    def constraints():
        return "**CONSTRAINTS**\n" + row_constraints() + column_constraints() + box_constraints() + clue_constraints()
    def footer():
        return "**EOF**"
    return header() + variables() + search() + constraints() + footer()

def solve_as_CP(fixed, boxsize):
    """Use constraint programming to solve Sudoku puzzle of dimension 'boxsize'
    with 'fixed' cells."""
    return puzzle_as_CP(fixed, boxsize).getSolution()
