# Authors: Thony Price, Niklas Lindqvist
# Last revision: 2017-04-28

# This file contains a class that initializes a tkinter window which
# are able to run the cellular simulation, Conway's Game of Life

import tkinter as tk

class Window(tk.Canvas):
    def __init__(self, board, sz, master=None):
        tk.Canvas.__init__( self, 
                            width=len(board[0])*sz+1, 
                            height=len(board)*sz+1, 
                            highlightthickness=0, 
                            bd=0, 
                            bg='grey'
        )
        self.pack()
        # self.showBoard(board, size)
        print("---EOC---")

    