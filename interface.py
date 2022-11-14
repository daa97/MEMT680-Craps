import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def remove(string, chars):
    return "".join([c for c in filter(lambda x: not x in chars, string)])



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.minsize(width=380, height=310)
        self.left = ttk.Label(self)
        self.right = ttk.Label(self)
        self.labelbox = ttk.Frame(self)
        self.labels = dict()
        self.labels['title'] =  ttk.Label(self.labelbox,text=f"Craps", font="bold 16")
        self.labels['balance'] = ttk.Label(self.labelbox,text=f"Balance: $0")
        self.labels['win'] = ttk.Label(self.labelbox,text=f"")
        self.labels['bet'] = ttk.Label(self.labelbox,text="Current Bet: $0")
        self.labels['point'] = ttk.Label(self.labelbox, text="No Point Set")

        self.betvar = tk.StringVar(value="")
        self.boxlabel = ttk.Label(self, text="Enter bet:  $")
        self.betbox = ttk.Entry(self,textvariable=self.betvar, width=9)
        self.anim = 0
        # create frame containing images of two dice
        self.die_images = [tk.PhotoImage(file=f"resources\\die_{i+1}.ppm") for i in range(6)]
        self.balloon_images = [tk.PhotoImage(file=f"resources\\f{i+1}.ppm") for i in range(15)]
        self.dice = ttk.Frame(self)
        self.die = [ttk.Label(self.dice, image=self.die_images[0]), ttk.Label(self.dice, image=self.die_images[0])] 
        self.die[0].grid(row=0, column=0, padx=5, pady=5)
        self.die[1].grid(row=0, column=1, padx=5, pady=5)
        # create buttons
        self.odds_button = ttk.Button(self, text="Odds Bet")        # button to make odds bet
        self.pass_button = ttk.Button(self, text="Pass")            # button to make pass bet
        self.no_pass_button = ttk.Button(self, text="Do Not Pass")  # button to make do not pass bet
        self.roll_button = ttk.Button(self, text="Just Roll")       # button to roll without a bet
        self.quit_button = ttk.Button(self,text="Walk Away")        # button to quit game
        
        # ******** Place Widgets ************* 
        # place labels at top   
        self.labels['title'].grid(row=0,column=0, pady=5)           # place title 'Craps'
        self.labels["balance"].grid(row=1, column=0)                # place bankroll label
        self.labels['win'].grid(row=2,column=0)                     # place winnings label
        self.labels["bet"].grid(row=3, column=0)                    # place bet label
        self.labels["point"].grid(row=4, column=0)                  # place point label

        # place 
        self.left.grid(row=0,column=0, rowspan=9, sticky="n")       # place left margin graphics
        self.right.grid(row=0,column=3, rowspan=9, sticky="n")      # place right margin graphics
        self.labelbox.grid(row=0,column=1, columnspan=2)            # place all labels at top
        self.dice.grid(row=1,column=1, columnspan=2, padx=40)       # place dice graphics in middle
        self.boxlabel.grid(row=4, column=1, sticky="e")             # place label with prompt for bet entry
        self.betbox.grid(row=4,column=2, pady=5, sticky="w")        # place bet entry box
        self.pass_button.grid(row=5, column=1)                      # place pass line bet button
        self.no_pass_button.grid(row=5, column=2)                   # place dont pass bet button
        self.odds_button.grid(row=6,column=1)                       # place odds bet button
        self.roll_button.grid(row=6, column=2)                      # place button to roll without betting
        self.quit_button.grid(row=7,column=1,columnspan=2,pady=10)  # place button to quit game
        self.columnconfigure(0, minsize=80, weight=1)               # set left margin to auto-scale with window
        self.columnconfigure(3, minsize=80, weight=1)               # set right margin to auto-scale with window

        
    def clear_entry(self):
        self.betvar.set("")
    
    def win_anim(self):
        "plays an animation upon winning a bet"
        self.left.config(image=self.balloon_images[self.anim])
        self.right.config(image=self.balloon_images[self.anim])
        self.anim = (self.anim + 1) % len(self.balloon_images)
        if self.anim!=0:
            self.after(100,self.win_anim)
        else:
            self.left.config(image="")
            self.right.config(image="")

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
        self.label.grid(row=0,column=0, padx=15)
        self.box.grid(row=1,column=0, padx=15)
        self.errlabel.grid(row=2, column=0)
        self.button.grid(row=3,column=0, pady=15)
        self.mainloop()

    def userval(self):
        return self.var.get()
        
    def okay(self, event=None):
        if self.check_func is not None:
            if not self.check_func(self.var.get()):
                self.errlabel['text']="Invalid Entry!"
                return
        self.destroy()

                
