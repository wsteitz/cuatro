from collections import defaultdict
import random
import copy
import texttable

from fields import *
from player import Human


class Dice:
    """ Representation of the five dice

    Attributes:
      throws (int): How often the dice were rolled.
      faces (list[int]): the current faces of the dice.
      counts (dict[int->int]): occurances of each face value.

    """

    def __init__(self):
        self.throws = 0
        self.faces = [0, 0, 0, 0, 0]
        self.counts = {}

    def roll(self, keep=None):
        # making sure only existing faces are kept
        keep = self.verify(keep)
        # increase counter
        self.throws += 1
        if keep is not None:
            to_throw = 5 - len(keep)
        else:
            to_throw = 5
            keep = []
        # update faces
        self._update(keep + [random.randint(1, 6) for i in range(to_throw)])

    def _update(self, values):
        """ updates the face values of the dice"""
        self.faces = values
        self._update_counts()

    def _update_counts(self):
        """ update face counter """
        self.counts = defaultdict(int)
        for num in self.faces:
            self.counts[num] += 1

    def verify(self, keep):
        """ verifies that keep only contains existing faces """
        verified = []
        available = self.faces[:]
        for k in keep:
            if k in available:
                verified.append(k)
                available.remove(k)
        return verified

    def __repr__(self):
        """ string representation """
        return " ".join([str(d) for d in sorted(self.faces)])


class Board:

    def __init__(self):
        self.matrix = [[FullHouse(), ThreeOfAKind(), FourOfAKind(), Straight(), One, ThreeOfAKind()],
                       [Straight(), Six, ThreeOfAKind(), FullHouse(), Yahtzee(), FourOfAKind()],
                       [FourOfAKind(), FullHouse(), Yahtzee(), Straight(), ThreeOfAKind(), Three],
                       [FullHouse(), Straight(), Five, FourOfAKind(), FullHouse(), ThreeOfAKind()],
                       [Two, Yahtzee(), FullHouse(), ThreeOfAKind(), FourOfAKind(), Straight()],
                       [ThreeOfAKind(), FourOfAKind(), Straight(), Four, Straight(), FullHouse()]
                      ]

    def place(self, place, player, dice):
        field = self.matrix[place[0]][place[1]]
        return field.place(player, dice)

    def __repr__(self):
        table = texttable.Texttable(max_width=120)
        table.set_cols_align(["c"] * (len(self.matrix) + 1))
        table.add_row([""] + [str(i) for i in range(len(self.matrix))])
        for num, row in enumerate(self.matrix):
            items = [num]
            for field in row:
                items.append("%s\n\n%s\n%i" % (field.name, field.player, field.height))
            table.add_row(items)
        return table.draw()


class Game:
    colors = ['blue', 'red', 'green', 'yellow']
    max_players = 4

    def __init__(self):
        self.players = []

    def add_player(self, player):
        if len(self.players) < self.max_players:
            self.players.append(player)
            player.color = self.colors[len(self.players) - 1]

    def start(self):
        self.board = Board()
        self.rounds = 0
        self.winner = self._loop()
        print self.winner.name, "wins the game in", self.rounds, "rounds"

    def _loop(self):
        while True:
            self.rounds += 1
            if not self._stones_left():
                return None
            for player in self.players:
                if player.stones > 0:
                    self._turn(player)
                    if self._is_finished():
                        return player

    def _stones_left(self):
        stones = sum([p.stones for p in self.players])
        return stones > 0

    def _is_finished(self):
        print "not implemented"
        return False

    def _turn(self, player):
        # pass a copy of the original board, so the players cannot cheat
        board = copy.deepcopy(self.board)
        dice = Dice()
        keep = []
        for throw in range(1, 5):
            dice.roll(keep)
            keep = player.play(dice, board)
            # verify the answer of the player
            keep = dice.verify(keep)
            if len(keep) == 5:
                break
        # last roll, nothing for the player to decide
        dice.roll(keep)
        # ask player where to place the stone
        place = player.place(dice, board)
        placed = self.board.place(place, player, dice)
        if placed:
            player.stones -= 1


if __name__ == "__main__":
    g = Game()
    g.add_player(Human("Adam"))
    g.add_player(Human("Eve"))
    g.start()

