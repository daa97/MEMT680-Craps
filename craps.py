from random import randint
from interface import *


class Dice:
    "Represents a set of dice"
    def __init__(self, count=2, sides=6):
        self.count = count      # number of dice which are rolled
        self.sides = sides      # number of sides per die
        self.total = count      # total value of dice roll
        self.each = [1]*count   # value of roll for each die
        self.dist = self.pmf()  # probability distribution of dice roll values

    def chance(self, value):
        "probability of rolling a given value"
        return self.dist[value]


    def pmf(self):
        "returns a probability mass function for dice results"
        p0 = [1]*self.sides                         # frequency of each dice roll for single die
        pnew = p0                                   # frequency of possible summed rolls for first die only
        for die in range(1,self.count):             # iterate through each die which is rolled
            pi = pnew                               # frequency for summed rolls of all previous dice
            pnew = [0]*(self.sides*(die+1)-die)     # initializes frequency for combination of all dice up to current
            for roll in range(len(pi)):             # for each possible summed value of previous rolls
                for nextroll in range(len(p0)):     # for each possible current roll
                    pnew[roll+nextroll] += pi[roll]*p0[nextroll]    # add expected frequency of dice roll combination
        pdict = dict()                              # dictionary of probability distribution
        for i in range(len(pnew)):                  # iterate over possible roll sum values
            pdict[i+self.count] = float(pnew[i]) / (self.sides**self.count)     # probability = frequency / total samples
        return pdict                                # returns dictionary containing pairs of (roll total):(probability)
    

    def roll(self):
        "Rolls dice and returns the total value of the roll"
        self.each = [randint(1,7) for i in range(self.count)]       # list of dice values
        self.total = sum(self.each)                                 # total value of roll
        return self.each                                            # return both die values individually

class Table(Dice):
    "Represents a craps table at which games take place"
    def __init__(self):
        super().__init__()                                          # instantiate associated dice
        self.point = 0                                              # start off with no point set

class Player(Table): 
    "Represents a single player at the table"
    def __init__(self):
        super().__init__()                                                      # instantiate associated table
        self.name = EntryBox("Please enter your name:").userval()               # get player name from input
        balance_box = EntryBox("Please enter the balance you want to gamble:",   
                        check_func=lambda s: remove(s,"$,0_ ").isnumeric())     # get user bankroll, ensure it is a whole nonzero dollar amount
        self.balance = int(remove(balance_box.userval(),"$,"))                  # convert bankroll string to an integer
        self.starting_balance = self.balance                                    # set starting balance to calculate overall winnings at end

