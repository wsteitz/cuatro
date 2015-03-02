from cuatro import Dice
from fields import *


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
