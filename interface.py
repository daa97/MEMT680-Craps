import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def remove(string, chars):
    return "".join([c for c in filter(lambda x: not x in chars, string)])



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.labelbox = ttk.Frame()
        self.labels = dict()
        self.labels['title'] =  ttk.Label(self.labelbox,text=f"Craps", font=("bold 16"))
        self.labels['balance'] = ttk.Label(self.labelbox,text=f"Balance: $0")
        self.labels['bet'] = ttk.Label(self.labelbox,text="Current Bet: $0")
        self.labels['point'] = ttk.Label(self.labelbox, text="Point: None")
        
        self.betvar = tk.StringVar(value="0")
        self.betbox = ttk.Entry(self,textvariable=self.betvar)

        # create frame containing images of two dice
        self.dice = ttk.Frame(self)
        self.die_images = [tk.PhotoImage(file=f"resources\\die_{i+1}.ppm") for i in range(6)]
        self.die = [ttk.Label(self.dice, image=self.die_images[0]), ttk.Label(self.dice, image=self.die_images[0])] 
        self.die[0].grid(row=0, column=0)
        self.die[1].grid(row=0, column=1)

        self.pass_button = ttk.Button(self, text="Pass")
        self.no_pass_button = ttk.Button(self, text="Do Not Pass")
        self.roll_button = ttk.Button(self, text="Start Roll")
        
        # place all widgets in appropriate locations within window
        self.labels['title'].grid(row=0,column=0)
        self.dice.grid(row=1,column=0, columnspan=2)
        
        self.labels["balance"].grid(row=3, column=0)
        self.labels["bet"].grid(row=3, column=1)
        self.labelbox.grid(row=0,column=0)
        self.betbox.grid(row=4,column=1)
        self.pass_button.grid(row=5, column=0)
        self.no_pass_button.grid(row=5, column=1)
        self.roll_button.grid(row=6, column=0)
        

    def update_view(self, roll, balance, point):
        self.die[0]['image'] = self.die_images[roll[0] - 1]
        self.die[1]['image'] = self.die_images[roll[1] - 1]
        self.labels['balance'].configure(text=f"Balance: ${balance}")
        self.labels


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

                
