import dokushin

from dokushin import n_rows, box_representative

def test_nrows():
    assert n_rows(3) == 9

def test_box_representative():
    assert box_representative(1, 3) == 1
    assert box_representative(2, 3) == 4
    assert box_representative(3, 3) == 7
    assert box_representative(4, 3) == 28
    assert box_representative(5, 3) == 31
    assert box_representative(6, 3) == 34
    assert box_representative(7, 3) == 55
    assert box_representative(8, 3) == 58
    assert box_representative(9, 3) == 61
