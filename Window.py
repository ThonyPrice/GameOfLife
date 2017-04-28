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
        self.showBoard(board, sz)
        print("---EndOfClass---")

    def showBoard(self, bd, sz):
        self.delete(tk.ALL)
        cols = len(bd[0])
        rows = len(bd)
        for x in range(cols):
            for y in range(rows):
                rect = (x*sz, y*sz, (x+1)*sz, (y+1)*sz)
                if bd[y][x] == 1:
                    self.create_rectangle(rect, outline="black", fill="orange")
                else:
                    self.create_rectangle(rect, outline="black")
        print("---EndOfShowBoard")
