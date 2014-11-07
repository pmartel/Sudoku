""" This file is a sudoku game.  Later I'll add a solver """

from tkinter import *

class Cell:
    row = []
    col = []
    box = []
    val = []
    origVal = []
    
    def __init__(self, r, c, box, val):
        self.row = r
        self.col = c
        self.box = box
        self.val = val
        self.OrigVal = val

    def reset(self):
        self.val = self.origVal

    def get(self):
        return self.val

    def set(self,v):  # note: this overloads the builtin class set
        if self.val == [] :
            self.val = v
        else:
            # some warning if you try to load over a non-blank?
            pass

    
class SudokuGame:
    def __init__(self, tk, n=3):
        """ tk is the tkinter object that will display the board.
            n is a number that specifies the board size n^2 x n^2
            Normally 3, it could be 4 (use hex digits).  Possibly 2 for
            a kid. """
        self.tk = tk
        self.n = n
        self.nSq = n * n
        self.numCells = self.nSq * self.nSq
        for k in range(self.numCells):
            ( r, c) = divmod(k, self.nSq)
            rr = r // self.n
            cc = c // self.n
            b = rr * self.n + cc
            print(k,r,c,b)
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

    def undo(self): # was called backup
        pass
  
# main routine
# This creates a window
root = Tk()

# start the game
game = SudokuGame(root,2)
#game.mainloop()
# for debug

    

    
