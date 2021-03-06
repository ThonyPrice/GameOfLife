#!/usr/bin/env python
"""This file is responsible for the GUI in the game"""

__author__ = "Thony Price, Niklas Lindqvist"
__version__ = "1.0.1"
__email__ = "thonyp@kth.se, nlindq@kth.se"

import tkinter as tk
import saved_boards as gameplans
import CellClass
import time
import webbrowser
from pygame import mixer

class ControlBar(tk.Frame):
    """Container for buttons and sliders"""
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.dropdown = Dropdown(self)
        self.btns = Btns(self)
        self.speedSlider = SpeedSlider(self)

        self.dropdown.pack(side='left')
        self.speedSlider.pack(side='left')
        self.btns.pack(side='left')

class Dropdown(tk.Frame):
    """Displays a dropdown with boards that the user can load into the board"""
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
        """initalize and start boards with the selected board from dropdown"""
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

class Btns(tk.Frame):
    """Container for all buttons"""
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.state = False
        """Create button that runs the simulation"""
        self.run_btn = tk.Button(
            self, width = 7,
            text = 'Run',
            command = lambda: self.run()
        ).pack(side='left')
        """Create button that stops it"""
        self.stop_btn = tk.Button(
            self, width = 7,
            text = 'Stop',
            command = lambda: self.stop()
        ).pack(side='left')
        """Create button that mutes music"""
        self.mute_btn = tk.Button(
            self, width = 7,
            text = 'Mute Music',
            command = lambda: self.mute()
        )
        self.mute_btn.pack(side='left')
        """Create button that quits program"""
        self.quit_btn = tk.Button(
            self, width = 7,
            text = 'Quit',
            command = lambda: self.quit()
        ).pack(side='left')

    def run(self):
        """Run the game"""
        self.state = True
        self.parent.parent.runGame()

    def stop(self):
        self.state = False

    def mute(self):
        if self.mute_btn["text"] == "Mute Music":
            mixer.music.pause()
            self.mute_btn["text"] = "Play Music"
        else:
            mixer.music.unpause()
            self.mute_btn["text"] = "Mute Music"

class SpeedSlider(tk.Frame):
    """Add a slider that controls the simulation speed"""
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text='Generations per second:').pack(side='left')
        self.scale = tk.Scale(self, from_=1, to=20, orient='horizontal')
        self.scale.set(1)
        self.scale.pack(side='left')

class Info(tk.Frame):
    """Add a frame in window that contains information about the game"""
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
        """Direct user to hyperlink"""
        webbrowser.open_new(r"https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life")

class GenereationInfo(tk.Frame):
    """Labels with information of generations and population"""
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

class MainApplication(tk.Frame):
    """
    Frame initialized with root. This frame will contains all other frames
    as subframes. Each other window will have this as parent allowing
    operations in subframes affect sibling frames
    """
    def __init__(self, parent, cell_size):
        tk.Frame.__init__(self, parent, bg='#1b1b1b', bd=10)
        self.root = parent
        self.pack()
        self.controlBar = ControlBar(self)
        self.board = Board(self, cell_size)
        self.info = Info(self)
        self.genInfo = GenereationInfo(self)

        # Pack containers in frame
        self.controlBar.pack(side='bottom', fill='x', pady=0)
        self.genInfo.pack(side='bottom', anchor='w', pady=5)
        # self.gen_lbl.pack(side='bottom', anchor='w', pady=5)
        # self.alive_lbl.pack(side='right', pady=5)
        self.board.pack(side='left', fill='x', padx= 5, expand=False)
        self.info.pack(side='right', fill='both', padx= 5, expand=True)
        text = tk.Label(text='Made by Thony Price and Niklas Linqvist for DD1349')
        text.config(bg='#1b1b1b', fg="white")
        text.pack(side='bottom', anchor='e', padx= (20,20), pady = (0,9))

    def runGame(self):
        """
        Initalize list with cells. While no interrupts occurs,
        the board updates continously in the while-loop below
        """
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
        """init a list of cellObjects"""
        listCells = []
        for row in range(len(board)):
            for col in range(len(board[0])):
                listCells.append(CellClass.CellClass(int(board[row][col]), row , col,
                    self.getListNeighbourValue(row, col, board)))
        return listCells

    def getListNeighbourValue(self, row, col, board):
        """Create a list with all 8 values of neighbours of a cell"""
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

class Board(tk.Canvas):
    """This class inits a canvas on which the game plan is displayed"""
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
        """Resize canvas to a given board"""
        self.config(
            width=len(bd[0]) * self.sz + 1,
            height=len(bd) * self.sz + 1
        )

    def switchCell(self, event=None):
        """Switch the value of a cell on click"""
        cx = event.x
        cy = event.y
        bx = cx//self.sz
        by = cy//self.sz
        board = self.plan
        if bx < len(board[0]) and by < len(board):
            if board[by][bx] == 0:
                board[by][bx] = 1
            else:
                board[by][bx] = 0
            self.showBoard(board)

    def showBoard(self, bd):
        """Given all values of bd, display the boards on canvas"""
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
