from cuatro.game import Game
from cuatro.player import Human


def test_add_player():
    g = Game()
    g.add_player(Human("1"))
    assert len(g.players) == 1
    for i in range(100):
        g.add_player(Human(str(i)))
    assert len(g.players) == g.max_players


def test_determine_winner():
    # the winner if there is no four-in-a-row after 15 rounds
    g = Game()
    p1 = Human("1")
    g.add_player(p1)
    p2 = Human("2")
    g.add_player(p2)

    # a draw, no one as any points
    assert g._determine_winner() == None

    g.board.matrix[0][0].players.append(p1)
    assert g._determine_winner() == p1

    # putting p2 on top, who should win now
    g.board.matrix[0][0].players.append(p2)
    assert g._determine_winner() == p2

    # building another stack
    g.board.matrix[0][1].players.append(p2)
    assert g._determine_winner() == p2
    g.board.matrix[0][1].players.append(p1)
    # draw again
    assert g._determine_winner() == None
