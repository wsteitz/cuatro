from collections import defaultdict
import random
import copy
from texttable import Texttable

from fields import *


class Dice:
    
    def __init__(self):
        self.throws = 0
        
    def roll(self, keep=None):
        self.throws += 1
        if keep is not None:
            to_throw = 5 - len(keep)
        else: 
            to_throw = 5
            keep = []
        self.dices = keep + [random.randint(1, 6) for i in range(to_throw)]
        self.update_counts()
        
    def update_counts(self):
        self.counts = defaultdict(int)
        for num in self.dices:
            self.counts[num] += 1
            
    def verify(self, keep):
        verified = []
        available = self.dices[:]
        for k in keep:
            if k in available:
                verified.append(k)
                available.remove(k)
        return verified
        
    def __repr__(self):
        return " ".join([str(d) for d in sorted(self.dices)])
            

#FIXME correct board layout
class Board:
    
    def __init__(self):
        self.matrix = [[ThreeOfAKind(), FourOfAKind(), ThreeOfAKind(), One, Two],
                       [Three, Street(), FullHouse(), Four, FiveOfAKind()],
                       [FiveOfAKind(), ThreeOfAKind(), FourOfAKind(), Street(), FullHouse()],
                       [FourOfAKind(), ThreeOfAKind(), Five, ThreeOfAKind(), FourOfAKind()],
                       [FourOfAKind(), Street(), FiveOfAKind(), FullHouse(), Six]
                      ]
        
    def place(self, place, player, dice):
        field = self.matrix[place[0]][place[1]]
        return field.place(player, dice)
        
    def __repr__(self):
        table = Texttable()
        table.set_cols_align(["c"] * (len(self.matrix) + 1))
        table.add_row([""] + [str(i) for i in range(len(self.matrix))])
        for num, row in enumerate(self.matrix):
            items = [num]
            for field in row:
                items.append("%s\n\n%s\n%i" % (field.name, field.player, field.height))
            table.add_row(items)
        return table.draw()
        
                        
#FIXME keep track of players stones left            
class Game:
    
    def __init__(self):
        self.players = []
                
    def add_player(self, player):
        self.players.append(player)
    
    def start(self):
        self.board = Board()
        self.rounds = 0
        self.winner = self.loop()
        print self.winner.name, "wins the game in", self.rounds, "rounds"
        
    def loop(self):
        while True:
            self.rounds += 1
            if not self.stones_left():
                return None
            for player in self.players:
                if player.stones > 0:
                    self.turn(player)
                    if self.is_finished():
                        return player
    
    def stones_left(self):
        stones = sum([p.stones for p in self.players])
        return stones > 0
                
    def is_finished(self):
        print "not implemented"
        return False
    
    def turn(self, player):
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
        

class Player:
    
    def __init__(self, name):
        self.name = name
        self.stones = 15
        
    def play(self, *args):
        print "not implemented"
        return []
    
    def place(self, *args):
        print "not implemented"
            
        
class Human(Player):
    
    def __init__(self, name):
        Player.__init__(self, name)
     
    def play(self, dice, board):
        print board
        print dice.throws, "\t", dice
        keep = raw_input("which numbers do you want to keep? ")
        return [int(k) for k in keep if k.isdigit()]
    
    def place(self, dice, board):
        print board
        print dice
        place = raw_input("where to place your stone ('row col')? ")
        place = [int(k) for k in place if k.isdigit()]
        return place[0], place [1]
        

if __name__ == "__main__":
    g = Game()
    g.add_player(Human("Adam"))
    g.add_player(Human("Eve"))
    g.start()
    
