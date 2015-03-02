""" this holds the guessing part of the solver. """
from Cell import Cell

class Guesser():
    possibilities = [] #array of all possibilites by cell
    # these two lists are treated as stacks guessIdx stores the cells guessed
    # guessStack holds the possible guesses for each guessIdx.
    guessIdx=[]
    guessStack=[]
    possibilities =[]
    
    def __init__(self, solver ):
        self.guessIdx =[]
        self.guessStack = []
        self.solver = solver
        #self.findPossibilities()
        pass

    def backUp(self):
        ok = True
        #last guess is on guessIdx stack but the value is not readily available
        #read if from the cell
        while len( self.guessIdx ) > 0:
            lastIdx = self.guessIdx[-1]
            game = self.solver.game
            c = game.cell[lastIdx]
            guess=c.getv()
            print('bad guess: cell',lastIdx,'was not', guess)
            undoVal = -1
            while undoVal != lastIdx:
                undoVal = game.undo()
                if undoVal == None:
                    print('No solution')
                    return
                pass
            # Is there another guess at this level?
            if len( self.guessStack[-1] ) > 0:
                guess = self.guessStack[-1].pop()
                return [ok, lastIdx, guess]
            else: # back up a level
                self.guessIdx.pop()
                self.guessStack.pop()
                pass
            pass #while len( guessIdx ) > 0:
        # no more guesses
        return [ False, [],[]]
        pass 

    def displayStacks(self):
        print('Guess Stack')
        print('Cell    Possibilities')
        for n in range(len(self.guessIdx)):
            print(self.guessIdx[n],self.guessStack[n])
            pass
        pass
    
    def findPossibilities(self):
        ''' set up a list of all possibilities for the game as it is now '''
        self.possibilities = []
        game = self.solver.game
        for n in range(game.numCells):
            self.possibilities.append(self.solver.findOptions(n,1))
            pass
        pass
    
    def getGuesses(self):
        """ Find the shortest options list.  If there's a cell with an empty
         list the guess was bad, back up and retry.
         A singleton list doesn't count; that's just a filled cell."""
        self.findPossibilities()
        bad = False
        game = self.solver.game
        shortest = 0
        opt = game.digList # list of all digits
        for n in range(game.numCells):
            o1 = self.possibilities[n]
            if len(o1) == 0:
                #bad value, try backing out
                print('no options for cell',n)
                bad = True
                break
            # if o1 is a singleton, the cell has a fixed value
            elif len(o1) > 1: 
                if len(o1) < len(opt):
                    opt = o1
                    shortest =n
                    pass
                pass
            pass
        # At this point, if bad is true, we have to back up. Otherwise, we
        # append to the guessIdx and guessStack lists
        if not bad:
            self.displayStacks()
            self.guessIdx.append(shortest)
            g = opt.pop()
            self.guessStack.append(opt)
            return [bad, shortest, g]
        else:
            return [bad,None, None]
    pass
        

    
