import tkinter as tk
from tkinter import ttk



class App(tk.Tk):
    def __init__(self, bets):
        super().__init__()
        self.bets = bets
        self.balancelabel = ttk.Label(self,text=f"Balance: ${self.bets.balance}")
        self.betlabel = ttk.Label(self,text="Last Bet: $0")
        
        self.betvar = tk.StringVar(value="0")
        self.betbox = ttk.Entry(self,textvariable=self.betvar)
        self.dice = ttk.Frame(self)
        self.die_images = [tk.PhotoImage(file=f"resources\\die_{i+1}.ppm") for i in range(6)]
        self.die1 = ttk.Label(self.dice, image=self.die_images[0])
        self.die2 = ttk.Label(self.dice, image=self.die_images[0])
        self.die1.grid(row=0, column=0)
        self.die2.grid(row=0, column=1)

        self.roll_button = ttk.Button(self, text="Start Roll", command=self.roll_dice)

        self.dice.grid(row=0,column=0, columnspan=2)
        self.balancelabel.grid(row=1, column=0)
        self.betlabel.grid(row=1, column=1)
        self.betbox.grid(row=2,column=1)
        self.roll_button.grid(row=3, column=0)
        
        self.mainloop()
    

    def roll_dice(self):
        rolls = self.bets.roll()
        print(rolls)
        self.die1['image'] = self.die_images[rolls[0] - 1]
        self.die2['image'] = self.die_images[rolls[1]- 1]


class EntryBox(tk.Tk):
    def __init__(self, message, check_func=None):
        super().__init__()
        self.check_func = check_func

        self.label = ttk.Label(self, text=message)
        self.errlabel = ttk.Label(self, text="")
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

                
