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
    digits = {}
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

    # load and store to files
    def load(self, fileName = []):
        if fileName == []:
            print('empty')
        #open the file and read the board
        try :
            f = open(fileName,'r')
        except FileNotFoundError:
            print('Error opening file',fileName)
            return      
        boxes =f.readlines()
        f.close()
        # check the number of rows is ok
        n2 = len(boxes)
        if n2 != self.nSq:
            print( "Error, File is for a size", n2, 'board',
                   'current board is', self.nSq)
            return
        elif n2 == 4:
            self.digits = {'1','2','3','4'}
        elif n2 == 9:
            self.digits = {'1','2','3','4','5','6','7','8','9'}
        elif n2 == 16:
            self.digits = {'1','2','3','4','5','6','7','8','9',
                      "A","B","C","D","E","F",'0'}
        else:
            print( 'File error.', n2,'rows (should be 4, 9, or 16)')
            return
        
        # check length of rows
        for k in range(n2):
            rowLen = len(boxes[k])-1
            if  rowLen != n2: # 1 for the line feed
                print( 'File error. Row',k+1,'is', rowLen,
                       'characters.  Expecting',n2)
                return
            
        # populate the board
        for row in range(n2):
            rowLine = boxes[row]
            for col in range(n2):
                v = rowLine[col]
                if not(v in self.digits):
                    v = ' '
                print(v, end = ' ')
            print('')
                
        print(self.digits)
        pass
    
    def save(self, fileName = []):
        if fileName == []:
            print('empty')
        pass

    def clear(self):
        pass

    def restart(self):
        pass

    def check(self):
        pass

    def undo(self): # was called backup
        pass

    def print(self):
        """Display the sudoku to the console using unicode box characters"""
        print('display of Sudoku board')
        # top line
        print('\u250c',end='')
        for j in range(self.n-1):
            for k in range(self.n):
                print('\u2500',end='')
            print('\u252c',end='')
        for j in range(self.n):
            print('\u2500',end='')
        print('\u2510')
        #ordinary line
        c=1
        for j in range(self.n):
            print('\u2502',end='')
            for k in range(self.n):
                print(c,end='')
                c +=1
        print('\u2502')
                
        #box line
        print('\u251c',end='')
        for j in range(self.n-1):
            for k in range(self.n):
                print('\u2500',end='')
            print('\u253c',end='')
        for j in range(self.n):
            print('\u2500',end='')
        print('\u2524')
        
        #ordinary line #2
        c=1
        for j in range(self.n):
            print('\u2502',end='')
            for k in range(self.n):
                print(c,end='')
                c +=1
        print('\u2502')

        #bottom line
        print('\u2514',end='')
        for j in range(self.n-1):
            for k in range(self.n):
                print('\u2500',end='')
            print('\u2534',end='')
        for j in range(self.n):
            print('\u2500',end='')
        print('\u2518')
        

# main routine
# This creates a window
root = Tk()

# start the game
game = SudokuGame(root)
#game.mainloop()
# for debug
game.print()

    

    
