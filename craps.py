from numpy.random import randint

from interface import *



def catch(err_func):
    def inner_func(err_func, *args, **kwargs):
        try:
            err_func(*args, **kwargs)
        except ValueError:
            print("Bet must be in dollars!")
            


class Dice:
    "Represents a set of dice"
    def __init__(self, count=2, sides=6):
        self.count = count      # number of dice which are rolled
        self.sides = sides      # number of sides per die
        self.total = None
        self.each = None
        self.dist = self.pmf()

    def chance(self, value):
        return self.dist[value]


    def pmf(self):
        "returns a probability mass function for dice results"
        p0 = [1]*self.sides                 # frequency of each dice roll for single die
        pnew = p0                           # frequency of possible summed rolls for first die only
        for die in range(1,self.count):     # iterate through each die which is rolled
            pi = pnew                       # frequency for summed rolls of all previous dice
            pnew = [0]*(self.sides*(die+1)-die) # initializes frequency for combination of all dice up to current
            for roll in range(len(pi)):     # roll
                for nextroll in range(len(p0)):
                    pnew[roll+nextroll] += pi[roll]*p0[nextroll]
        pdict = dict()
        for i in range(len(pnew)):
            pdict[i+self.count] = float(pnew[i]) / (self.sides**self.count)
        return pdict        # returns dictionary containing pairs of (roll total):(probability)
    

    def roll(self):
        "Rolls dice and returns the total value of the roll"
        self.each = [randint(1,7) for i in range(self.count)]
        self.total = sum(self.each)
        return self.each

class Table(Dice):
    "Represents a craps table at which games take place"
    def __init__(self):
        super().__init__()
        self.point = False

class Player(Table): 
    "Represents a single player at the table"
    def __init__(self):
        super().__init__()
        self.name = EntryBox("Please enter your name:").userval()
        balance_box = EntryBox("Please enter the balance you want to gamble:", check_func=lambda s: remove(s,"$,0_ ").isnumeric())
        self.balance = int(remove(balance_box.userval(),"$,"))
        print(self.balance)

class Bets(Player, App):
    "Represents bets belonging to a particular player"
    def __init__(self):
        #super().__init__()
        Player.__init__(self)
        App.__init__(self)
        self.title(f"{self.name} plays craps")
        self.pass_bet = 0
        self.no_pass_bet = 0
        self.odds_bet = 0
        self.max_odds = 0
        self.payout = 0
        self.mainloop()

    def pass_line(self):
        if not self.point:
            userval = self.ingest_bet()
            if userval is not None:
                self.pass_bet = userval
                self.shooter()
            
    def do_not_pass(self):
        if not self.point:
            userval = self.ingest_bet()
            if userval is not None:
                self.no_pass_bet = userval
                self.shooter()

    def shooter(self):
        if max(self.pass_bet, self.no_pass_bet) != 0:
            val = sum(self.roll())
            if val==7 or val==11:
                pass

    def ingest_bet(self):
        bet = remove(self.betvar.get(), "$,_ ")
        if not bet.isnumeric():                     # check if bet contains non-numeric symbols
            if remove(bet,".").isnumeric():         # check if bet is number with decimal
                messagebox.showerror(message="Bet must be whole dollar amount!")
            elif remove(bet,"-").isnumeric():       # check if bet contains a minus sign
                messagebox.showerror(message="Bet must be positive!")
            else:                                   # if bet is not a number at all
                messagebox.showerror(message="Bet must be a number!")
        elif int(bet)<1:                            # check if bet is zero
            messagebox.showerror(message="Bet must be greater than zero!")
        elif int(bet)>self.balance:                 # check if bet is greater than player balance
            messagebox.showerror(message=f'''You don't have enough money for that bet!
                                            \nYour balance: ${self.bets.balance}
                                            \nYou tried to bet: ${bet}
                                            \nWin a few more rounds first...''')

        else:                                       # if bet is valid
            return int(bet)

Bets()