""" This file is a sudoku game.  Later I'll add a solver """

from tkinter import *
#import tkmessagebox
from Cell import *
from SudokuMenu import *

class SudokuGame(Frame):
    cell=[]

    # dictionary holding valid characters for a given size game
    digits = { 4: (' ','1','2','3','4')}
    digits[9] = (' ','1','2','3','4','5','6','7','8','9')
    digits[16] = (' ','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F')
    
    #parameters
    boxSize = 50
    xOff = 3
    yOff = 3

    def __init__(self, tk, n=3):
        """ tk is the tkinter object that will display the board.
            n is a number that specifies the board size n^2 x n^2
            Normally 3, it could be 4 (use hex digits).  Possibly 2 for
            a kid. """
        # things related to the number of cells
        self.n = n
        self.nSq = n * n
        self.numCells = self.nSq * self.nSq
        size = self.boxSize * (self.nSq +1)
        self.gString = '{0}x{1}'.format(size,size)

        # set up the graphics
        self.tk = tk
        tk.title('Sudoku - Phil Martel')
        tk.geometry(self.gString)
        super(SudokuGame,self).__init__(tk)

        # set up the cells. Everything is on a canvas
        self.can = Canvas(tk, height=self.nSq*self.boxSize+self.yOff,\
                          width=self.nSq*self.boxSize+self.xOff,\
                          bg='light gray')
        self.can.grid(row=1,column=1)

        #draw outline
        for x in range(0,self.nSq+1):
            if x % 3 == 0:
                wid = 3
            else:
                wid = 1
            s = self.boxSize # aliases
            yo = self.yOff
            xo = self.xOff
            self.can.create_line(0,x*s+yo,500,x*s+yo,fill='black',width=wid)
            self.can.create_line(x*s+xo,0,x*s+xo,500,fill='black',width=wid)

        #generate the cells.  Each cell will have a entry widget attached
        # to the canvas
        for k in range(self.numCells):
            ( r, c) = divmod(k, self.nSq)
            rr = r // self.n
            cc = c // self.n
            b = rr * self.n + cc
            # this checks that r,c, and b are good
            #print(k,r,c,b)
            self.cell.append(Cell(r,c,b,self.can,self))
        # add a menu
        self.menu = SudokuMenu(self)
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
        """Display the sudoku to the console using the boxPrint routine
            
            """
        print('display of Sudoku board')
        # top line
        print('\u250f',end='')
        for j in range(self.n-1):
            for k in range(self.n):
                print('\u2501',end='')
            print('\u252f',end='')
        for j in range(self.n):
            print('\u251f',end='')
        print('\u2513')
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
c = game.cell[0]
e = c.ent


    

    
