from collections import defaultdict
import random


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
