import pytest
import sudoku

def test_0():
    assert len(sudoku.cells(0))==len([])
    assert len(sudoku.symbols(0))==len([])
    assert len(sudoku.cells_by_row(0))==len([])

