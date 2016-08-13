from game import Game
from player import Human
from player import GoForYahtzee


if __name__ == "__main__":
    g = Game()
    #g.add_player(Human())
    g.add_player(GoForYahtzee())
    g.add_player(GoForYahtzee("yahtzee2"))

    g.start()
    print g.board

