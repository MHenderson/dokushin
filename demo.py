import dokushin

s = """
    2 5 . . 3 . 9 . 1
    . 1 . . . 4 . . .
    4 . 7 . . . 2 . 8
    . . 5 2 . . . . .
    . . . . 9 8 1 . .
    . 4 . . . 3 . . .
    . . . 3 6 . . 7 2
    . 7 . . . . . . 3
    9 . 3 . . . 6 . 4
    """

p = dokushin.Puzzle(s, 3, format = 's')

#dokushin.solve(p)

#print(p)

#print(p.fixed)

#dokushin.solve_as_CP(p.fixed, 3)

cp = dokushin.puzzle_as_CP(p.fixed, 3)

cp.getSolution()

#cp._getArgs()

#print(cp.__dir__())

#print(cp._constraints)

#print(dokushin.cells_by_box(3))
#print(dokushin.box_r(10, 3))
#print(dokushin.col_r(10, 3))
#print(dokushin.box_representative(10, 3))