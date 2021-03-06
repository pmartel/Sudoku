""" This file is a sudoku game.  Later I'll add a solver """
from tkinter import *
from Cell import *
from SudokuMenu import *
from BoxPrint import BoxPrint
# the sudoku module is getting kind of big.  Break out the guessing module
#then solutions in general
#from guessing import guessingSolve 

from Solver import SudokuSolver


class SudokuGame(Frame):
    cell=[]
    undoStack = []
    focusIdx = 0
    # dictionary holding valid characters for a given size game
    digits = { 4: (' ','1','2','3','4')}
    digits[9] = (' ','1','2','3','4','5','6','7','8','9')
    digits[16] = (' ','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F')
    digList = []
    #parameters
    boxSize = 50
    xOff = 3
    yOff = 3
    extraWidth = 100 # for buttons
    
    def __init__(self, tk, n=3):
        """ tk is the tkinter object that will display the board.
            n is a number that specifies the board size n^2 x n^2
            Normally 3, it could be 4 (use hex digits).  Possibly 2 for
            a kid. """
        # things related to the number of cells
        self.n = n
        self.nDigits = n * n
        self.numCells = self.nDigits * self.nDigits
        size = self.boxSize * (self.nDigits +1)
        self.size = size
        #get a list of the 'legal' digits
        digList = self.digits[self.nDigits]
        self.digList = list(digList[1:len(digList)])

        self.gString = '{0}x{1}'.format(size+self.extraWidth,size)

        # set up the graphics
        self.tk = tk
        tk.title('Sudoku - Phil Martel')
        tk.geometry(self.gString)
        super(SudokuGame,self).__init__(tk)

        # set up the cells. Everything is on a canvas
        self.can = Canvas(tk, height=self.nDigits*self.boxSize+self.yOff,
                          width=self.nDigits*self.boxSize+self.xOff+
                          self.extraWidth, bg='light gray')
        self.can.grid(row=1,column=1)

        #draw outline
        for x in range(0,self.nDigits+1):
            if x % 3 == 0:
                wid = 3
            else:
                wid = 1
            s = self.boxSize # aliases
            yo = self.yOff
            xo = self.xOff
            xyMax = self.size -s
            
            self.can.create_line(0,x*s+yo,xyMax+xo,x*s+yo,fill='black',width=wid)
            self.can.create_line(x*s+xo,0,x*s+xo,xyMax+yo,fill='black',width=wid)

        #generate the cells.  Each cell will have a entry widget attached
        # to the canvas
        for k in range(self.numCells):
            ( r, c) = divmod(k, self.nDigits)
            rr = r // self.n
            cc = c // self.n
            b = rr * self.n + cc
            # this checks that r,c, and b are good
            #print(k,r,c,b)
            self.cell.append(Cell(r,c,b,self.can,self))
        # add the solver
        self.solver = SudokuSolver(self)
        # add a menu
        self.menu = SudokuMenu(self)
        #add buttons
        self.restartButton = Button(tk,command = self.restart, text='Restart')
        self.can.create_window(xyMax+10,10,window=self.restartButton,
                               anchor=NW)       
        self.undoButton = Button(tk,command = self.undo, text='Undo')
        self.can.create_window(xyMax+10,s+10,window=self.undoButton,
                               anchor=NW)       
        self.checkButton = Button(tk,command = self.checkGame, text='Check')
        self.can.create_window(xyMax+10,2*s+10,window=self.checkButton,
                               anchor=NW)       
        self.optButton = Button(tk,command = self.printOptions, text='Options?')
        self.can.create_window(xyMax+10,3*s+10,window=self.optButton,
                               anchor=NW)       
        self.solveButton = Button(tk,command = self.solver.solve, text='Solve')
        self.can.create_window(xyMax+10,4*s+10,window=self.solveButton,
                               anchor=NW)       
        self.guessButton = Button(tk,command = self.solver.guessingSolve,
                                  text='Solve with guessing')
        self.can.create_window(xyMax+10,5*s+10,window=self.guessButton,
                               anchor=NW)       
        #clear board
        #self.clear()

        #set up exit actions
        self.top = self.can.winfo_toplevel()
        self.top.protocol("WM_DELETE_WINDOW", self.__SaveOnClosing)
        pass
    
    def __SaveOnClosing(self):
        ret = self.checkChanged()
        print('checkChanged() returned',ret)
        if ret != 'cancel':
            print('closing Sudoku')
            self.top.destroy()
        pass

    def checkChanged(self):
        """ ask the user if s/he wants to save if the game has changed """
        if len(self.undoStack):
            self.msg = messagebox.askyesnocancel('Save Data?',
                                              'Game is not saved.  Save it?')
            if self.msg == None:
                return 'cancel'
            elif self.msg == 'yes':
                self.save()
                return 'yes'
            else:
                return 'no'
        
    def checkGame(self):
        ''' see if there are any duplicate digits '''
        gameOk = True
        full = 0
        for k in range(self.numCells):
            cel = self.cell[k]
            v = cel.getv()
            if v == ' ' or v == '': # a blank is ok
                continue
            full +=1
            for n in range(k+1,self.numCells):
                #print('cells',n,k)
                #all cells below k have been checked
                nCel = self.cell[n]
                nV = nCel.getv()
                if v != nV:
                    continue
                # same digit
                #print( 'same digit in cells {0}, {1}'.format(k,n))
                if cel.row == nCel.row:
                    gameOk = False
                    break
                elif cel.col == nCel.col:
                    gameOk = False
                    break
                elif cel.box == nCel.box:
                    gameOk = False
                    break
                pass #inner loop 
            if not gameOk :
                break
            pass
        
        #display info
        if gameOk :
            print('game is ok')
            if full == self.numCells:
                print("Congratulations! You win!!");
        else:
            print('Duplicate digits in')
            print('idx\trow\tcol\tbox\tval')
            print('{0}\t{1}\t{2}\t{3}\t{4}'.format(k,cel.row,cel.col,
                                                   cel.box,v))
            print('{0}\t{1}\t{2}\t{3}\t{4}'.format(n,nCel.row,nCel.col,
                                                   nCel.box,nV))
        return gameOk       

    # load and store to files
    def load(self, fileName = []):
        print('SudokuGame.load({0})'.format(fileName))
        if fileName == []:
            print('No file selected')
        #open the file and read the board
        try :
            f = open(fileName,'r')
        except FileNotFoundError:
            print('Error opening file <{0}>'.format(fileName))
            return      
        boxes =f.readlines()
        f.close()
        # check the number of rows is ok
        n2 = len(boxes)
        if n2 != self.nDigits:
            print( "Error, File <{0}> is for a size".format(filename),
                   n2, 'board', 'current board is', self.nDigits)
            return
        
        # check length of rows
        for k in range(n2):
            rowLen = len(boxes[k])-1
            if  rowLen != n2: # 1 for the line feed
                print( 'File error in {0}.'.format(fileName), 'Row',k+1,
                       'is', rowLen, 'characters.  Expecting',n2)
                return
            
        # populate the board
        for row in range(n2):
            rowLine = boxes[row]
            for col in range(n2):
                v = rowLine[col]
                if not(v in self.digits[n2]):
                    v = ' '
                n = row * n2 + col
                c = self.cell[n]  
                c.setv(v)
                c.origVal = v # so that reload works
        self.undoStack.clear()  # don't undo past a load point          
