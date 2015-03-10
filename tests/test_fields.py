from cuatro.dice import Dice
from cuatro.fields import *


def test_one():
    d = Dice()
    one = One()
    d._update([2, 2, 2, 3, 4])
    assert one.fits(d) == False
    d._update([1, 2, 2, 3, 4])
    assert one.fits(d) == False
    d._update([1, 1, 2, 3, 4])
    assert one.fits(d) == True
    d._update([1, 1, 1, 3, 4])
    assert one.fits(d) == True
    d._update([1, 1, 1, 1, 4])
    assert one.fits(d) == True
    d._update([1, 1, 1, 1, 1])
    assert one.fits(d) == True


def test_straight():
    d = Dice()
    straight = Straight()
    d._update([1, 2, 3, 4, 4])
    assert straight.fits(d) == False
    d._update([1, 2, 3, 4, 5])
    assert straight.fits(d) == True
    d._update([6, 2, 3, 4, 5])
    assert straight.fits(d) == True
