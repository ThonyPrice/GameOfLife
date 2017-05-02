# Authors: Thony Price, Niklas Lindqvist
# Last revision: 2017-04-28

# This file contains a class that initializes a tkinter window which
# are able to run the cellular simulation, Conway's Game of Life

import tkinter as tk
import saved_boards as gameplans
import CellClass
import time

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

class RunBtn(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.btn = tk.Button(
            self,
            text = 'Run',
            command = lambda: self.run()
        )
        self.btn.pack()

    def run(self):
        print("Hej")
        parent.parent.runGame()

class SpeedSlider(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text='Generations per second:').pack(side='left')
        scale = tk.Scale(self, from_=1, to=20, orient='horizontal')
        scale.set(1)
        scale.pack(side='left')

class MainApplication(tk.Frame):
    def __init__(self, parent, cell_size):
        tk.Frame.__init__(self, parent)
        self.pack()
        tk.Label(self, text="MAIN APP").pack()
        self.controlBar = ControlBar(self)

        self.board = Board(self, gameplans.boards.get('Pulsar'), cell_size)

        self.board.pack(side='top')
        self.controlBar.pack(side='top', fill="x")

    def runGame(self):
        listOfCells = self.createClasses(self.board.plan)
        while True:
            self.board.showBoard(self.board.plan)
            self.updateCells(listOfCells)
            self.board.plan = updateBoard(listCells)
            listOfCells = self.creatClasses(self.board.plan)
            time.sleep(1)

    def createClasses(self):
        listCells = []
        for row in range(10):
            for col in range(10):
                listCells.append(CellClass(int(board[row][col]), row , col,
                    self.GetListNeighbourValue(row, col, board)))
        return listCells

    def GetListNeighbourValue(self, row, col, board):
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

    def updateBoard(self, listCells):
        ret_val = []
        i = 0
        for rows in range(10):
            row = []
            for cell in listCells[i:i+10]:
                row.append(cell.value)
            i += 10
            ret_val.append(row)
        return ret_val

def creatClasses(board):
    listCells = []
    for row in range(10):
        for col in range(10):
            listCells.append(CellClass(int(board[row][col]), row , col,
                GetListNeighbourValue(row, col, board)))
    return listCells

class Board(tk.Canvas):
    def __init__(self, parent, plan, sz):
        tk.Canvas.__init__(self, parent,
            width=len(plan[0])*sz+1,
            height=len(plan)*sz+1,
            highlightthickness=0,
            bd=0,
            bg='grey'
        )
        self.plan = None
        startboard = gameplans.blank
        self.pack()
        self.showBoard(startboard)

    def showBoard(self, bd):
        sz = 12
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
