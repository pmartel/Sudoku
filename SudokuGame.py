""" This file is a sudoku game.  Later I'll add a solver """

from tkinter import *

class Cell:
    row = []
    col = []
    box = []
    val = []
    origVal = []
    
    def __init__(self, r, c, box, tk, size):
        self.row = r
        self.col = c
        self.box = box
        self.tk = tk
        self.size=size
        if size == 16:
            self.base = 16
        else:
            self.base = 10
        # set up value and button
        self.val = StringVar()
        self.val.set(' ')
        self.OrigVal = ' '
        self.but = Button(tk, bg='white', command = self.pressed,\
                          relief='groove',padx=10,pady=10,\
                          textvariable=self.val)
        self.but.grid(row=r+1, column=c+1)

    def reset(self):
        self.val = self.origVal

    def getv(self):
        return self.val

    def setv(self,v):  # note: just set() overloads the builtin class set
##        if self.val == ' ':
##            self.val.set(str(v))
##        else:
##            # some warning if you try to load over a non-blank?
##            pass
        self.val.set(str(v))
        
    def pressed(self):
        v = input('? ')
        vInt = int(v,self.base)
        if vInt >= 1 and vInt <= self.size :
            self.setv(vInt)
        else:
            print('Bad value. Should be digit between 1 and',self.size)
        pass
    
class SudokuGame(Frame):
    cell=[]
    def __init__(self, tk, n=3):
        """ tk is the tkinter object that will display the board.
            n is a number that specifies the board size n^2 x n^2
            Normally 3, it could be 4 (use hex digits).  Possibly 2 for
            a kid. """
        # set up the graphics
        self.tk = tk
        tk.title('Sudoku - Phil Martel')
        tk.geometry('500x500')
        super(SudokuGame,self).__init__(tk)

        # set up the cells
        lab1 = Label(tk,text='  ')# this pushes the grid away from top-left
        lab1.grid(row=0,column=0)
        self.n = n
        self.nSq = n * n
        self.numCells = self.nSq * self.nSq
        for k in range(self.numCells):
            ( r, c) = divmod(k, self.nSq)
            rr = r // self.n
            cc = c // self.n
            b = rr * self.n + cc
            # this checks that r,c, and b are good
            #print(k,r,c,b)
            self.cell.append(Cell(r,c,b,tk,self.nSq))
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
game = SudokuGame(root)
#game.mainloop()
# for debug

    

    
