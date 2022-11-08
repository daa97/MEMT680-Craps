from interface import App
from random import randint

def catch(err_func):
    def inner_func(err_func, *args, **kwargs):
        try:
            err_func(*args, **kwargs)
        except ValueError:
            print("Bet must be in dollars!")
            


class Dice:
    def __init__(self):
        self.total = None
        self.each = None
    
    def roll(self):
        self.each = (randint(1,6),randint(1,6))
        self.total = sum(self.each)
        return self.total

class Table(Dice):
    def __init__(self):
        super().__init__()
        self.point = False

class Player(Table):
    def __init__(self):
        super().__init__()
        
class Bets(Player):
    def __init__(self):
        super().__init__()



def chance(roll):                   # returns the probability of a given roll (2-12) occuring
    return (6 - abs(roll-7))/6**2   # rolls have 1/36, 2/36, 3/36 chance, with peak of 6/36 for a seven