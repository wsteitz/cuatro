import copy

from board import Board
from dice import Dice


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
            if not self._pieces_left():
                return None
            for player in self.players:
                if player.pieces > 0:
                    self._turn(player)
                    if self.board.four_in_a_row():
                        return player

    def _pieces_left(self):
        pieces = sum([p.pieces for p in self.players])
        return pieces > 0

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
        # ask player where to place his/her piece
        place = player.place(dice, board)
        placed = self.board.place(place, player, dice)
        if placed:
            player.pieces -= 1

