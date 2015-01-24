""" This file is a sudoku game.  Later I'll add a solver """
# TO-DO: save game on close
from tkinter import *
#import tkmessagebox
from Cell import *
from SudokuMenu import *
from BoxPrint import BoxPrint

class SudokuGame(Frame):
    cell=[]
    undoStack = []
    
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
        #clear board
        #self.clear()

        #set up exit actions
        self.top = self.can.winfo_toplevel()
        self.top.protocol("WM_DELETE_WINDOW", self.__SaveOnClosing)
        pass
    
    def __SaveOnClosing(self):
        ret = self.checkChanged()
        print('checkchanged returned',ret)
        if ret != 'cancel':
            print('closing Save on')
            self.top.destroy()
        pass

    def checkChanged(self):
        """ ask the usere if s/he wants to save if the text is changed """
        if len(self.undoStack):
            self.msg = messagebox.askyesnocancel('Save Data?',
                                              'Text is not saved.  Save it?')
            if self.msg == None:
                return 'cancel'
            elif self.msg == 'yes':
                self.save()
            return 'ok'
        
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

    def restart(self):
        for n in range(self.numCells):
            c = self.cell[n]
            c.setv(c.origVal)
        self.undoStack.clear() # don't undo past a restart point
        pass

    def check(self):
        pass

    def undo(self): # was called backup
        if len(self.undoStack) > 0:
            uData = self.undoStack.pop()
            print('undo',uData)
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



###########################################################
# main routine
###########################################################
# This creates a window
root = Tk()

# start the game
game = SudokuGame(root)
#game.mainloop()
# for debug
c0 = game.cell[0]
c10 =game.cell[10]
c52 =game.cell[52]



    

    
