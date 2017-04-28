# Authors: Thony Price, Niklas Lindqvist
# Last revision: 2017-04-28

# This file handles the backend part of what's displayed in Window.py
# That is calculating which "cells" dies, lives on or dies each iteration
# of the simulation.

import Window
from CellClass import CellClass


def GetListNeighbourValue(row, col, board):
    ValueList = []
    if row == 0 and col == 0:
        ValueList = [0,0,0,0]
        # Corner case
        for i in range(0,2):
            for j in range(0,2):
                ValueList.append(int(board[row+i][col+j]))
            ValueList.append(0)
        return ValueList[:9]
    if row == 0 and col!=0:
        # Skip looking up
        ValueList = [0,0,0]
        for i in range(0,2):
            for j in range(-1,2):
                try:
                    ValueList.append(int(board[row+i][col+j]))
                except IndexError:
                    ValueList.append(0)
        return ValueList
    if col == 0 and row != 0:
        # Skip looking left
        ValueList = [0]
        for i in range(-1,2):
            for j in range(0,2):
                try:
                    ValueList.append(int(board[row+i][col+j]))
                except IndexError:
                        ValueList.append(0)
            ValueList.append(0)
        return ValueList[:9]
    else:
        for i in range(-1,2):
            for j in range(-1,2):
                try:
                    ValueList.append(int(board[row+i][col+j]))
                except IndexError:
                    ValueList.append(0)
    return ValueList

def creatClasses(board):
    listCells = []
    for row in range(10):
        for col in range(10):
            listCells.append(CellClass(int(board[row][col]), row , col,
                GetListNeighbourValue(row, col, board)))
    return listCells

def updateCells(listCells):
    for cell in listCells:
        cell.update()

def updateBoard(listCells):
    ret_val = []
    i = 0
    for rows in range(10):
        row = []
        for cell in listCells[i:i+10]:
            row.append(cell.value)
        i += 10
        ret_val.append(row)

    return ret_val

def main():
    size = 24
    board = [
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,0,0,0],
        [0,0,0,1,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
    ]
    listCells = creatClasses(board)

    while True:
        win = Window.Window(board, size)
        win.mainloop()
        updateCells(listCells)
        board = updateBoard(listCells)
        listCells = creatClasses(board)
        # print(newBoard)
    print("---EOF---")



if __name__ == '__main__':
    main()
