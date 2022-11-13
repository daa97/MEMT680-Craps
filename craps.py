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
        self.each = [1]*count
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
        self.starting_balance = self.balance

class Bets(Player, App):
    "Represents bets belonging to a particular player"
    def __init__(self):
        #super().__init__()
        Player.__init__(self)                               # instantiate player
        App.__init__(self)                                  # instantiate app
        self.title(f"{self.name} plays craps")              # add window title
        self.pass_bet = 0                                   # current wager on pass line
        self.no_pass_bet = 0                                # current wager on don't pass line
        self.odds_bet = 0                                   # current odds bet
        self.max_odds = 0                                   # maximum allowable odds bet (dollar value)
        self.payout = 0                                     # winnings from most recent roll
        
        # button configuration
        self.pass_button.config(command=self.pass_line)     # call pass_line method on button click
        self.no_pass_button.config(command=self.do_not_pass)# call do_not_pass method on button click
        self.odds_button.config(command=self.odds)          # call odds method on button click
        self.roll_button.config(command=self.shooter)       # call shooter method on button click
        self.quit_button.config(command=self.on_close)      # call on_close method on button click
        self.protocol("WM_DELETE_WINDOW", self.on_close)    # call on_close method when user attempts to "X" out of window
        self.update_view()
        self.mainloop()
    
    def pass_line(self):
        "allows a pass line bet to be made"
        if not self.point:
            userval = self.ingest_bet()
            if userval is not None:
                self.pass_bet += userval

                self.shooter()

    def do_not_pass(self):
        "allows a dont pass bet to be made"
        if not self.point:
            userval = self.ingest_bet()
            if userval is not None:
                self.no_pass_bet = userval
                self.shooter()

    def odds(self):
        "allows an odds bet to be made"
        if self.point:
            userval = self.ingest_bet()
            if userval is not None:
                self.odds_bet = userval
                self.shooter()

    def shooter(self):
        "rolls dice and evaluates payout"
        self.payout = 0                     # set winnings from this particular roll
        net_pass = self.pass_bet - self.no_pass_bet
        if self.any_bet():
            val = sum(self.roll())
            if not self.point:              # if no point is set, in come-out phase
                if val==7 or val==11:       # on 7 or 11, pass wins, dont pass loses
                    self.payout = net_pass
                elif val==2  or val==3:     # on 2 or 3, pass loses, dont pass wins
                    self.payout = -net_pass
                elif val==12:               # on 12, pass loses, dont pass ties
                    self.payout = -self.pass_bet
                else:                       # on other rolls, set point
                    self.point = val
                
                if self.point:
                    self.max_odds = (6 - abs(7-val)) * max(self.pass_bet, self.no_pass_bet)
                else:
                    self.clear_bets()
                self.update_view()
            
            else:
                if self.total==7:
                    self.payout = -net_pass 
                    self.clear_bets()
                elif self.total == self.point:
                    self.payout = net_pass
                    self.clear_bets()
                self.update_view() 
    
    def clear_bets(self):
        "clear all existing bets"
        self.balance += self.payout
        self.point = 0
        self.pass_bet = 0
        self.no_pass_bet = 0
        self.odds_bet = 0
        self.max_odds = 0

    def any_bet(self):
        "Checks if any bet is currently on the table"
        return max(self.pass_bet, self.no_pass_bet, self.odds_bet) != 0
    
    def update_view(self):
        "Updates GUI view and options based on current status"
        self.betvar.set("")
        on = lambda tf: [("!" if tf else "") + "disabled"]      # translates boolean T/F into enabled/disabled status for widgets
        self.pass_button.state(on(not self.point))              # pass line bet only enabled during come-out
        self.no_pass_button.state(on(not self.point))           # dont pass bet only enabled during come-out
        self.odds_button.state(on(self.any_bet()))              # odds bet only enabled when bet is on the table
        self.quit_button.state(on(not self.any_bet()))          # quit button only enabled when no bets are on the table
        
        self.die[0]['image'] = self.die_images[self.each[0] - 1]
        self.die[1]['image'] = self.die_images[self.each[1] - 1]
        self.labels['balance'].config(text=f"Balance: ${self.balance:,}")
        total_bet = self.pass_bet + self.no_pass_bet + self.odds_bet
        self.labels['bet'].config(text=f"Bet: ${total_bet:,}")

        if self.point:
            self.labels['point'].configure(text=f"Point: {self.point}")
        else:
            self.labels['point'].configure(text=f"Point: None")
    def on_close(self):
        if self.any_bet():
            messagebox.showerror(title="Not so soon", message="You still have bets on the table!")
        else:
            if messagebox.askyesno(title="Exit Game",
            message="Are you sure you want to quit?"):
                self.destroy()
    
    def ingest_bet(self):
        "Allows user to input a bet value"
        bet = remove(self.betvar.get(), "$,_ ")
        if not bet.isnumeric():                                 # check if bet contains non-numeric symbols
            if remove(bet,".").isnumeric():                     # check if bet is number with decimal
                messagebox.showerror(message="Bet must be whole dollar amount!")

            elif remove(bet,"-").isnumeric():                   # check if bet contains a minus sign
                messagebox.showerror(message="Bet must be positive!")

            else:                                               # if bet cannot be recognized as a number at all
                messagebox.showerror(message="Bet must be a number!")

        elif int(bet)<1:                                        # check if bet is zero
            messagebox.showerror(message="Bet must be greater than zero!")

        elif int(bet)>self.balance:                             # check if bet is greater than player balance
            messagebox.showerror(message=f'''You don't have enough money for that bet!
                                            \nYour balance: ${self.balance}
                                            \nYou tried to bet: ${bet}
                                            \nWin a few more rounds first...''')

        elif self.point and int(bet)>self.max_odds:             # check if odds bet is greater than allowed max
            messagebox.showerror(message=f"Odds bet is limited to ${self.max_odds}!")

        else:                                       # if bet is valid, continue
            return int(bet)

Bets()