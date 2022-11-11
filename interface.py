import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def remove(string, chars):
    return "".join([c for c in filter(lambda x: not x in chars, string)])



class App(tk.Tk):
    def __init__(self, bets):
        super().__init__()
        self.bets = bets                    # associated player bets
        self.title(f"{self.bets.name} plays craps")
        self.balancelabel = ttk.Label(self,text=f"Balance: ${self.bets.balance}")
        self.betlabel = ttk.Label(self,text="Current Bet: $0")
        self.betvar = tk.StringVar(value="0")
        self.betbox = ttk.Entry(self,textvariable=self.betvar)

        # create frame containing images of two dice
        self.dice = ttk.Frame(self)
        self.die_images = [tk.PhotoImage(file=f"resources\\die_{i+1}.ppm") for i in range(6)]
        self.die1 = ttk.Label(self.dice, image=self.die_images[0])
        self.die2 = ttk.Label(self.dice, image=self.die_images[0])
        self.die1.grid(row=0, column=0)
        self.die2.grid(row=0, column=1)

        self.pass_button = ttk.Button(self, text="Pass", command=lambda: self.ingest_bet( pass_=True))
        self.no_pass_button = ttk.Button(self, text="Do Not Pass", command=lambda: self.ingest_bet( pass_=False))
        self.roll_button = ttk.Button(self, text="Start Roll", command=self.shoot)
        

        # place all widgets in appropriate locations within window
        self.dice.grid(row=0,column=0, columnspan=2)
        self.balancelabel.grid(row=1, column=0)
        self.betlabel.grid(row=1, column=1)
        self.betbox.grid(row=2,column=1)
        self.pass_button.grid(row=3, column=0)
        self.no_pass_button.grid(row=3, column=1)
        self.roll_button.grid()
        
        self.mainloop()

    def ingest_bet(self, pass_):
        bet = remove(self.betvar.get(), "$,_ ")
        if not bet.isnumeric():                     # check if bet contains non-numeric symbols
            if remove(bet,".").isnumeric():         # check if bet is number with decimal
                messagebox.showerror(message="Bet must be whole dollar amount!")
            elif remove(bet,"-").isnumeric():       # check if bet is a negative number
                messagebox.showerror(message="Bet must be positive!")
            else:                                   # if bet is not a number at all
                messagebox.showerror(message="Bet must be a number!")
        elif int(bet)<1:                            # check if bet is zero
            messagebox.showerror(message="Bet must be greater than zero!")
        elif int(bet)>self.bets.balance:            # check if bet is greater than player balance
            messagebox.showerror(message=f'''You don't have enough money for that bet!
                                            \nYour balance: ${self.bets.balance}
                                            \nYou tried to bet: ${bet}
                                            \nWin a few more rounds first...''')

        else:                                       # if bet is valid
            if pass_:                               # bet pass line
                self.bets.pass_line(int(bet))
            else:                                   # bet do not pass line
                self.bets.do_not_pass(int(bet))
            self.shoot()
        

    def shoot(self):
        a = self.bets.shooter()
        rolls = self.bets.roll()
        print(rolls)
        self.die1['image'] = self.die_images[rolls[0] - 1]
        self.die2['image'] = self.die_images[rolls[1] - 1]


class EntryBox(tk.Tk):
    def __init__(self, message, check_func=None):
        super().__init__()
        self.title("Enter a value")
        redtext = ttk.Style()
        redtext.configure("redtext.TLabel", foreground="red") 
        self.check_func = check_func

        self.label = ttk.Label(self, text=message)
        self.errlabel = ttk.Label(self, text="", style="redtext.TLabel")
        self.var = tk.StringVar()
        self.box = ttk.Entry(self, textvariable=self.var)
        self.box.bind("<Return>", self.okay)
        self.button = ttk.Button(self,text="OK", command=self.okay)
        self.label.grid(row=0,column=0)
        self.box.grid(row=1,column=0)
        self.errlabel.grid(row=2, column=0)
        self.button.grid(row=3,column=0)
        self.mainloop()

    def userval(self):
        return self.var.get()

    def okay(self, event=None):
        if self.check_func is not None:
            if not self.check_func(self.var.get()):
                self.errlabel['text']="Invalid Entry!"
                
                return
        self.destroy()

                