class Bets(Player, App):
    "Represents bets belonging to a particular player"
    def __init__(self):
        Player.__init__(self)                               # instantiate associated player
        App.__init__(self)                                  # instantiate associated app
        self.title(f"{self.name} plays craps")              # add window title
        self.pass_bet = 0                                   # current wager on pass line
        self.no_pass_bet = 0                                # current wager on don't pass line
        self.odds_bet = 0                                   # current odds bet
        self.pass_odds = 0                                  # payout ratio for pass line odds bet
        self.max_odds = 0                                   # maximum allowable odds bet (dollar value)
        self.winnings = 0                                   # winnings from most recent roll
        
        # Associate buttons with respective functions
        self.pass_button.config(command=self.pass_line)     # call pass_line method on button click
        self.no_pass_button.config(command=self.do_not_pass)# call do_not_pass method on button click
        self.odds_button.config(command=self.odds)          # call odds method on button click
        self.roll_button.config(command=self.shooter)       # call shooter method on button click
        self.quit_button.config(command=self.on_close)      # call on_close method on button click
        self.protocol("WM_DELETE_WINDOW", self.on_close)    # call on_close method when user attempts to "X" out of window

        self.update_view()                                  # set label values correctly
        self.mainloop()                                     # start window
    
    def pass_line(self):
        "allows a pass line bet to be made"
        if not self.point:                      # check that no point has been set
            userval = self.ingest_bet()         # get bet
            if userval is not None:             # ensure valid bet was made
                self.pass_bet += userval        # add user defined bet to current bet
                self.balance -= userval         # subtract user defined bet from balance
                self.shooter()                  # roll dice and evaluate

    def do_not_pass(self):
        "allows a dont pass bet to be made"
        if not self.point:                      # check that no point has been set
            userval = self.ingest_bet()         # get bet
            if userval is not None:             # ensure valid bet was made
                self.no_pass_bet += userval     # add user defined bet to current bet
                self.balance -= userval         # subtract user defined bet from balance
                self.shooter()                  # roll dice and evaluate

    def odds(self):
        "allows an odds bet to be made"
        if self.point:                          # check that point has been set
            userval = self.ingest_bet()         # get bet
            if userval is not None:             # ensure valid bet was made
                self.odds_bet += userval        # add user defined bet to current bet
                self.balance -= userval         # subtract user defined bet from balance
                self.shooter()                  # roll dice and evaluate

    def shooter(self) -> None:
        "rolls dice and evaluates payout"
        self.winnings = 0                       # set winnings from current roll
        net_pass = self.pass_bet - self.no_pass_bet     # net bet on pass line
        if self.any_bet():                      # if a bet has been placed
            val = sum(self.roll())              # get current dice roll
            if not self.point:                  # if no point is set
                if val==7 or val==11:           # on 7 or 11, pass wins, dont pass loses
                    self.winnings = net_pass
                elif val==2  or val==3:         # on 2 or 3, pass loses, dont pass wins
                    self.winnings = -net_pass
                elif val==12:                   # on 12, pass loses, dont pass ties
                    self.winnings = -self.pass_bet
                else:                           # on other rolls, set point
                    self.point = val            # set point
                    self.max_odds = (6 - abs(7-val)) *  max(self.pass_bet, self.no_pass_bet)    # set maximum odds bet in dollars
                
                if not self.point:              # if no point was set, update balance with payout
                    self.payout()
                self.update_view()
            
            else:                   # if point is set
                # determine pass line odds bet payout ratios from point
                if self.point==4 or self.point==10:
                    self.pass_odds = 2.
                elif self.point==5 or self.point==9:
                    self.pass_odds = 3/2.
                elif self.point==6 or self.point==8:
                    self.pass_odds = 6/5.

                # evaluate pass line and odds bet payouts
                if self.total==7:                   # pass line loses, dont pass wins
                    if net_pass>0:                  # taking odds (pass) loses
                        self.winnings = - net_pass - self.odds_bet
                    else:                           # laying odds (dont pass) wins
                        self.winnings = - net_pass + self.odds_bet / self.pass_odds
                    self.payout()

                elif self.total == self.point:      # pass line wins, dont pass loses
                    if net_pass>0:                  # taking odds (pass) wins
                        self.winnings = net_pass + self.odds_bet * self.pass_odds
                    else:                           # laying odds (dont pass) loses
                        self.winnings = net_pass - self.odds_bet
                    self.payout()
                self.update_view() 
    
    def payout(self) -> None:
        "update balance, reset point, and clear existing bets if needed"
        self.balance += self.winnings               # add winnings to balance
        self.point = 0                              # reset point
        if self.odds_bet != 0 or self.winnings<=0:  # if money was lost/tied or odds bet was placed
            # return bets to original balance and clear them from the table
            self.balance += self.pass_bet + self.no_pass_bet + self.odds_bet   # add bets back to bankroll
            self.pass_bet = 0                       # clear pass bet
            self.no_pass_bet = 0                    # clear dont pass bet
            self.odds_bet = 0                       # clear odds bet
        self.max_odds = 0                           # reset maximum allowable odds bet
        self.pass_odds = 0                          # reset the odds payout ratio for pass line bet

    def any_bet(self) -> bool:
        "Checks if any bet is currently on the table"
        return max(self.pass_bet, self.no_pass_bet, self.odds_bet) != 0
    
    def update_view(self) -> None:
        "Updates GUI view and options based on current status"
        self.betvar.set("")
        on = lambda tf: [("!" if tf else "") + "disabled"]      # translates boolean T/F into enabled/disabled status for tk widgets
        self.pass_button.state(on(not self.point))              # pass line bet only enabled during come-out
        self.no_pass_button.state(on(not self.point))           # dont pass bet only enabled during come-out
        self.odds_button.state(on(self.point))                  # odds bet only enabled during point phase
        self.roll_button.state(on(self.any_bet()))              # can only roll w/out betting if bet is already placed
        self.quit_button.state(on(not self.any_bet()))          # quit button only enabled when no bets are on the table
        
        self.die[0]['image'] = self.die_images[self.each[0] - 1]    # update first die with image of roll
        self.die[1]['image'] = self.die_images[self.each[1] - 1]    # update second die with image of roll  

        if self.winnings > 0:                                       # if last roll won money, display winnings
            self.labels['win'].config(text=f"You won ${self.winnings:,.2f}!")
            self.win_anim()                                     # play a celebratory animated graphic upon win
        elif self.winnings < 0:                                 # if last roll lost money, display losses
            self.labels['win'].config(text=f"You lost ${-self.winnings:,.2f}!")
        else:                                                   # if no money was won or lost
            self.labels['win'].config(text=f"")
        self.labels['balance'].config(text=f"Balance: ${self.balance:,.2f}")

        # Add pass line bet value
        if self.no_pass_bet != 0:
            self.labels['bet'].config(text=f"Do Not Pass Bet: ${self.no_pass_bet:,}")
        else:
            self.labels['bet'].config(text=f"Pass Line Bet: ${self.pass_bet:,}")

        # Add labels containing current point, odds bet, and maximum possible odds bet
        if self.point:
            self.labels['odds'].configure(text=f"Odds Bet: ${self.odds_bet:,} (Max ${self.max_odds:,})")
            self.labels['point'].configure(text=f"Point: {self.point}")
        else:
            self.labels['odds'].configure(text="")
            self.labels['point'].configure(text="No Point Set")

    def on_close(self) -> None:
        "Determine if the game can be ended, and if so, display winnings"
        if self.any_bet():                                                  # if there is an active bet, dont allow quitting
            messagebox.showerror(title="Not so soon", message="You still have bets on the table!")
        else:                                                               # if no bets are on the table
            net = self.balance - self.starting_balance                      # net earnings of player
            status = "won" if net>=0 else "lost"                            # text of overall status of player
            walk = messagebox.askyesno(title="Exit Game",                   # display winnings and double-check intention to quit
                    message=f'''Are you sure you want to quit playing?
                                You {status} ${abs(net):,.2f} in total.''')
            if walk:                                                        # player chose to quit
                self.destroy()                                              # close window
    
    def ingest_bet(self):
        "Allows user to input a bet value"
        errbox = lambda msg: messagebox.showerror(title="Aw Crap!", message=msg)
        bet = remove(self.betvar.get(), "$,_ ")
        if not bet.isnumeric():                                 # check if bet contains non-numeric symbols
            if remove(bet,".").isnumeric():                     # check if bet is number with decimal
                errbox("Bet must be whole (integer) dollar amount!")

            elif remove(bet,"-").isnumeric():                   # check if bet contains a minus sign
                errbox("Bet must be positive!")

            else:                                               # if bet cannot be recognized as a number at all
                errbox("Bet must be a number!")

        elif int(bet)<1:                                        # check if bet is zero
            errbox("Bet must be greater than zero!")

        elif int(bet)>self.balance:                             # check if bet is greater than player balance
            errbox(f'''You don't have enough money for that bet!
                        Your balance: ${self.balance}
                        You tried to bet: ${bet}
                        Win a few more rounds first...''')

        elif self.point and (int(bet)+self.odds_bet)>self.max_odds:     # check if total odds bet is greater than allowed max
            errbox(f"Odds bet is limited to ${self.max_odds}!")

        else:                                       # if bet is valid, continue
            return int(bet)

if __name__=="__main__":
    Bets()