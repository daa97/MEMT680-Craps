import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def remove(string, chars):
    return "".join([c for c in filter(lambda x: not x in chars, string)])



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.labelbox = ttk.Frame(self)
        self.labels = dict()
        self.labels['title'] =  ttk.Label(self.labelbox,text=f"Craps", font=("bold 16"))
        self.labels['balance'] = ttk.Label(self.labelbox,text=f"Balance: $0")
        self.labels['bet'] = ttk.Label(self.labelbox,text="Current Bet: $0")
        self.labels['point'] = ttk.Label(self.labelbox, text="Point: None")
        self.betvar = tk.StringVar(value="")
        self.boxlabel = ttk.Label(self, text="Enter bet:  $")
        self.betbox = ttk.Entry(self,textvariable=self.betvar, width=9)
        
        # create frame containing images of two dice
        self.dice = ttk.Frame(self)
        self.die_images = [tk.PhotoImage(file=f"resources\\die_{i+1}.ppm") for i in range(6)]
        self.die = [ttk.Label(self.dice, image=self.die_images[0]), ttk.Label(self.dice, image=self.die_images[0])] 
        self.die[0].grid(row=0, column=0)
        self.die[1].grid(row=0, column=1)
        self.odds_button = ttk.Button(self, text="Odds Bet")        # button to make odds bet
        self.pass_button = ttk.Button(self, text="Pass")            # button to make pass bet
        self.no_pass_button = ttk.Button(self, text="Do Not Pass")  # button to make do not pass bet
        self.roll_button = ttk.Button(self, text="Just Roll")       # button to roll without a bet
        self.quit_button = ttk.Button(self,text="Quit Game")        # button to quit game
        
        # place all widgets in appropriate locations within window
        
        
        self.labels['title'].grid(row=0,column=0)
        self.labels["balance"].grid(row=2, column=0)
        self.labels["bet"].grid(row=3, column=0)
        self.labels["point"].grid(row=4, column=0)

        self.labelbox.grid(row=0,column=1, columnspan=2, padx=50)
        self.dice.grid(row=1,column=1, columnspan=2)
        self.boxlabel.grid(row=4, column=1, sticky="e")
        self.betbox.grid(row=4,column=2, pady=5, sticky="w")
        self.pass_button.grid(row=5, column=1)
        self.no_pass_button.grid(row=5, column=2)
        self.odds_button.grid(row=6,column=1)
        self.roll_button.grid(row=6, column=2)
        self.quit_button.grid(row=7,column=1,columnspan=2,pady=8)
        self.columnconfigure(0, minsize=80, weight=1)
        self.columnconfigure(3, minsize=80, weight=1)

        
    def clear_entry(self):
        self.betvar.set("")
        


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

                
