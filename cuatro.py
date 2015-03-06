
from game import Game
from player import Human


if __name__ == "__main__":
    g = Game()
    #g.add_player(Human("Adam"))
    g.add_player(Human("Eve"))

    g.start()

