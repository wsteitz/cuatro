
class Field:
    
    def __init__(self, name):
        self.name = name
        self.height = 0
        self.player = "-"
        
    def place(self, player, dice):
        if self.fits(dice):
            self.height += 1
            self.player = player.name
    
    def fits_height(self, dice):
        return 5 - self.height >= dice.throws
        
    def __repr__(self):
        return self.name


class CountField(Field):
    
    def __init__(self, name, count):
        Field.__init__(self, name)
        self.count = count
    
    def fits(self, dice):
        if max(dice.counts.values()) >= self.count:
            return self.fits_height(dice)
        return False


class ThreeOfAKind(CountField):
    
    def __init__(self):
        CountField.__init__(self, "ThreeOfAKind", 3)


class FourOfAKind(CountField):
    
    def __init__(self):
        CountField.__init__(self, "FourOfAKind", 4)


class FiveOfAKind(CountField):
    
    def __init__(self):
        CountField.__init__(self, "FiveOfAKind", 5)
        
        
class FullHouse(Field):
    
    def __init__(self):
        Field.__init__(self, "FullHouse")
    
    def fits(self, dice):
        if max(dice.counts.values()) == 3 and min(dice.counts.values()) == 2:
            return self.fits_height(dice)
        return False 
        
        
class Street(Field):
    
    def __init__(self):
        Field.__init__(self, "Street")
    
    def fits(self, dice):
        s = set(dice.dices)
        if s == (1, 2, 3, 4, 5) or s == (2, 3, 4, 5, 6):
            return self.fits_height(dice)
        return False 


class NumberField(Field):
    
    def __init__(self, name, number):
        Field.__init__(self, name)
        self.number = number
    
    def fits(self, dice):
        if dice.counts[self.number] >= 2:
            return self.fits_height(dice)
        return False


One = NumberField("Ones", 1)
Two = NumberField("Twos", 2)
Three = NumberField("Threes", 3)
Four = NumberField("Fours", 4)
Five = NumberField("Fives", 5)
Six = NumberField("Sixes", 6)


