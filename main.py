# Authors: Thony Price, Niklas Lindqvist
# Last revision: 2017-04-28

# This file handles the backend part of what's displayed in Window.py
# That is calculating which "cells" dies, lives on or dies each iteration
# of the simulation. 

import Window

def main():
    board = [
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,1,1,0,0,0,0,0,0,0,0],
        [0,1,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,1,1,1,0,0],
        [0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,0],
        [0,0,0,0,0,0,0,0,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,0],
    ]
    win = Window.Window(board)
    win.mainloop()

if __name__ == '__main__':
    main()
