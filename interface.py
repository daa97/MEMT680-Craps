import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self, player, table):
        super().__init__()
        self.dice = ttk.Frame(self)
        self.dice.grid(row=0,column=0)
        self.die_images = [tk.PhotoImage(file=f"resources\\die_{i+1}.ppm") for i in range(6)]
        self.die1 = ttk.Label(self.dice, image=self.die_images[0])
        self.die2 = ttk.Label(self.dice, image=self.die_images[0])
        self.die1.grid(row=0, column=0)
        self.die2.grid(row=0, column=1)
        self.roll_button = ttk.Button(self, text="Start Roll", command=table.roll_dice)
        self.roll_button.grid(row=1, column=0)

        self.mainloop()

    def update_dice(self, roll1, roll2):
        self.die1['image'] = self.die_images[roll1 - 1]
        self.die2['image'] = self.die_images[roll2- 1]



        
App()