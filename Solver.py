""" This  is the solver code that was in SudokuGame.  Making it a class
makes it easier to keep things like guess stacks arount """
import collections # for named tuples

import time
from Guesser import Guesser

class SudokuSolver():
    guessStack = []
    idxStack=[]
    def __init__(self,game):
        self.game=game
        self.guesser = Guesser(self)

    def guessingSolve(self):
        game = self.game
        self.guessStack=[]
        self.idxStack=[]
        bad = False
        print('guessing solver')
        while True:
            # try the deterministic solver
            self.solve()
            blanks = self.countEmpty()
            if blanks == 0:
                break #done
            [bad, cellIdx,guess] = self.guesser.getGuesses()
            if bad:
                #input('hit enter')
                [ok, cellIdx, guess] = self.guesser.backUp()
                if not ok :
                   print( "No guesses left. Can't solve")
                   return
                pass
            print( '===>guessing cell',cellIdx,'is',guess)
            game.cell[cellIdx].setvStack(guess)
            pass #while True
        pass
    

    # non-guess solver code
    def solve(self):
        passes = 0
        oldBlanks = self.countEmpty()
        while True:
            blanks = self.countEmpty()
            if blanks == 0:
                break
            passes +=1
            print( 'Solving puzzle. Pass {0}.  Initially {1} empty cells.'
                   .format(passes,blanks))
            print('Test 1 - cells with only one option')
            for n in range(self.game.numCells):
                if self.game.cell[n].getv() !=' ':
                    continue # skip already filled cells
                t = self.findOptions(n,1)
                if len(t) == 1:
                    print('Cell',n,'can only be',t[0])
                    self.game.cell[n].setvStack(t[0])
                    self.game.can.update()
                    time.sleep(.1)
            if not self.game.checkGame():
                break
            blanks = self.countEmpty()
            if blanks == 0:
                break
            print(
                'Test 2 - by digits check for only one cell in a row can be it');
            for d in self.game.digList:
                # make sure that the options lists are up to date
                for n in range(self.game.numCells):
                    self.findOptions(n,1)
                for r in range(self.game.nDigits): # number of digits == cells in row
                    rowDig = []
                    for c in  range(self.game.nDigits):
                        idx = self.rc2idx(r,c)
                        if d in self.game.cell[idx].optList:
                            rowDig.append(idx)
                        pass # for c
                    if len(rowDig) == 1:
                        if self.game.cell[rowDig[0]].getv() == ' ':
                            print( 'only',d,'in row',r,'is index',rowDig[0])
                            self.game.cell[rowDig[0]].setvStack(d)
                            self.game.can.update()
                            time.sleep(.1)
                    pass # for r
            if not self.game.checkGame():
                break
            blanks = self.countEmpty()
            if blanks == 0:
                break
            print(
                'Test 3 - by digits check for only one cell in a col can be it');
            for d in self.game.digList:
                # make sure that the options lists are up to date
                for n in range(self.game.numCells):
                    self.findOptions(n,1)
                for c in range(self.game.nDigits): # number of digits == cells in col
                    colDig = []
                    for r in  range(self.game.nDigits):
                        idx = self.rc2idx(r,c)
                        if d in self.game.cell[idx].optList:
                            colDig.append(idx)
                        pass # for r
                    if len(colDig) == 1:
                        if self.game.cell[colDig[0]].getv() == ' ':
                            print( 'only',d,'in col',c,'is index',colDig[0])
                            self.game.cell[colDig[0]].setvStack(d)
                            self.game.can.update()
                            time.sleep(.1)
                    pass # for c
            if not self.game.checkGame():
                break
            blanks = self.countEmpty()
            if blanks == 0:
                break
            print(
                'Test 3 - by digits check for only one cell in a box can be it')
            for d in self.game.digList:
                for b in range(self.game.nDigits): # number of digits == cells in box
                    # make sure that the options lists are up to date
                    for n in range(self.game.numCells):
                        self.findOptions(n,1)
                    # find a row, col in b, get the index
                    r = (b // 3)* 3
                    c = (b * 3) % 9
                    idx = self.rc2idx(r,c)
                    bList = self.boxList(idx)
                    boxDig=[]
                    #print('b',b,'list',bList)
                    for idx in bList:
                        c = self.game.cell
                        #print(idx,c[idx].optList, '1' in c[idx].optList)
                        if d in self.game.cell[idx].optList:
                            boxDig.append(idx)
                        pass # for idx
                    # this was over too far so it got executed for every idx :(
                    if len(boxDig) == 1:
                        if self.game.cell[boxDig[0]].getv() == ' ':
                            print( 'only',d,'in box',b,'is index',
                                   boxDig[0])
                            self.game.cell[boxDig[0]].setvStack(d)
                            self.game.can.update()
                            time.sleep(.1)
                    pass # for b
                pass #for d
            
            if not self.game.checkGame():
                break
            # check if we're done or stuck
            blanks = self.countEmpty()
            if blanks == 0:
                break
            elif oldBlanks == blanks:
                break
            else:
                oldBlanks = blanks
            pass # end of while loop
        if blanks == 0:
            print( 'Sudoku solved')
        else:
            print('Sudoku solver stuck')
    
    pass

# solver related functions
    def findOptions(self, idx, flag):
        ''' return a list of possible values for cell[idx]. if flag is 1,
 a filled cell only has it's value, otherwise other options show up '''
        if flag == 1:
            v = self.game.cell[idx].getv()
            if v != ' ':
                self.game.cell[idx].optList=[v]
                return [v]
            
        l = self.game.digits[self.game.nDigits]
        
        l = list(l[1:len(l)])
        rL = self.rowList(idx)
        rL.remove(idx) # leave active cell's value (if any) on list
        for n in rL:
            v = self.game.cell[n].getv()
            if v in l:
                l.remove(v)

        # for the col of the active cell
        cL = self.colList(idx)
        cL.remove(idx) # leave active cell's value (if any) on list
        for n in cL:
            v = self.game.cell[n].getv()
            if v in l:
                l.remove(v)

        # for the box of the active cell
        bL = self.boxList(idx)
        bL.remove(idx) # leave active cell's value (if any) on list
        for n in bL:
            v = self.game.cell[n].getv()
            if v in l:
                l.remove(v)
        self.game.cell[idx].optList = l
        return l
    

    def countEmpty(self):
        count = 0
        for n in range(self.game.numCells):
            if self.game.cell[n].getv() == ' ':
                count += 1
        return count

    def rc2idx(self,r,c):
        """ takes a row and column number of a cell and returns its index """
        return c + r * self.game.nDigits

    def rowList(self, idx):
        """ returns a list of indices of cells in the same row as idx """
        rL = []
        r = self.game.cell[idx].row
        for c in range(self.game.nDigits):
            n = self.rc2idx(r,c)
            rL.append(n)
        return rL
            

    def colList(self, idx):
        """ returns a list of indices of cells in the same column as idx """
        cL = []
        c = self.game.cell[idx].col
        for r in range(self.game.nDigits):
            n = self.rc2idx(r,c)
            cL.append(n)
        return cL

    def boxList(self, idx):
        """ returns a list of indices of cells in the same box as idx """
        bL = []
        r = self.game.cell[idx].row
        c = self.game.cell[idx].col
##        print('boxList({0}) r{1} c{2} b{3}'.format
##              (idx,r,c,self.game.cell[idx].box))
        # find lower limit r, c of box
        n = self.game.n
        r = (r // n) * n
        c = (c // n) * n
##        print('new rc',r,c)
        for r1 in range( r,r+n):
            for c1 in range(c,c+n):
                idx = self.rc2idx(r1,c1)
                bL.append(idx)
##        print(bL)
        return bL
