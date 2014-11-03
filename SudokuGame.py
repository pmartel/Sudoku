""" This file is a sudoku game.  Later I'll add a solver """

from tkinter import *

class SudokuGame:
    def __init__(self, tk, n=3):
        """ tk is the tkinter object that will display the board.
            n is a number that specifies the board size n^2 x n^2
            Normally 3, it could be 4 (use hex digits).  Possibly 2 for
            a kid. """
        pass

    def load(self, fileName):
        pass

    def save(self, fileName):
        pass

    def clear(self):
        pass

    def restart(self):
        pass

    def check(self):
        pass

    def backup(self):
        pass
  
# main routine
# This creates a window
root = Tk()

# start the game
game = SudokuGame(root)
#game.mainloop()
# for debug

    

    
