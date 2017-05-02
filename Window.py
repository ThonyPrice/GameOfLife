# Authors: Thony Price, Niklas Lindqvist
# Last revision: 2017-04-28

# This file contains a class that initializes a tkinter window which
# are able to run the cellular simulation, Conway's Game of Life

import tkinter as tk

class ControlBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # self.pack()
        self.dropdown = Dropdown(self)
        self.runBtn = RunBtn(self)
        self.speedSlider = SpeedSlider(self)

        self.dropdown.pack(side='left')
        self.speedSlider.pack(side='left')
        self.runBtn.pack(side='left')

class Dropdown(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tkvar = tk.StringVar(parent)
        choices = self.getBoards()
        option = tk.OptionMenu(self, tkvar, *choices)
        tkvar.set('Select board')
        option.config(width=15)
        option.pack()

    def getBoards(self):
        # TODO: Here som files containing boards should be read
        #   and put into this dictionary along with values.
        test_data = {
            'Clear', 'Glider', 'Shooter', 'Blinker', 'Ship'
        }
        return test_data

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
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack()
        tk.Label(self, text="MAIN APP").pack()
        self.controlBar = ControlBar(self)

        test_board = [
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

        self.board = Board(self, test_board, 24)

        self.board.pack(side='top')
        self.controlBar.pack(side='top', fill="x")

class Board(tk.Canvas):
    def __init__(self, parent, plan, sz):
        tk.Canvas.__init__(self, parent,
            width=len(plan[0])*sz+1,
            height=len(plan)*sz+1,
            highlightthickness=0,
            bd=0,
            bg='grey'
        )
        self.pack()
        self.showBoard(plan, sz)

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