#        pass
    
    def save(self, fileName = []):
        if fileName == []:
            print('No file selected')
        #open the file and write the board
        try :
            f = open(fileName,'w')
        except FileNotFoundError:
            print("Error, can't write to file <{0}>".format(fileName))
            return
        for row in range(self.nDigits):
            rowline=''
            for col in range(self.nDigits):
                n = row * self.nDigits + col
                c = self.cell[n]
                v = c.getv()
                if len(v) > 1:
                    print( "long string <{0}> at r{1} c{2}".format(v,row,col))
                if v == ' ':
                    v = '.'
                rowline += v
            print(rowline)
            f.writelines(rowline+'\n')
        f.close()
        #clear undo stack.  We may want a different indicator that
        # nothing has changed after a save
        self.undoStack.clear()          
        pass

    def clear(self):
        for n in range(self.numCells):
            c = self.cell[n]
            c.setv(' ')
            c.origVal = ' '
        self.undoStack.clear() # don't undo past a clear point
        pass

    def printOptions(self):
        self.can.update()
        active = self.focusIdx
        print('active <{0}>'.format(active))
        l = self.solver.findOptions(active,0)
        print('Options for cell {0}: {1}'.format(active,l))
              
    def restart(self):
        for n in range(self.numCells):
            c = self.cell[n]
            c.setv(c.origVal)
        self.undoStack.clear() # don't undo past a restart point
        pass

    def undo(self): # was called backup
        if len(self.undoStack) > 0:
            uData = self.undoStack.pop()
            idx = uData[0]
            print('undo cell',idx,'from',self.cell[idx].getv(),'to "',
                  uData[1],'"') # uData[1] is usually blank
            self.cell[uData[0]].setv(uData[1])
            return uData[0]
        else:              
            print('undo stack empty')
            return None
        pass

    
    def print(self):
        """ prettyprint the board """
        data = []
        for row in range(self.nDigits):
            rowline=''
            for col in range(self.nDigits):
                n = row * self.nDigits + col
                c = self.cell[n]
                v = c.getv()
                if len(v) > 1:
                    print( "long string <{0}> at r{1} c{2}".format(v,row,col))
                rowline += v
            data.append(rowline)
            pass
        BoxPrint(data)
        pass

    def quit(self):
        print( 'quitting')

            
###########################################################
# main routine
###########################################################
# This creates a window
root = Tk()

# start the game
game = SudokuGame(root)

# for debug
c = game.cell
c10 =game.cell[10]
c52 =game.cell[52]

#game.mainloop()


    

    
