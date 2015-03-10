import copy

from board import Board
from dice import Dice


class Game:
    colors = ['blue', 'red', 'green', 'yellow']
    max_players = 4
    max_rounds = 15

    def __init__(self):
        self.players = []

    def add_player(self, player):
        if len(self.players) < self.max_players:
            self.players.append(player)
            player.color = self.colors[len(self.players) - 1]

    def start(self):
        self.board = Board()
        self.winner = self._loop()
        print self.winner.name, "wins the game in", self.round, "rounds"

    def _loop(self):
        for round in range(self.max_rounds):
            self.round = round + 1
            for player in self.players:
                self._turn(player)
                if self.board.four_in_a_row():
                    return player
        # if there is no winner after max_rounds, the game ends. The winner is determined by
        # counting the houses...
        return self._determine_winner()

    def _determine_winner(self):
        points = {}
        for player in self.players:
            points[player] = 0
        for field in self.board:
            for i, player in enumerate(field.players):
                points[player] += i + 1
        # return the player with the most points
        return points.keys()[points.values().index(max(points.values()))]

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
        self.board.place(place, player, dice)
