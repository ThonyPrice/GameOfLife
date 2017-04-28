# Authors: Thony Price, Niklas Lindqvist
# Last revision: 2017-04-28

# This file handles the backend part of what's displayed in Window.py
# That is calculating which "cells" dies, lives on or dies each iteration
# of the simulation.

import Window
from CellClass import CellClass


def GetListNeighbourValue(x,y,board):
    ValueList = []
    for i in range(-1,2):
        for j in range(-1,2):
            try:
                ValueList.append(int(board[x+i][y+j]))
            except IndexError:
                    ValueList.append(0)

    return ValueList

def creatClasses(board):
    ListNeighbourValue = []
    listCells = []
    for x in range(10):
        for y in range(10):
            listCells.append(CellClass(int(board[x][y]), x ,y, GetListNeighbourValue(x,y,board)))

    return listCells

def updateCells(listCells):
    for cell in listCells:
        cell.update()


def main():
    size = 24
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
    listCells = creatClasses(board)
    win = Window.Window(board)
    win.mainloop()
    updateCells(listCells)



if __name__ == '__main__':
    main()
