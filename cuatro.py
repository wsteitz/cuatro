from collections import defaultdict
import random
import copy

from board import Board
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
                    if self.board.four_in_a_row():
                        return player

    def _stones_left(self):
        stones = sum([p.stones for p in self.players])
        return stones > 0

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
    #g.add_player(Human("Adam"))
    g.add_player(Human("Eve"))

    g.start()

