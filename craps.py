from interface import App
from random import randint

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
        



