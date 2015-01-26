""" This file is a sudoku game.  Later I'll add a solver """
# TO-DO: save game on close
from tkinter import *
#import tkmessagebox
from Cell import *
from SudokuMenu import *
from BoxPrint import BoxPrint

import time

class SudokuGame(Frame):
    cell=[]
    undoStack = []
    focusIdx = []
    # dictionary holding valid characters for a given size game
    digits = { 4: (' ','1','2','3','4')}
    digits[9] = (' ','1','2','3','4','5','6','7','8','9')
    digits[16] = (' ','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F')
    
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
        self.nSq = n * n
        self.numCells = self.nSq * self.nSq
        size = self.boxSize * (self.nSq +1)
        self.size = size

        self.gString = '{0}x{1}'.format(size+self.extraWidth,size)

        # set up the graphics
        self.tk = tk
        tk.title('Sudoku - Phil Martel')
        tk.geometry(self.gString)
        super(SudokuGame,self).__init__(tk)

        # set up the cells. Everything is on a canvas
        self.can = Canvas(tk, height=self.nSq*self.boxSize+self.yOff,
                          width=self.nSq*self.boxSize+self.xOff+
                          self.extraWidth, bg='light gray')
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
            xyMax = self.size -s
            
            self.can.create_line(0,x*s+yo,xyMax+xo,x*s+yo,fill='black',width=wid)
            self.can.create_line(x*s+xo,0,x*s+xo,xyMax+yo,fill='black',width=wid)

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
        self.solveButton = Button(tk,command = self.solve, text='Solve')
        self.can.create_window(xyMax+10,4*s+10,window=self.solveButton,
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
        if n2 != self.nSq:
            print( "Error, File <{0}> is for a size".format(filename),
                   n2, 'board', 'current board is', self.nSq)
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
        for row in range(self.nSq):
            rowline=''
            for col in range(self.nSq):
                n = row * self.nSq + col
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
        l = self.findOptions(active)
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
            print('undo cell',idx,'from',self.cell[idx].getv(),'to',uData[1])
            self.cell[uData[0]].setv(uData[1])
        else:              
            print('undo stack empty')
        pass

    
    def print(self):
        """ prettyprint the board """
        data = []
        for row in range(self.nSq):
            rowline=''
            for col in range(self.nSq):
                n = row * self.nSq + col
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

    # the solver code
    def solve(self):
        passes = 0
        blanks = 1 # fake starting the loop
        oldBlanks = -1
        while blanks > 0:
            blanks = self.countEmpty()
            passes +=1
            print( 'Solving puzzle. Pass {0}.  Initially {1} empty cells.'
                   .format(passes,blanks))
            print('Test 1 - cells with only one option')
            for n in range(self.numCells):
                if self.cell[n].getv() !=' ':
                    continue # skip already filled cells
                t = self.findOptions(n)
                if len(t) == 1:
                    print('Cell',n,'can only be',t[0])
                    self.cell[n].setv(t[0])
                    self.can.update()
                    time.sleep(.25)
            print( 'Test 2 - by digits check for only one digit per row');
            time.sleep(.5)
            if oldBlanks == blanks:
                break
            else:
                oldBlanks = blanks

        if blanks == 0:
            print( 'Sudoku solved')
        else:
            print('Sudoku solver stuck')


# solver related functions
    def findOptions(self, idx):
        ''' return a list of possible values for cell[idx] '''
        l = self.digits[self.nSq]
        l = list(l[1:len(l)])
        rL = self.rowList(idx)
        rL.remove(idx) # leave active cell's value (if any) on list
        for n in rL:
            v = self.cell[n].getv()
            if v in l:
                l.remove(v)

        # for the col of the active cell
        cL = self.colList(idx)
        cL.remove(idx) # leave active cell's value (if any) on list
        for n in cL:
            v = self.cell[n].getv()
            if v in l:
                l.remove(v)

        # for the box of the active cell
        bL = self.boxList(idx)
        bL.remove(idx) # leave active cell's value (if any) on list
        for n in bL:
            v = self.cell[n].getv()
            if v in l:
                l.remove(v)
        self.cell[idx].optList = l
        return l
    
    #auxiliary functions
    def rc2idx(self,r,c):
        """ takes a row and column number of a cell and returns its index """
        return c + r * self.nSq

    def rowList(self, idx):
        """ returns a list of indices of cells in the same row as idx """
        rL = []
        r = self.cell[idx].row
        for c in range(self.nSq):
            n = self.rc2idx(r,c)
            rL.append(n)
        return rL
            

    def colList(self, idx):
        """ returns a list of indices of cells in the same column as idx """
        cL = []
        c = self.cell[idx].col
        for r in range(self.nSq):
            n = self.rc2idx(r,c)
            cL.append(n)
        return cL

    def boxList(self, idx):
        """ returns a list of indices of cells in the same box as idx """
        bL = []
        r = self.cell[idx].row
        c = self.cell[idx].col
        # find lower limit r, c of box
        r = (r // self.n) * self.n
        c = (c // self.n) * self.n
        for r1 in range( r,r+self.n):
            for c1 in range(c,c+self.n):
                n = self.rc2idx(r1,c1)
                bL.append(n)
        return bL

    def countEmpty(self):
        count = 0
        for n in range(self.numCells):
            if self.cell[n].getv() == ' ':
                count += 1
        return count
    
            
###########################################################
# main routine
###########################################################
# This creates a window
root = Tk()

# start the game
game = SudokuGame(root)

# for debug
c0 = game.cell[0]
c10 =game.cell[10]
c52 =game.cell[52]

game.mainloop()


    

    
