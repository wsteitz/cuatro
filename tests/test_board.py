from cuatro.board import Board


def test_four_in_a_row():
    b = Board()
    m = b.matrix
    assert b.four_in_a_row() == False
    # check 4 in one row
    m[0][0].players.append("foo")
    m[0][1].players.append("foo")
    m[0][2].players.append("foo")
    m[0][3].players.append("foo")
    assert b.four_in_a_row() == True
    
    # check 4 in one col
    b = Board()
    m = b.matrix
    m[0][0].players.append("foo")
    m[1][0].players.append("foo")
    m[2][0].players.append("foo")
    m[3][0].players.append("foo")
    
    # check 4 in one diagonal
    b = Board()
    m = b.matrix
    m[0][0].players.append("foo")
    m[1][1].players.append("foo")
    m[2][2].players.append("foo")
    m[3][3].players.append("foo")
