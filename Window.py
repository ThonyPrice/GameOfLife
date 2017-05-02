# Authors: Thony Price, Niklas Lindqvist
# Last revision: 2017-04-28

# This file contains a class that initializes a tkinter window which
# are able to run the cellular simulation, Conway's Game of Life

import tkinter as tk
import saved_boards as gameplans

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

    def just(self, val):
        print("HERE", val)

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
        self.btn.config(bg='green')

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
        return

class Board(tk.Canvas):
    def __init__(self, parent, plan, sz):
        tk.Canvas.__init__(self, parent,
            width=len(plan[0])*sz+1,
            height=len(plan)*sz+1,
            highlightthickness=0,
            bd=0,
            bg='grey'
        )
        startboard = gameplans.blank
        self.pack()
        self.showBoard(startboard)

    def showBoard(self, bd):
        sz = 12
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
