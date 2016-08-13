
class Player:
    """ Base class of a cuatro player """

    def __init__(self, name):
        self.name = name
        # the color is assigned by the Game, when the player is added.
        self.color = None

    def play(self, *args):
        print "not implemented"
        return []

    def place(self, *args):
        print "not implemented"


class Human(Player):
    """ A console-based human player. """

    def __init__(self, name="Human"):
        Player.__init__(self, name)

    def play(self, dice, board):
        print board
        print dice.throws, "\t", dice
        keep = raw_input("which numbers do you want to keep? ")
        return [int(k) for k in keep if k.isdigit()]

    def place(self, dice, board):
        print board
        print dice
        place = ""
        while len(place) != 2:
            place = raw_input("where to place your piece? ").upper()
        return place


class GoForYahtzee(Player):

    weights = {
        "Yahtzee": 200,
        "Full House": 90,
        "Straight": 90,
        "4-of-a-kind": 80,
        "3-of-a-kind": 40,
        "Ones": 5,
        "Twos": 5,
        "Threes": 5,
        "Fours": 5,
        "Fives": 5,
        "Sixes": 5
     }

    def __init__(self, name="GoForYahtzeeBot"):
        Player.__init__(self, name)

    def play(self, dice, board):
        maximum = max(dice.counts, key=dice.counts.get)
        max_count = dice.counts[maximum]
        keep = [maximum] * max_count
        print self.name, dice, keep
        return keep

    def place(self, dice, board):
       # score each field ==> take highest
       candidates = []
       for field in board.fields():
           if field.fits(dice):
               score = self.weights[field.name] * (1 + field.height * 0.2)
               candidates.append((score, field.position))
       pos = None if len(candidates) == 0 else max(candidates)[1]
       return pos
