# Authors: Thony Price, Niklas Lindqvist
# Last revision: 2017-04-28

# This file contains a class that initializes a tkinter window which
# are able to run the cellular simulation, Conway's Game of Life

import tkinter as tk

class Window(tk.Frame):
    def __init__(self, board, master=None):
        tk.Frame.__init__(self, master)
        sz = 12 
        # self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.canvas = tk.Canvas(self, width=len(board[0])*sz + 1, 
            height=len(board)*sz+1, highlightthickness=0, bd=0, bg='grey')
        self.quitButton = tk.Button(self, text='Quit',
            command=self.quit)

