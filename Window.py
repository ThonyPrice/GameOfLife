# Authors: Thony Price, Niklas Lindqvist
# Last revision: 2017-04-28

# This file contains a class that initializes a tkinter window which
# are able to run the cellular simulation, Conway's Game of Life

import tkinter as tk
import saved_boards as gameplans
import CellClass
import time
import webbrowser

# ControlBar acts as a container for Dropdown, run btn and speed slider.
class ControlBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.dropdown = Dropdown(self)
        self.btns = Btns(self)
        self.speedSlider = SpeedSlider(self)

        self.dropdown.pack(side='left')
        self.speedSlider.pack(side='left')
        self.btns.pack(side='left')

# The dropdown shows gameplans that the user can load into interface
class Dropdown(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        tkvar = tk.StringVar()
        tkvar.set('--Select board--')
        boards = [x for x in gameplans.boards.keys()]
        option = tk.OptionMenu(self, tkvar, *boards,
            command=lambda var=tkvar.get():
                self.resizeAndStart(gameplans.boards.get(var)))
        option.config(width=15)
        option.pack()

    def resizeAndStart(self, bd):
        tmp = sum([x for xs in bd for x in xs])
        self.parent.parent.genInfo.alive_lbl.configure(
            text='Population: %s' % str(tmp)
        )
        tmp = self.parent.parent.genInfo.gens = 0
        self.parent.parent.genInfo.gen_lbl.configure(
            text='Generations: %s' % str(tmp)
        )
        self.parent.btns.state = False
        self.parent.parent.board.resizeCanvas(bd)
        self.parent.parent.board.showBoard(bd)

# Run simulation by clicking this button
# TODO: User should also be able to paus the simulation from here too.
class Btns(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.state = False
        self.run_btn = tk.Button(
            self,
            text = 'Run',
            command = lambda: self.run()
        ).pack(side='left')
        self.stop_btn = tk.Button(
            self,
            text = 'Stop',
            command = lambda: self.stop()
        ).pack(side='left')
        self.quit_btn = tk.Button(
            self,
            text = 'Quit',
            command = lambda: self.quit()
        ).pack(side='left')

    def run(self):
        self.state = True
        self.parent.parent.runGame()

    def stop(self):
        self.state = False

# Let user decide on simulation speed.
class SpeedSlider(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text='Generations per second:').pack(side='left')
        self.scale = tk.Scale(self, from_=1, to=20, orient='horizontal')
        self.scale.set(1)
        self.scale.pack(side='left')

class Info(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        head = tk.Label(self, text='\nAbout this game\n')
        head.config(font=("Courier", 16))
        head.pack()
        text = tk.Label(self,
            text =
'Each grid in the cell represents a cell in one of two\n\
possible states, alive or dead. Every cell interacts\n\
with its eight neighbours and at each step in time,\n\
the following transitions occur:\n\n\
    # Any live cell with fewer than two live\n\
        neighbours dies, as if caused by underpopulation.\n\
    # Any live cell with two or three live neighbours\n\
        lives on to the next generation.\n\
    # Any live cell with more than three live\n\
        neighbours dies, as if by overpopulation.\n\
    # Any dead cell with exactly three live neighbours\n\
        becomes a live cell, as if by reproduction.\n\n\
By these simple rules complex patterns as well as\n\
self organization may arise. For more on the topic: \
')
        text.config(font=("Courier", 12))
        text.pack(anchor='w')
        link = tk.Label(self, text='Wikipedia\n', fg='blue', cursor='hand2')
        link.config(font=("Courier", 12))
        link.pack()
        link.bind("<Button-1>", self.browse)

    def browse(self, event=None):
        webbrowser.open_new(r"https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life")

class GenereationInfo(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='#1b1b1b', bd=2)
        self.gens = 0
        self.alive = 0
        self.gen_lbl = tk.Label(self, text='Generations: %s' % str(self.gens))
        self.gen_lbl.config(bg='#1b1b1b', fg="white")
        self.alive_lbl = tk.Label(self, text='Population: %s' % str(self.alive))
        self.alive_lbl.config(bg='#1b1b1b', fg="white", padx=3)
        self.gen_lbl.pack(side='left')
        self.alive_lbl.pack(side='left', padx=30)

# Main class, this acts as a container for all other sub-frames in
#   tkinter. from here the steps of simulation are calculated as well.
class MainApplication(tk.Frame):
    def __init__(self, parent, cell_size):
        tk.Frame.__init__(self, parent, bg='#1b1b1b', bd=10)
        self.root = parent
        self.pack()
        self.controlBar = ControlBar(self)
        self.board = Board(self, cell_size)
        self.info = Info(self)
        self.genInfo = GenereationInfo(self)
        # self.gen_lbl = tk.Label(self, text='Generations: %s' % str(self.gens))
        # self.gen_lbl.config(bg='#1b1b1b', fg="white")
        # self.alive_lbl = tk.Label(self, text='Population: %s' % str(self.alive))
        # self.alive_lbl.config(bg='#1b1b1b', fg="white", padx=3)


        self.controlBar.pack(side='bottom', fill='x', pady=7)
        self.genInfo.pack(side='bottom', anchor='w', pady=5)
        # self.gen_lbl.pack(side='bottom', anchor='w', pady=5)
        # self.alive_lbl.pack(side='right', pady=5)
        self.board.pack(side='left', fill='x', padx= 5, expand=False)
        self.info.pack(side='right', fill='both', padx= 5, expand=True)
        text = tk.Label(text='Made by Thony Price and Niklas Linqvist for DD1349')
        text.config(bg='#1b1b1b', fg="white")
        text.pack(side='bottom', anchor='e')

    def runGame(self):
        listOfCells = self.createClasses(self.board.plan)
        row_sz = len(self.board.plan[0])
        col_sz = len(self.board.plan)
        ol_plan = self.board.plan
        while self.controlBar.btns.state:
            self.genInfo.alive = sum([x.getValue() for x in listOfCells])
            self.genInfo.alive_lbl.configure(
            text='Population: %s' % str(self.genInfo.alive)
            )
            if self.genInfo.alive == 0:
                break
            self.updateCells(listOfCells)
            plan = self.updateBoard(listOfCells, row_sz, col_sz)
            if plan == ol_plan:
                break
            ol_plan = plan
            self.genInfo.gens += 1
            self.genInfo.gen_lbl.configure(
                text='Generations: %s' % str(self.genInfo.gens)
                )
            listOfCells = self.createClasses(plan)
            self.board.showBoard(plan)
            self.root.update()
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
        self.bind("<Button-1>", self.switchCell)

    def resizeCanvas(self, bd):
        self.config(
            width=len(bd[0]) * self.sz + 1,
            height=len(bd) * self.sz + 1
        )

    def switchCell(self, event=None):
        """Switch the value of a cell on click"""
        print("Click-test works")

    def showBoard(self, bd):
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
