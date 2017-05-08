# Unittesting

import unittest
import test_data as test
import tkinter as tk
import Window as win
import CellClass as cc

class TestStringMethods(unittest.TestCase):

    def test_updateCells(self):
        cell_sz = 1
        root = tk.Tk()
        row_sz = len(test.board1[0])
        col_sz = len(test.board1)
        test_app = win.MainApplication(root, cell_sz)
        listOfCells = test_app.createClasses(test.board1)
        test_app.updateCells(listOfCells)
        self.assertEqual(
            test_app.updateBoard(listOfCells, row_sz, col_sz),
            test.board1_update1
        )

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
