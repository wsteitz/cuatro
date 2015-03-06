from cuatro.dice import Dice
from cuatro.fields import *


def test_one():
    d = Dice()
    d._update([2, 2, 2, 3, 4])
    assert One.fits(d) == False
    d._update([1, 2, 2, 3, 4])
    assert One.fits(d) == False
    d._update([1, 1, 2, 3, 4])
    assert One.fits(d) == True
    d._update([1, 1, 1, 3, 4])
    assert One.fits(d) == True
    d._update([1, 1, 1, 1, 4])
    assert One.fits(d) == True
    d._update([1, 1, 1, 1, 1])
    assert One.fits(d) == True


def test_straight():
    d = Dice()
    straight = Straight()
    d._update([1, 2, 3, 4, 4])
    assert straight.fits(d) == False
    d._update([1, 2, 3, 4, 5])
    assert straight.fits(d) == True
    d._update([6, 2, 3, 4, 5])
    assert straight.fits(d) == True
