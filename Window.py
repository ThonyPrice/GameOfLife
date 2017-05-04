# Authors: Thony Price, Niklas Lindqvist
# Last revision: 2017-04-28

# This file contains a class that initializes a tkinter window which
# are able to run the cellular simulation, Conway's Game of Life

import tkinter as tk
import saved_boards as gameplans
import CellClass
import time

# ControlBar acts as a container for Dropdown, run btn and speed slider.
class ControlBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.dropdown = Dropdown(self)
        self.runBtn = RunBtn(self)
        self.speedSlider = SpeedSlider(self)

        self.dropdown.pack(side='left')
        self.speedSlider.pack(side='left')
        self.runBtn.pack(side='left')

# The dropdown shows gameplans that the user can load into interface
class Dropdown(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tkvar = tk.StringVar()
        tkvar.set('--Select board--')
        boards = [x for x in gameplans.boards.keys()]
        option = tk.OptionMenu(self, tkvar, *boards,
            command=lambda var=tkvar.get():
                parent.parent.board.showBoard(gameplans.boards.get(var)))
        option.config(width=15)
        option.pack()

# Run simulation by clicking this button
# TODO: User should also be able to paus the simulation from here too.
class RunBtn(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.btn = tk.Button(
            self,
            text = 'Step',
            command = lambda: self.run()
        )
        self.btn.pack()

    def run(self):
        self.parent.parent.runGame()

# Let user decide on simulation speed.
class SpeedSlider(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text='Generations per second:').pack(side='left')
        self.scale = tk.Scale(self, from_=1, to=20, orient='horizontal')
        self.scale.set(1)
        self.scale.pack(side='left')

# Main class, this acts as a container for all other sub-frames in
#   tkinter. from here the steps of simulation are calculated as well.
class MainApplication(tk.Frame):
    def __init__(self, parent, cell_size):
        tk.Frame.__init__(self, parent)
        self.root = parent
        self.pack()
        self.controlBar = ControlBar(self)
        self.board = Board(self, cell_size)

        self.board.pack(side='top')
        self.controlBar.pack(side='top', fill="x")

    def runGame(self):
        listOfCells = self.createClasses(self.board.plan)
        row_sz = len(self.board.plan[0])
        col_sz = len(self.board.plan)
        while True:
            self.updateCells(listOfCells)
            plan = self.updateBoard(listOfCells, row_sz, col_sz)
            listOfCells = self.createClasses(plan)
            self.board.showBoard(plan)
            self.root.update()
            # self.root.after(1000, clock
            wait_time = 1/(self.controlBar.speedSlider.scale.get())
            time.sleep(wait_time)

    def createClasses(self, board):
        listCells = []
        for row in range(len(board)):
            for col in range(len(board[0])):
                listCells.append(CellClass.CellClass(int(board[row][col]), row , col,
                    self.getListNeighbourValue(row, col, board)))
        return listCells

    def getListNeighbourValue(self, row, col, board):
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

    def updateCells(self, listCells):
        for cell in listCells:
            cell.update()

    def updateBoard(self, listCells, row_sz, col_sz):
        ret_val = []
        i = 0
        for rows in range(col_sz):
            row = []
            for cell in listCells[i:i+row_sz]:
                row.append(cell.value)
            i += row_sz
            ret_val.append(row)
        return ret_val

# This class handles the visualization of the visualization of the game.
class Board(tk.Canvas):
    def __init__(self, parent, sz):
        tk.Canvas.__init__(self, parent,
            width=len(gameplans.blank[0])*sz+1,
            height=len(gameplans.blank)*sz+1,
            highlightthickness=0,
            bd=0,
            bg='grey'
        )
        self.sz = sz
        self.plan = gameplans.blank
        startboard = gameplans.blank
        self.showBoard(startboard)

    def resizeCanvas(self, bd):
        self.config(
            width=len(bd[0]) * self.sz + 1,
            height=len(bd) * self.sz + 1
        )
        print("tried resize...")

    def showBoard(self, bd):
        self.resizeCanvas(bd)
        sz = self.sz
        self.plan = bd
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
