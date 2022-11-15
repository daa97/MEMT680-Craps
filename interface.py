import tkinter as tk
from tkinter import messagebox, ttk

def remove(string, chars):
    "filters out specified characters from provided string"
    return "".join([c for c in filter(lambda x: not x in chars, string)])


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.minsize(width=380, height=310)     # minimum window size allowed
        self.left = ttk.Label(self)             # placeholder for left margin graphics
        self.right = ttk.Label(self)            # placeholder for right margin graphics

        # add in several labels which explain status of the game and are updated frequently
        self.labelbox = ttk.Frame(self)                                                         # frame containing these labels within the window
        self.labels = dict()                                                                    # dictionary of labels
        self.labels['title'] =  ttk.Label(self.labelbox,text=f"Craps", font="bold 14")          # name of the game
        self.labels['balance'] = ttk.Label(self.labelbox,text=f"Balance: $0")                   # player cash balance indicator
        self.labels['win'] = ttk.Label(self.labelbox,text=f"")                                  # win status indicator
        self.labels['bet'] = ttk.Label(self.labelbox,text=f"Pass Line Bet: $0")                 # pass/dont pass bet indicator
        self.labels['odds'] = ttk.Label(self.labelbox,text="")                                  # odds bet indicator
        self.labels['point'] = ttk.Label(self.labelbox, text="No Point Set")                    # point indicator

        self.betvar = tk.StringVar(value="")                                                    # variable containing user-entered bet value
        self.boxlabel = ttk.Label(self, text="Enter bet:  $")                                   # prompt for user to enter bet
        self.betbox = ttk.Entry(self,textvariable=self.betvar, width=9)                         # entry box for user to enter bet
        self.anim_frame = 0                                                                     # tracks current frame number of win animation
        self.balloon_images = [tk.PhotoImage(file=f"resources\\f{i+1}.ppm") for i in range(15)] # frames for win animation

        # create frame containing images of two dice
        self.die_images = [tk.PhotoImage(file=f"resources\\die_{i+1}.ppm") for i in range(6)]   # list of possible die images for each roll value
        self.dice = ttk.Frame(self)                                     # frame containing die image graphics    
        self.die = [ttk.Label(self.dice, image=self.die_images[0]),
                     ttk.Label(self.dice, image=self.die_images[0])]    # list with die image graphics
        self.die[0].grid(row=0, column=0, padx=5, pady=2)               # place first image
        self.die[1].grid(row=0, column=1, padx=5, pady=2)               # place second image
        
        # create buttons
        self.odds_button = ttk.Button(self, text="Odds Bet")        # button to make odds bet
        self.pass_button = ttk.Button(self, text="Pass")            # button to make pass bet
        self.no_pass_button = ttk.Button(self, text="Do Not Pass")  # button to make do not pass bet
        self.roll_button = ttk.Button(self, text="Just Roll")       # button to roll without a bet
        self.quit_button = ttk.Button(self,text="Walk Away")        # button to quit game
        
        # ******** Place Widgets ************* 
        # place labels at top   
        self.labels['title'].grid(row=0,column=0, pady=3)           # place title 'Craps'
        self.labels["balance"].grid(row=1, column=0)                # place bankroll label
        self.labels['win'].grid(row=2,column=0)                     # place winnings label
        self.labels["bet"].grid(row=3, column=0)                    # place pass bet label
        self.labels["odds"].grid(row=4,column=0)                    # place odds bet label
        self.labels["point"].grid(row=5, column=0)                  # place point label

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

        
    def clear_entry(self)-> None:
        "clears bet entry"
        self.betvar.set("")
    
    def win_anim(self) -> None:
        "plays an animation upon winning a bet"
        self.left.config(image=self.balloon_images[self.anim_frame])        # set image frame in left margin of window
        self.right.config(image=self.balloon_images[self.anim_frame])       # set image frame in right margin of window
        self.anim_frame = (self.anim_frame + 1) % len(self.balloon_images)  # increment frame number
        if self.anim_frame!=0:                                              # if animation has not reached ending point
            self.after(100,self.win_anim)                                   # callback for next frame to update in 0.1 seconds
        else:                                                               # if animation is complete
            self.left.config(image="")                                      # clear image in left margin
            self.right.config(image="")                                     # clear image in right margin

class EntryBox(tk.Tk):
    "window which takes in a string from the user"
    def __init__(self, message, check_func=None):
        super().__init__()                                      # initialize as a Tk window
        self.title("Enter a value")                             # set heading at top of window
        redtext = ttk.Style()                                   # custom text style
        redtext.configure("redtext.TLabel", foreground="red")   # make custom text style appear red
        self.check_func = check_func                            # optional function to check whether user-entered string is valid
        self.label = ttk.Label(self, text=message)              # label with prompt for user to respond to
        self.errlabel = ttk.Label(self, text="", style="redtext.TLabel")    # label which will inform user of invalid entries
        self.var = tk.StringVar()                               # variable containing user-entered string
        self.box = ttk.Entry(self, textvariable=self.var)       # box allowing user to enter string
        self.box.bind("<Return>", self.okay)                    # continue upon pressing Enter key
        self.button = ttk.Button(self,text="OK", command=self.okay)

        # place widgets within window
        self.label.grid(row=0,column=0, padx=15)                # place prompt label
        self.box.grid(row=1,column=0, padx=15)                  # place entry box
        self.errlabel.grid(row=2, column=0)                     # place error label for invalid inputs
        self.button.grid(row=3,column=0, pady=15)               # place OK button
        self.protocol("WM_DELETE_WINDOW", lambda: quit(1))      # quit game with error if window is closed
        self.mainloop()                                         # display window


    def userval(self) -> str:
        "returns string value from user"
        return self.var.get()
        
    def okay(self, event=None):
        "close window if user entry is determined to be valid, otherwise raise error"
        if self.check_func is not None:                 # if validation function is set
            if not self.check_func(self.var.get()):     # if user input fails validation check
                self.errlabel['text']="Invalid Entry!"  # display error message
                return                                  # exit function and keep window open

        self.destroy()                                  # otherwise, close window

                
